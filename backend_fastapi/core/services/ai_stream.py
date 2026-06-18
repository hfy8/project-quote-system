"""AI Agent 流式版本 - generator 化

设计：
- 每执行一步（call_llm / execute_tool）就 yield 一个 SSE 事件
- 前端用 EventSource 接收
- 事件类型：start / tool_call / tool_result / token / done / error
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
import re
from typing import List, Dict, Iterator

from utils.llm_client import ask_llm_stream
from core.services.ai_tools import TOOLS, execute_tool


def _recover_tool_args(tool_name: str, tool_args: dict) -> dict:
    """从 LLM 异常输出中恢复工具参数

    某些 LLM（如 MiniMax-Text-01）会把多个工具调用的参数 JSON 拼起来，
    包在一个 _raw 字段里，例如：
        {"_raw": "{\"quotation_id\": 68}{\"quotation_id\": 69}..."}
    或：
        {"_raw": "{}{\"material_cost\": 8000, \"labor_hours\": 100}"}

    这种情况需要从中提取第一个合法 JSON 对象作为参数。
    """
    if "_raw" not in tool_args:
        return tool_args

    raw_str = tool_args["_raw"]
    if not isinstance(raw_str, str):
        return tool_args

    # 用正则找所有 {...} 块
    candidates = re.findall(r'\{[^{}]*\}', raw_str)

    # 倒序遍历：通常第一个块是正确答案，但有时第一个是空 {}，第二个才是
    # 这里取最后一个非空块（如果第一个块是 {}，更可能是"prefix noise"）
    valid = []
    for c in candidates:
        try:
            parsed = json.loads(c)
            if parsed:  # 非空 dict
                valid.append(parsed)
        except json.JSONDecodeError:
            continue

    if not valid:
        return tool_args  # 解析失败，保留原样（让工具自己报错）

    # 取最后一个非空 JSON 块（一般是 LLM 真正想用的参数）
    recovered = valid[-1]
    print(f"🔧 [_recover_tool_args] {tool_name}: 从 _raw 恢复参数 {recovered}")
    return recovered


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
1. 调工具后，如果工具结果已经足够回答用户问题 → **直接输出最终答案**
2. 工具结果不够明确时，可以再调一次补充信息
"""}
    ]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_query})

    steps = 0
    max_steps = max_steps  # 从参数传入，默认 20
    tools_used = []
    final_answer = ""
    # 防失控：连续 10 次调同一工具（相同参数）才强制退出
    REPEAT_LIMIT = 10  # 阈值：连续重复调用次数
    recent_calls = []  # [(tool_name, json_args), ...]  最近 N 步

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
                    # 提前恢复异常参数（如 _raw 拼接），保证前端和后续执行看到的是干净的 args
                    tool_args = _recover_tool_args(tool_name, tool_args)
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
                        # 参数已在 tool_call 阶段恢复过，这里直接用
                        # 防失控：检测连续重复调用
                        args_json = json.dumps(tool_args, sort_keys=True, ensure_ascii=False)
                        call_sig = (tool_name, args_json)
                        recent_calls.append(call_sig)
                        # 只保留最近 REPEAT_LIMIT 步
                        if len(recent_calls) > REPEAT_LIMIT:
                            recent_calls = recent_calls[-REPEAT_LIMIT:]

                        # 检测：连续 REPEAT_LIMIT 步调同一个工具（参数相同）→ 强制退出
                        if len(recent_calls) >= REPEAT_LIMIT and len(set(recent_calls[-REPEAT_LIMIT:])) == 1:
                            logger_msg = f"检测到连续 {REPEAT_LIMIT} 次重复调用 {tool_name}，强制退出"
                            yield {"type": "warning", "message": logger_msg}
                            # 不传 answer，让前端保留累积的 fullAnswer（流式 token 累加的）
                            yield {
                                "type": "done",
                                "answer": final_answer,  # 通常是空字符串，不覆盖前端累积的 token
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
                        # 去除 LLM 输出开头/结尾的多余空白（避免前端显示首行空白）
                        final_answer = "".join(content_parts).strip()
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
