"""FastAPI 路由 - Module Participants (迁移版)

业务逻辑 1:1 复刻 backend/app/routes/module_participants.py

注意路径映射 (Flask module_participant_bp url_prefix='/api/modules'):
- GET    /api/modules/<module_id>/participants
- POST   /api/modules/<module_id>/participants
- DELETE /api/modules/<module_id>/participants/<participant_id>

FastAPI 用 router prefix='/api/modules'，因此路由装饰器只写相对路径。
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from core.auth import get_db, get_current_user_id
from api.quotations import _check_permission
from utils.log_helpers import record_crud

router = APIRouter(prefix='/api/modules')


def _resolve_participant_label(user_id: int, db: Session) -> str:
    """解析模块参与人显示标签: user_name + 类型 (机构/电气/项目).

    模块参与人本身的 participant_type 字段不存储在 ModuleParticipant 表上,
    需要从 QuotationParticipant 表里取该用户在该报价单中的参与类型。
    """
    try:
        from core.models.user import User
        from core.models.quotation import QuotationParticipant

        user = db.query(User).get(user_id)
        user_name = user.real_name if user else f'用户#{user_id}'

        # 取最新一条 QuotationParticipant 记录作为类型来源
        qp = (
            db.query(QuotationParticipant)
            .filter(QuotationParticipant.user_id == user_id)
            .order_by(QuotationParticipant.id.desc())
            .first()
        )
        type_label_map = {
            'project': '项目',
            'agency': '机构',
            'electrical': '电气',
        }
        ptype = qp.participant_type if qp else None
        type_zh = type_label_map.get(ptype, ptype or '其他')
        return f'{user_name} ({type_zh})'
    except Exception:
        return f'用户#{user_id} (其他)'


# ============== Pydantic 模型 ==============

class ParticipantAddRequest(BaseModel):
    """添加参与者请求"""
    user_ids: List[int]


# ============== 端点 ==============

@router.get("/{module_id}/participants", summary="获取模块参与者")
def get_module_participants(
    module_id: int,
    db=Depends(get_db),
):
    """获取模块参与人员"""
    from core.models.module import ModuleParticipant

    participants = db.query(ModuleParticipant).filter_by(module_id=module_id).all()
    return JSONResponse(content={"participants": [p.to_dict() for p in participants]})


@router.post("/{module_id}/participants", summary="添加参与者", status_code=201)
def add_module_participants(
    module_id: int,
    body: ParticipantAddRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """添加模块参与人员（1:1 复刻 Flask 逻辑，含消息通知）"""
    _check_permission(db, int(user_id), 'module.edit')
    from core.models.module import ModuleParticipant, Module
    from core.services.message_service import MessageService

    user_ids = body.user_ids
    if not user_ids:
        return JSONResponse(status_code=400, content={"error": "请选择人员"})

    # 获取模块和报价单信息用于发消息
    module = db.query(Module).get(module_id)
    quotation = module.quotation if module else None

    added = []
    for uid in user_ids:
        # 检查是否已存在
        existing = db.query(ModuleParticipant).filter_by(
            module_id=module_id, user_id=uid
        ).first()
        if existing:
            continue
        p = ModuleParticipant(module_id=module_id, user_id=uid)
        db.add(p)
        added.append(uid)

        # 发送消息通知被添加的成员
        if module and quotation:
            MessageService.notify_module_member_added(
                user_id=uid,
                quotation_name=quotation.name,
                module_name=module.name,
                quotation_id=quotation.id
            )

    db.commit()

    # 操作日志: 每个成功添加的人员记录一条
    for uid in added:
        record_crud(
            user_id,
            'quotation',
            'create',
            f'添加 模块参与人 {_resolve_participant_label(uid, db)}',
            resource_type='module_participant',
            resource_id=str(uid),
        )

    return JSONResponse(content={
        "message": f"已添加 {len(added)} 名人员",
        "added": added,
    })


@router.delete("/{module_id}/participants/{participant_id}", summary="移除参与者")
def remove_module_participant(
    module_id: int,
    participant_id: int,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """移除模块参与人员"""
    _check_permission(db, int(user_id), 'module.edit')
    from core.models.module import ModuleParticipant

    p = db.query(ModuleParticipant).filter_by(
        id=participant_id, module_id=module_id
    ).first()
    if not p:
        raise HTTPException(status_code=404, detail="人员不存在")

    db.delete(p)
    db.commit()

    record_crud(
        user_id,
        'quotation',
        'delete',
        f'移除 模块参与人 {_resolve_participant_label(p.user_id, db)}',
        resource_type='module_participant',
        resource_id=str(p.id),
    )

    return JSONResponse(content={"message": "已移除"})
