"""FastAPI 路由 - 消息 (迁移版)"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from core.models.message import Message
from core.auth import get_db, get_current_user_id
from datetime import datetime

router = APIRouter(prefix="/api/messages")


class ReadMessagesRequest(BaseModel):
    message_ids: list[int]


@router.get("")
def get_messages(
    page: int = Query(1, ge=1),
    pageSize: int = Query(20, ge=1, le=100),
    is_read: Optional[str] = Query(None, alias="is_read"),
    db=Depends(get_db),
    user_id=Depends(get_current_user_id),
):
    """获取当前用户的消息列表"""
    query = db.query(Message).filter_by(recipient_id=int(user_id)).order_by(Message.created_at.desc())

    if is_read is not None:
        query = query.filter_by(is_read=is_read.lower() == "true")

    total = query.count()
    items = query.offset((page - 1) * pageSize).limit(pageSize).all()

    return JSONResponse(
        content={
            "items": [m.to_dict() for m in items],
            "total": total,
            "page": page,
            "pageSize": pageSize,
        }
    )


@router.get("/unread-count")
def get_unread_count(
    db=Depends(get_db),
    user_id=Depends(get_current_user_id),
):
    """获取未读消息数量"""
    count = (
        db.query(Message)
        .filter_by(recipient_id=int(user_id), is_read=False)
        .count()
    )
    return JSONResponse(content={"count": count})


@router.post("/read")
def mark_messages_read(
    body: ReadMessagesRequest,
    db=Depends(get_db),
    user_id=Depends(get_current_user_id),
):
    """批量标记消息为已读"""
    now = datetime.utcnow()
    updated = (
        db.query(Message)
        .filter(
            Message.id.in_(body.message_ids),
            Message.recipient_id == int(user_id),
        )
        .update({"is_read": True, "updated_at": now}, synchronize_session=False)
    )
    db.commit()
    return JSONResponse(content={"success": True, "updated": updated})


@router.put("/read-all")
def mark_all_as_read_put_alias(
    db=Depends(get_db),
    user_id=Depends(get_current_user_id),
):
    """标记所有消息为已读（PUT alias，兼容 Flask legacy）"""
    return mark_all_as_read(db=db, user_id=user_id)


@router.post("/read-all")
def mark_all_as_read(
    db=Depends(get_db),
    user_id=Depends(get_current_user_id),
):
    """标记所有消息为已读"""
    now = datetime.utcnow()
    db.query(Message).filter_by(
        recipient_id=int(user_id), is_read=False
    ).update(
        {"is_read": True, "updated_at": now}, synchronize_session=False
    )
    db.commit()
    return JSONResponse(content={"success": True})
