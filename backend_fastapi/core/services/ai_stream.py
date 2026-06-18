"""AI Agent 流式版本 - generator 化

设计：
- 每执行一步（call_llm / execute_tool）就 yield 一个 SSE 事件
- 前端用 EventSource 接收
- 事件类型：start / tool_call / tool_result / token / done / error
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
from typing import List, Dict, Iterator

from utils.llm_client import ask_llm_stream
from core.services.ai_tools import TOOLS, execute_tool


def run_agent_stream(user_query: str, history: List[Dict] = None, user_id: int = None, max_steps: int = 20) -> Iterator[Dict]:
    """流式跑 Agent - 每步 yield 事件

    Args:
        user_query: 当前用户问题
        history: 历史消息（多轮对话用），格式：[{"role": "user/assistant", "content": "..."}]

    Yields:
        {"type": "start", "query": "..."}
        {"type": "tool_call", "name": "...", "arguments": {...}}
        {"type": "tool_result", "name": "...", "result": "..."}
        {"type": "token", "content": "..."}     # 流式内容（多次）
        {"type": "done", "answer": "...", "steps": N, "tools_used": [...]}
        {"type": "error", "message": "..."}
    """
    yield {"type": "start", "query": user_query}

    # 构造消息（合并历史）
    messages = [
        {"role": "system", "content": """你是项目报价系统的 AI 助手。善用工具查真实数据，回答必须用中文，简洁清晰。

**重要规则**：
1. 调工具后，如果工具结果已经足够回答用户问题 → **必须直接输出最终答案**，不要再调工具
2. 不要重复调同一个工具（除非参数不同）
3. 工具结果不够明确时，可以再调一次补充信息
4. 最多调用 2-3 个工具就必须出答案
"""}
    ]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_query})

    steps = 0
    max_steps = max_steps  # 从参数传入，默认 20
    tools_used = []
    final_answer = ""
    # 防失控：记录最近 N 步的 (tool_name, tool_args) 用于检测重复
    recent_calls = []  # [(tool_name, json_args), ...]  最近 3 步
    last_warning_step = 0  # 上次警告 step，避免每步都警告

    try:
        while steps < max_steps:
            steps += 1
            tool_name = None
            tool_args = {}
            content_parts = []

            # 1. 流式调 LLM
            for event in ask_llm_stream(messages, temperature=0, tools=TOOLS):
                etype = event.get("type")

                if etype == "token":
                    # 边生成边发给前端
                    yield {"type": "token", "content": event["content"]}
                    content_parts.append(event["content"])

                elif etype == "tool_call":
                    tool_name = event["name"]
                    tool_args = event["arguments"]
                    yield {
                        "type": "tool_call",
                        "name": tool_name,
                        "arguments": tool_args,
                    }

                elif etype == "error":
                    yield {"type": "error", "message": event.get("message", "LLM 错误")}
                    return

                elif etype == "done":
                    # 这一轮 LLM 完成
                    if tool_name:
                        # 防失控：检测重复调用
                        args_json = json.dumps(tool_args, sort_keys=True, ensure_ascii=False)
                        call_sig = (tool_name, args_json)
                        recent_calls.append(call_sig)
                        # 只保留最近 3 步
                        if len(recent_calls) > 3:
                            recent_calls = recent_calls[-3:]

                        # 检测：连续 3 步调同一个工具（参数相同）→ 强制退出
                        if len(recent_calls) >= 3 and len(set(recent_calls[-3:])) == 1:
                            # 同样的 (tool_name, args) 已经连续调了 3 次
                            logger_msg = f"检测到重复调用 {tool_name}({args_json}) 3 次，强制退出"
                            yield {
                                "type": "warning",
                                "message": logger_msg,
                            }
                            yield {
                                "type": "done",
                                "answer": final_answer or f"AI 重复调用工具 {tool_name} 超过 3 次，已自动停止。请换个问法或提供更多上下文。",
                                "steps": steps,
                                "tools_used": tools_used,
                            }
                            return

                        # 2. 执行工具
                        yield {"type": "tool_executing", "name": tool_name}
                        try:
                            result = execute_tool(tool_name, tool_args, user_id=user_id)
                        except Exception as e:
                            result = json.dumps({"error": str(e)}, ensure_ascii=False)

                        tools_used.append(tool_name)
                        yield {
                            "type": "tool_result",
                            "name": tool_name,
                            "result": result[:500],  # 截断
                        }

                        # 把工具结果回喂给 LLM（assistant 消息 + tool 消息）
                        messages.append({
                            "role": "assistant",
                            "content": "",
                            "tool_calls": [{"id": event.get("id", f"call_{steps}"),
                                            "type": "function",
                                            "function": {"name": tool_name, "arguments": args_json}}]
                        })
                        messages.append({
                            "role": "tool",
                            "tool_call_id": event.get("id", f"call_{steps}"),
                            "content": result,
                        })
                    else:
                        # LLM 直接给答案 - 收尾
                        final_answer = "".join(content_parts)
                        messages.append({"role": "assistant", "content": final_answer})
                        yield {
                            "type": "done",
                            "answer": final_answer,
                            "steps": steps,
                            "tools_used": tools_used,
                        }
                        return

        # 超过最大步数
        yield {
            "type": "done",
            "answer": final_answer or "达到最大步数限制",
            "steps": steps,
            "tools_used": tools_used,
        }

    except Exception as e:
        yield {"type": "error", "message": str(e)}


if __name__ == "__main__":
    print("🚀 流式 Agent 测试\n")
    for event in run_agent_stream("物料库有哪些酒精棉片？"):
        print(f"  事件: {event}")
