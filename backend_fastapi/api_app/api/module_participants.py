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

from api_app.main import get_db, get_current_user_id

router = APIRouter(prefix='/api/modules')


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
    from app.models.module import ModuleParticipant

    participants = db.query(ModuleParticipant).filter_by(module_id=module_id).all()
    return JSONResponse(content={"participants": [p.to_dict() for p in participants]})


@router.post("/{module_id}/participants", summary="添加参与者", status_code=201)
def add_module_participants(
    module_id: int,
    body: ParticipantAddRequest,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    """添加模块参与人员（1:1 复刻 Flask 逻辑，含消息通知）"""
    from app.models.module import ModuleParticipant, Module
    from app.services.message_service import MessageService

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
    return JSONResponse(content={
        "message": f"已添加 {len(added)} 名人员",
        "added": added,
    })


@router.delete("/{module_id}/participants/{participant_id}", summary="移除参与者")
def remove_module_participant(
    module_id: int,
    participant_id: int,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    """移除模块参与人员"""
    from app.models.module import ModuleParticipant

    p = db.query(ModuleParticipant).filter_by(
        id=participant_id, module_id=module_id
    ).first()
    if not p:
        raise HTTPException(status_code=404, detail="人员不存在")

    db.delete(p)
    db.commit()
    return JSONResponse(content={"message": "已移除"})
