"""第 5 课：AI Agent FastAPI 路由

提供 /api/ai/ask 端点，前端可以问业务问题，AI 自动查数据库回答。
"""
import sys
import os

# 让相对导入能找到 utils/ core/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from core.auth import get_current_user_id
from core.services.ai_agent import run_agent

import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ai", tags=["AI 智能"])


# ============== 请求 / 响应 schema ==============
class AskRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="用户问题")
    max_steps: int = Field(5, ge=1, le=10, description="Agent 最大步数（防失控）")


class AskResponse(BaseModel):
    answer: str
    success: bool
    error: Optional[str] = None
    steps: int = 0                # 实际用了多少步
    tools_used: list = []         # 调了哪些工具


# ============== 路由 ==============
@router.post("/ask", response_model=AskResponse)
def ask(
    req: AskRequest,
    user_id: str = Depends(get_current_user_id),
):
    """AI 智能问答 - 自动调用 LangGraph Agent 查数据库

    需要登录（复用现有 JWT 鉴权）。

    Body:
        {
            "query": "物料库里有哪些酒精棉片？",
            "max_steps": 5
        }

    Returns:
        {
            "answer": "物料库中有以下酒精棉片：...",
            "success": true,
            "error": null,
            "steps": 2,
            "tools_used": ["search_materials"]
        }
    """
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="query 不能为空")

    logger.info(f"AI ask from user {user_id}: {req.query[:50]}...")

    try:
        # 跑 LangGraph Agent
        # （返回答案字符串 + 工具调用列表 + 步数）
        from core.services.ai_agent import build_agent

        initial_state = {
            "user_query": req.query,
            "messages": [
                {"role": "system", "content": "你是报价员助手，善用工具查真实数据。回答简洁有条理。"},
                {"role": "user", "content": req.query}
            ],
            "intent": "",
            "tool_name": "",
            "tool_args": {},
            "tool_result": "",
            "final_answer": "",
            "step_count": 0,
        }

        agent = build_agent()
        final_state = agent.invoke(initial_state)

        # 收集统计
        steps = final_state.get("step_count", 0)
        tools_used = []
        for msg in final_state.get("messages", []):
            if msg.get("role") == "assistant" and msg.get("tool_calls"):
                for tc in msg["tool_calls"]:
                    tools_used.append(tc["function"]["name"])

        # 找最后一条 assistant 的 content
        answer = ""
        for msg in reversed(final_state.get("messages", [])):
            if msg.get("role") == "assistant" and msg.get("content"):
                if not msg.get("tool_calls"):
                    answer = msg["content"]
                    break

        if not answer:
            answer = final_state.get("final_answer", "")

        return AskResponse(
            answer=answer,
            success=True,
            steps=steps,
            tools_used=list(set(tools_used)),  # 去重
        )

    except Exception as e:
        logger.exception("AI ask failed")
        return AskResponse(
            answer="",
            success=False,
            error=str(e),
        )


@router.get("/health")
def health():
    """健康检查 - 不需要登录"""
    return {"status": "ok", "service": "ai-agent"}
