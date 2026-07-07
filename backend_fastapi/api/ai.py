"""第 5 课：AI Agent FastAPI 路由

提供端点：
- POST /api/ai/ask        非流式（兼容旧版本）
- POST /api/ai/ask/stream 流式输出（SSE）
- GET  /api/ai/health     健康检查
- GET  /api/ai/conversations          列表用户会话
- POST /api/ai/conversations          创建新会话
- PUT  /api/ai/conversations/{id}     更新标题
- DELETE /api/ai/conversations/{id}   删除会话+消息
- GET  /api/ai/conversations/{id}/messages  列出消息
- DELETE /api/ai/conversations/{id}/messages 清空消息
"""
import sys
import os
import json
import time
import uuid

# 让相对导入能找到 utils/ core/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from datetime import datetime

from core.auth import get_current_user_id, get_db
from core.services.ai_agent import run_agent
from api.quotations import _check_permission
from core.models.ai_conversation import AiConversation, AiMessage

import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai", tags=["AI 智能"])


# ============== 多轮对话：内存会话存储（兼容旧逻辑，DB 为主） ==============
# 生产环境应该用 Redis，但当前阶段先用内存 + DB 双写
_CONVERSATIONS: Dict[str, List[Dict]] = {}
_MAX_HISTORY = 10  # 最多保留 10 轮


def _get_history(conversation_id: str, db: Optional[Session] = None) -> List[Dict]:
    """获取会话历史 - 优先从 DB 读取，fallback 到内存"""
    # 尝试从 DB 读取
    if db is not None:
        try:
            messages = (
                db.query(AiMessage)
                .filter(AiMessage.conversation_id == conversation_id)
                .order_by(AiMessage.created_at)
                .all()
            )
            if messages:
                return [
                    {"role": m.role, "content": m.content}
                    for m in messages
                ]
        except Exception:
            pass
    # fallback 到内存
    return _CONVERSATIONS.get(conversation_id, [])


def _save_history(
    conversation_id: str,
    user_msg: str,
    assistant_msg: str,
    db: Optional[Session] = None,
    assistant_tool_calls: Optional[str] = None,
):
    """追加一条对话到历史（保留最近 N 轮）- 写入 DB 和内存"""
    # 对内存
    if conversation_id not in _CONVERSATIONS:
        _CONVERSATIONS[conversation_id] = []
    _CONVERSATIONS[conversation_id].append({"role": "user", "content": user_msg})
    _CONVERSATIONS[conversation_id].append({"role": "assistant", "content": assistant_msg})
    # 截断
    max_msgs = _MAX_HISTORY * 2
    if len(_CONVERSATIONS[conversation_id]) > max_msgs:
        _CONVERSATIONS[conversation_id] = _CONVERSATIONS[conversation_id][-max_msgs:]

    # 写入 DB
    if db is not None:
        try:
            now = datetime.utcnow()
            # 更新会话 updated_at
            conv = db.query(AiConversation).filter(
                AiConversation.id == conversation_id
            ).first()
            if conv:
                if conv.created_at is None or (now - conv.created_at).seconds < 30:
                    # 第一次消息后自动生成标题
                    if conv.title == '新对话' or not conv.title:
                        conv.title = user_msg[:60] + ('...' if len(user_msg) > 60 else '')
                conv.updated_at = now

            # 创建用户消息
            user_message = AiMessage(
                conversation_id=conversation_id,
                role='user',
                content=user_msg,
                created_at=now,
            )
            db.add(user_message)

            # 创建助手消息
            assistant_message = AiMessage(
                conversation_id=conversation_id,
                role='assistant',
                content=assistant_msg,
                tool_calls=assistant_tool_calls,
                created_at=now,
            )
            db.add(assistant_message)
            db.commit()
        except Exception as e:
            logger.warning(f"Failed to save history to DB: {e}")
            db.rollback()


# ============== 请求 / 响应 schema ==============
class AskRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="用户问题")
    max_steps: int = Field(20, ge=1, le=40, description="Agent 最大步数（防失控）")
    conversation_id: Optional[str] = Field(None, description="会话 ID（多轮对话用，不传则新建）")


class AskResponse(BaseModel):
    answer: str
    success: bool
    error: Optional[str] = None
    steps: int = 0
    tools_used: list = []
    conversation_id: str = ""


# ============== Conversation schemas ==============
class CreateConversationRequest(BaseModel):
    title: Optional[str] = Field(None, max_length=200, description="对话标题，不传则自动生成")


class UpdateConversationRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="对话标题")


# ============== 路由 ==============
@router.post("/ask", response_model=AskResponse)
def ask(
    req: AskRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """AI 智能问答 - 非流式版本（兼容旧客户端）"""
    _check_permission(db, int(user_id), 'ai.query')
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="query 不能为空")

    conv_id = req.conversation_id or str(uuid.uuid4())
    logger.info(f"AI ask from user {user_id} (conv={conv_id[:8]}): {req.query[:50]}...")

    try:
        from core.services.ai_agent import build_agent

        history = _get_history(conv_id, db=db)
        messages = [
            {"role": "system", "content": "你是项目报价系统的 AI 助手。善用工具查真实数据，回答简洁有条理。"},
        ] + history + [
            {"role": "user", "content": req.query}
        ]

        initial_state = {
            "user_query": req.query,
            "messages": messages,
            "intent": "",
            "tool_name": "",
            "tool_args": {},
            "tool_result": "",
            "final_answer": "",
            "step_count": 0,
        }

        agent = build_agent()
        final_state = agent.invoke(initial_state)

        steps = final_state.get("step_count", 0)
        tools_used = []
        for msg in final_state.get("messages", []):
            if msg.get("role") == "assistant" and msg.get("tool_calls"):
                for tc in msg["tool_calls"]:
                    tools_used.append(tc["function"]["name"])

        answer = ""
        for msg in reversed(final_state.get("messages", [])):
            if msg.get("role") == "assistant" and msg.get("content"):
                if not msg.get("tool_calls"):
                    answer = msg["content"]
                    break

        if not answer:
            answer = final_state.get("final_answer", "")

        # 保存到历史（DB + 内存）
        _save_history(conv_id, req.query, answer, db=db)

        return AskResponse(
            answer=answer,
            success=True,
            steps=steps,
            tools_used=list(set(tools_used)),
            conversation_id=conv_id,
        )

    except Exception as e:
        logger.exception("AI ask failed")
        return AskResponse(
            answer="",
            success=False,
            error=str(e),
            conversation_id=conv_id,
        )


@router.post("/ask/stream")
def ask_stream(
    req: AskRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """AI 智能问答 - SSE 流式输出

    Body:
        {"query": "...", "conversation_id": "..."}

    SSE Events:
        data: {"type": "start", "query": "..."}
        data: {"type": "tool_call", "name": "...", "arguments": {...}}
        data: {"type": "tool_result", "name": "...", "result": "..."}
        data: {"type": "token", "content": "..."}    (流式内容)
        data: {"type": "done", "answer": "...", "steps": N, "tools_used": [...]}
        data: {"type": "error", "message": "..."}
    """
    _check_permission(db, int(user_id), 'ai.query')
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="query 不能为空")

    conv_id = req.conversation_id or str(uuid.uuid4())
    logger.info(f"AI stream from user {user_id} (conv={conv_id[:8]}): {req.query[:50]}...")

    def event_generator():
        from core.services.ai_stream import run_agent_stream
        history = _get_history(conv_id, db=db)
        start_time = time.time()
        last_answer = ""
        try:
            for event in run_agent_stream(req.query, history=history, user_id=int(user_id), max_steps=req.max_steps):
                # 让前端拿到 conversation_id
                if event.get("type") in ("start",):
                    event["conversation_id"] = conv_id
                elif event.get("type") == "done":
                    event["conversation_id"] = conv_id
                    last_answer = event.get("answer", "")
                yield f"data: {json.dumps(event, ensure_ascii=False)}\n\n"

            # 流结束后保存真实回答到历史
            if last_answer:
                _save_history(conv_id, req.query, last_answer, db=db)

        except Exception as e:
            logger.exception("AI stream failed")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # 禁用 nginx 缓冲
            "Connection": "keep-alive",
        },
    )


# ============== Conversation CRUD ==============

@router.get("/conversations")
def list_conversations(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """列出当前用户的所有对话（按 updated_at 倒序）"""
    _check_permission(db, int(user_id), 'ai.query')
    conversations = (
        db.query(AiConversation)
        .filter(AiConversation.user_id == int(user_id))
        .order_by(AiConversation.updated_at.desc().nullslast(), AiConversation.created_at.desc())
        .all()
    )
    return {
        "conversations": [c.to_dict() for c in conversations],
        "total": len(conversations),
    }


@router.post("/conversations")
def create_conversation(
    req: Optional[CreateConversationRequest] = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """创建新对话"""
    _check_permission(db, int(user_id), 'ai.query')
    conv_id = str(uuid.uuid4())
    now = datetime.utcnow()
    title = "新对话"
    if req and req.title:
        title = req.title

    conversation = AiConversation(
        id=conv_id,
        user_id=int(user_id),
        title=title,
        created_at=now,
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    logger.info(f"Created conversation {conv_id[:8]} for user {user_id}")
    return {
        "conversation": conversation.to_dict(),
        "message": "对话创建成功",
    }


@router.put("/conversations/{conversation_id}")
def update_conversation(
    conversation_id: str,
    req: UpdateConversationRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """更新对话标题"""
    _check_permission(db, int(user_id), 'ai.query')
    conversation = db.query(AiConversation).filter(
        AiConversation.id == conversation_id,
        AiConversation.user_id == int(user_id),
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="对话不存在")

    conversation.title = req.title
    conversation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(conversation)

    return {
        "conversation": conversation.to_dict(),
        "message": "标题已更新",
    }


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """删除对话及其所有消息"""
    _check_permission(db, int(user_id), 'ai.query')
    conversation = db.query(AiConversation).filter(
        AiConversation.id == conversation_id,
        AiConversation.user_id == int(user_id),
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="对话不存在")

    # 级联删除消息
    db.query(AiMessage).filter(
        AiMessage.conversation_id == conversation_id,
    ).delete()
    db.delete(conversation)
    # 也清理内存
    _CONVERSATIONS.pop(conversation_id, None)
    db.commit()

    return {"status": "ok", "message": f"已删除对话 {conversation_id[:8]}"}


@router.get("/conversations/{conversation_id}/messages")
def list_messages(
    conversation_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """列出指定对话的消息列表"""
    _check_permission(db, int(user_id), 'ai.query')
    conversation = db.query(AiConversation).filter(
        AiConversation.id == conversation_id,
        AiConversation.user_id == int(user_id),
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="对话不存在")

    messages = (
        db.query(AiMessage)
        .filter(AiMessage.conversation_id == conversation_id)
        .order_by(AiMessage.created_at)
        .all()
    )

    return {
        "messages": [m.to_dict() for m in messages],
        "total": len(messages),
    }


@router.delete("/conversations/{conversation_id}/messages")
def clear_messages(
    conversation_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """清空对话的所有消息，但保留对话本身"""
    _check_permission(db, int(user_id), 'ai.query')
    conversation = db.query(AiConversation).filter(
        AiConversation.id == conversation_id,
        AiConversation.user_id == int(user_id),
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="对话不存在")

    count = db.query(AiMessage).filter(
        AiMessage.conversation_id == conversation_id,
    ).delete()
    # 清理内存
    _CONVERSATIONS.pop(conversation_id, None)
    conversation.updated_at = datetime.utcnow()
    db.commit()

    return {
        "status": "ok",
        "message": f"已清除 {count} 条消息（对话保留）",
    }


# ============== 兼容旧端点 ==============

# 保留旧版本的 clear endpoint（用单数 conversation）
@router.delete("/conversation/{conversation_id}")
def clear_conversation_legacy(
    conversation_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """清除指定会话的历史（兼容旧版本）"""
    _check_permission(db, int(user_id), 'ai.query')
    # 尝试 DB 方式删除
    conv = db.query(AiConversation).filter(
        AiConversation.id == conversation_id,
        AiConversation.user_id == int(user_id),
    ).first()
    if conv:
        db.query(AiMessage).filter(AiMessage.conversation_id == conversation_id).delete()
        db.delete(conv)
        db.commit()
    # 也清理内存
    if conversation_id in _CONVERSATIONS:
        del _CONVERSATIONS[conversation_id]
        return {"status": "ok", "message": f"已清除会话 {conversation_id[:8]}"}
    return {"status": "ok", "message": "会话不存在"}


@router.get("/health")
def health(db: Session = Depends(get_db)):
    """健康检查 - 不需要登录"""
    conv_count = 0
    try:
        conv_count = db.query(AiConversation).count()
    except Exception:
        pass
    return {
        "status": "ok",
        "service": "ai-agent",
        "active_conversations": len(_CONVERSATIONS),
        "db_conversations": conv_count,
    }
