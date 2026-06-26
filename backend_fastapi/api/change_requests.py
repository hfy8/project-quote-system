"""FastAPI 路由 - 变更申请 (迁移版)"""

import json
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from core.models.change_request import ChangeRequest
from core.models.quotation import Quotation
from core.models.module import Module
from core.models.material import ModuleMaterial
from core.models.material import Material
from core.models.user import User
from core.models.version import VersionSnapshot
from core.models.fee import OtherFee
from core.models.operation_log import Action, Module as LogModule
from core.auth import get_db, get_current_user_id
from api.quotations import _check_permission
from utils.logger import log_operation

router = APIRouter()


# ============== Pydantic 模型 ==============


class ChangeRequestCreate(BaseModel):
    quotation_id: int
    module_id: int
    change_type: str
    proposed_data: dict
    original_data: Optional[dict] = None


class ReviewRequest(BaseModel):
    remark: str = ""


# ============== 辅助函数 ==============


def check_can_submit_change_request(quotation, user_id):
    """检查用户是否有权限提交变更申请"""
    if quotation.status != "approved":
        return False, "报价单不是已归档状态，无需变更申请"
    return True, ""


# ============== 端点 ==============


@router.get("")
def get_change_requests(
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=200),
    status: Optional[str] = None,
    type: Optional[str] = Query(None, alias="type"),
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """获取变更申请列表"""
    query = db.query(ChangeRequest)

    if status:
        query = query.filter(ChangeRequest.status == status)
    if type:
        query = query.filter(ChangeRequest.change_type == type)

    total = query.count()
    items = (
        query.order_by(ChangeRequest.requested_at.desc())
        .offset((page - 1) * pageSize)
        .limit(pageSize)
        .all()
    )

    return JSONResponse(
        content={
            "items": [cr.to_dict() for cr in items],
            "total": total,
            "page": page,
            "page_size": pageSize,
        }
    )


@router.post("", status_code=201)
def create_change_request(
    body: ChangeRequestCreate,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """创建变更申请"""
    _check_permission(db, int(user_id), 'quotation.edit')
    quotation = db.query(Quotation).get(body.quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="报价单不存在")

    can_submit, msg = check_can_submit_change_request(quotation, user_id)
    if not can_submit:
        raise HTTPException(status_code=400, detail=msg)

    change_request = ChangeRequest(
        quotation_id=body.quotation_id,
        module_id=body.module_id,
        change_type=body.change_type,
        proposed_data=json.dumps(body.proposed_data, ensure_ascii=False),
        original_data=json.dumps(body.original_data, ensure_ascii=False)
        if body.original_data
        else None,
        requested_by=int(user_id),
    )
    db.add(change_request)
    db.commit()

    log_operation(
        action=Action.CREATE,
        module=LogModule.QUOTATION,
        resource_type="change_request",
        resource_id=str(change_request.id),
        detail=f"提交变更申请: {body.change_type}",
        db=db,
        user_id=user_id,
    )

    # 发送消息通知业务员
    if quotation.business_owner_id:
        requester = db.query(User).get(int(user_id))
        module = db.query(Module).get(body.module_id) if body.module_id else None
        from core.services.message_service import MessageService

        MessageService.notify_change_request_submitted(
            business_owner_id=quotation.business_owner_id,
            requester_name=requester.real_name if requester else "未知",
            quotation_name=quotation.name,
            module_name=module.name if module else "",
            change_type=body.change_type,
            change_request_id=change_request.id,
        )

    return JSONResponse(content=change_request.to_dict(), status_code=201)


@router.get("/{request_id}")
def get_change_request_detail(
    request_id: int,
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """获取变更申请详情"""
    change_request = db.query(ChangeRequest).get(request_id)
    if not change_request:
        raise HTTPException(status_code=404, detail="变更申请不存在")
    return JSONResponse(content=change_request.to_dict())


# 兼容 Flask legacy: 前端可能用 POST 调用 approve/reject
# FastAPI 主路由用 PUT（符合 REST 改状态语义），同时 alias POST 不破坏现有调用
@router.post("/{request_id}/approve")
def approve_change_request_post_alias(
    request_id: int,
    body: ReviewRequest = ReviewRequest(),
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """批准变更申请（POST alias，兼容 Flask legacy）"""
    return approve_change_request(
        request_id=request_id, body=body, db=db, user_id=user_id
    )


@router.put("/{request_id}/approve")
def approve_change_request(
    request_id: int,
    body: ReviewRequest = ReviewRequest(),
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """批准变更申请"""
    _check_permission(db, int(user_id), 'quotation.edit')
    change_request = db.query(ChangeRequest).get(request_id)
    if not change_request:
        raise HTTPException(status_code=404, detail="变更申请不存在")

    if change_request.status != "pending":
        raise HTTPException(status_code=400, detail="该申请已被处理")

    quotation = change_request.quotation
    if not quotation:
        raise HTTPException(status_code=404, detail="关联的报价单不存在")

    # 创建版本快照
    snapshot_data = {
        "name": quotation.name,
        "type": quotation.type,
        "scheme_no": quotation.scheme_no,
        "tax_rate": float(quotation.tax_rate) if quotation.tax_rate else 0,
        "business_owner_id": quotation.business_owner_id,
        "modules": [
            {
                "id": mod.id,
                "name": mod.name,
                "code": mod.code,
                "materials": [
                    {
                        "material_id": mm.material_id,
                        "quantity": float(mm.quantity),
                        "selected_by_id": mm.selected_by_id,
                    }
                    for mm in db.query(ModuleMaterial)
                    .filter_by(module_id=mod.id)
                    .all()
                ],
            }
            for mod in quotation.modules
        ],
        "fees": [
            {
                "module_id": f.module_id,
                "fee_type": f.fee_type,
                "location": f.location,
                "amount": float(f.amount) if f.amount else 0,
                "description": f.description,
            }
            for f in db.query(OtherFee)
            .filter_by(quotation_id=quotation.id)
            .all()
        ],
    }

    # 获取真实的最大版本号
    from sqlalchemy import func

    max_version = (
        db.query(func.max(VersionSnapshot.version_no))
        .filter_by(quotation_id=quotation.id)
        .scalar()
        or 0
    )

    version_no = max_version + 1
    version = VersionSnapshot(
        quotation_id=quotation.id,
        version_no=version_no,
        operation_type="change_approve",
        remark=f"变更申请 #{change_request.id} 批准: {body.remark}",
        operator_id=int(user_id),
        snapshot_data=json.dumps(snapshot_data, ensure_ascii=False),
    )
    db.add(version)
    db.flush()

    # 生成版本文件
    from api.exports import generate_version_files

    file_paths = generate_version_files(
        quotation.id, version_no, snapshot_data, snapshot_data
    )
    version.pdf_file = file_paths.get("pdf")
    version.word_file = file_paths.get("word")

    # 应用变更
    proposed = json.loads(change_request.proposed_data)
    original = json.loads(change_request.original_data) if change_request.original_data else {}

    if change_request.change_type == "material_add":
        material = ModuleMaterial(
            module_id=change_request.module_id,
            material_id=proposed["material_id"],
            quantity=proposed["quantity"],
        )
        db.add(material)

    elif change_request.change_type == "material_update":
        module_material = db.query(ModuleMaterial).get(proposed.get("id"))
        if module_material:
            module_material.quantity = proposed["quantity"]

    elif change_request.change_type == "material_delete":
        module_material = db.query(ModuleMaterial).get(original.get("id"))
        if module_material:
            db.delete(module_material)

    # 更新报价单版本号
    quotation.current_version += 1

    # 更新变更申请状态
    change_request.status = "approved"
    change_request.reviewed_by = int(user_id)
    change_request.reviewed_at = datetime.utcnow()
    change_request.review_remark = body.remark

    db.commit()

    log_operation(
        action=Action.APPROVE,
        module=LogModule.QUOTATION,
        resource_type="change_request",
        resource_id=str(change_request.id),
        detail=f"批准变更申请 #{change_request.id}",
        db=db,
        user_id=user_id,
    )

    # 发送消息通知申请人
    if change_request.requested_by:
        module = (
            db.query(Module).get(change_request.module_id)
            if change_request.module_id
            else None
        )
        from core.services.message_service import MessageService

        MessageService.notify_change_request_approved(
            requester_id=change_request.requested_by,
            quotation_name=quotation.name,
            module_name=module.name if module else "",
            change_type=change_request.change_type,
            change_request_id=change_request.id,
        )

    # 发送消息通知业务负责人和成员（版本更新）
    user_ids = [quotation.business_owner_id] if quotation.business_owner_id else []
    for p in quotation.modules:
        for participant in p.participants:
            if participant.user_id not in user_ids:
                user_ids.append(participant.user_id)

    if user_ids:
        MessageService.notify_version_updated(
            user_ids=user_ids,
            quotation_name=quotation.name,
            version_no=quotation.current_version,
            quotation_id=quotation.id,
        )

    return JSONResponse(
        content={
            "message": "变更申请已批准",
            "change_request": change_request.to_dict(),
        }
    )


@router.post("/{request_id}/reject")
def reject_change_request_post_alias(
    request_id: int,
    body: ReviewRequest = ReviewRequest(),
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """拒绝变更申请（POST alias，兼容 Flask legacy）"""
    return reject_change_request(
        request_id=request_id, body=body, db=db, user_id=user_id
    )


@router.put("/{request_id}/reject")
def reject_change_request(
    request_id: int,
    body: ReviewRequest = ReviewRequest(),
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """拒绝变更申请"""
    _check_permission(db, int(user_id), 'quotation.edit')
    change_request = db.query(ChangeRequest).get(request_id)
    if not change_request:
        raise HTTPException(status_code=404, detail="变更申请不存在")

    if change_request.status != "pending":
        raise HTTPException(status_code=400, detail="该申请已被处理")

    quotation = change_request.quotation
    if not quotation:
        raise HTTPException(status_code=404, detail="关联的报价单不存在")

    change_request.status = "rejected"
    change_request.reviewed_by = int(user_id)
    change_request.reviewed_at = datetime.utcnow()
    change_request.review_remark = body.remark

    db.commit()

    log_operation(
        action=Action.REJECT,
        module=LogModule.QUOTATION,
        resource_type="change_request",
        resource_id=str(change_request.id),
        detail=f"拒绝变更申请 #{change_request.id}",
        db=db,
        user_id=user_id,
    )

    # 发送消息通知申请人
    if change_request.requested_by:
        module = (
            db.query(Module).get(change_request.module_id)
            if change_request.module_id
            else None
        )
        from core.services.message_service import MessageService

        MessageService.notify_change_request_rejected(
            requester_id=change_request.requested_by,
            quotation_name=quotation.name,
            module_name=module.name if module else "",
            change_type=change_request.change_type,
            change_request_id=change_request.id,
            reason=body.remark,
        )

    return JSONResponse(
        content={
            "message": "变更申请已拒绝",
            "change_request": change_request.to_dict(),
        }
    )
