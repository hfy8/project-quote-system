"""第 5 课：AI Agent FastAPI 路由

提供端点：
- POST /api/ai/ask        非流式（兼容旧版本）
- POST /api/ai/ask/stream 流式输出（SSE）
- GET  /api/ai/health     健康检查
"""
import sys
import os
import json
import time
import uuid

# 让相对导入能找到 utils/ core/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, List, Dict
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from core.auth import get_current_user_id
from core.services.ai_agent import run_agent

import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai", tags=["AI 智能"])


# ============== 多轮对话：内存会话存储 ==============
# 简单 dict：{conversation_id: [{"role": "user/assistant", "content": "..."}]}
# 生产环境应该用 Redis，但 v17 阶段先用内存
_CONVERSATIONS: Dict[str, List[Dict]] = {}
_MAX_HISTORY = 10  # 最多保留 10 轮


def _get_history(conversation_id: str) -> List[Dict]:
    """获取会话历史"""
    return _CONVERSATIONS.get(conversation_id, [])


def _save_history(conversation_id: str, user_msg: str, assistant_msg: str):
    """追加一条对话到历史（保留最近 N 轮）"""
    if conversation_id not in _CONVERSATIONS:
        _CONVERSATIONS[conversation_id] = []
    _CONVERSATIONS[conversation_id].append({"role": "user", "content": user_msg})
    _CONVERSATIONS[conversation_id].append({"role": "assistant", "content": assistant_msg})
    # 截断
    max_msgs = _MAX_HISTORY * 2
    if len(_CONVERSATIONS[conversation_id]) > max_msgs:
        _CONVERSATIONS[conversation_id] = _CONVERSATIONS[conversation_id][-max_msgs:]


# ============== 请求 / 响应 schema ==============
class AskRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="用户问题")
    max_steps: int = Field(10, ge=1, le=30, description="Agent 最大步数（防失控）")
    conversation_id: Optional[str] = Field(None, description="会话 ID（多轮对话用，不传则新建）")


class AskResponse(BaseModel):
    answer: str
    success: bool
    error: Optional[str] = None
    steps: int = 0
    tools_used: list = []
    conversation_id: str = ""


# ============== 路由 ==============
@router.post("/ask", response_model=AskResponse)
def ask(
    req: AskRequest,
    user_id: str = Depends(get_current_user_id),
):
    """AI 智能问答 - 非流式版本（兼容旧客户端）"""
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="query 不能为空")

    conv_id = req.conversation_id or str(uuid.uuid4())
    logger.info(f"AI ask from user {user_id} (conv={conv_id[:8]}): {req.query[:50]}...")

    try:
        from core.services.ai_agent import build_agent

        history = _get_history(conv_id)
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

        # 保存到历史
        _save_history(conv_id, req.query, answer)

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
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="query 不能为空")

    conv_id = req.conversation_id or str(uuid.uuid4())
    logger.info(f"AI stream from user {user_id} (conv={conv_id[:8]}): {req.query[:50]}...")

    def event_generator():
        from core.services.ai_stream import run_agent_stream
        history = _get_history(conv_id)
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
                _save_history(conv_id, req.query, last_answer)

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


@router.delete("/conversation/{conversation_id}")
def clear_conversation(
    conversation_id: str,
    user_id: str = Depends(get_current_user_id),
):
    """清除指定会话的历史"""
    if conversation_id in _CONVERSATIONS:
        del _CONVERSATIONS[conversation_id]
        return {"status": "ok", "message": f"已清除会话 {conversation_id[:8]}"}
    return {"status": "ok", "message": "会话不存在"}


@router.get("/health")
def health():
    """健康检查 - 不需要登录"""
    return {"status": "ok", "service": "ai-agent", "active_conversations": len(_CONVERSATIONS)}
