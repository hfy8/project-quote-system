import os                          # 读环境变量
import logging                      # 打印日志
import json
from typing import List, Dict, Iterator       # 类型注解，让代码更清晰
import requests                     # 发 HTTP 请求（最流行）
from dotenv import load_dotenv
load_dotenv()

LLM_API_KEY = os.getenv("MINIMAX_API_KEY") or os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.minimax.chat/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "MiniMax-M2.7")
logger = logging.getLogger(__name__)



def ask_llm(messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
    """问 LLM 一个问题，返回它的回答

    Args:
        messages: OpenAI 协议消息列表
                  格式：[{"role": "user", "content": "..."}]
        temperature: 0=死板/确定，1=发散/有创造性

    Returns:
        LLM 的回复文本
    """
    if not LLM_API_KEY:
        raise RuntimeError("未设置 MINIMAX_API_KEY 环境变量")

    resp = requests.post(
        f"{LLM_BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": LLM_MODEL,
            "messages": messages,
            "temperature": temperature,
        },
        timeout=30,
    )
    data = resp.json()

    if "error" in data:
        raise RuntimeError(f"LLM 报错: {data['error']}")

    return data["choices"][0]["message"]["content"]


def ask_llm_stream(messages: List[Dict[str, str]], temperature: float = 0.7,
                   tools: List[Dict] = None) -> Iterator[Dict]:
    """流式调用 LLM - 每个 token yield 一次

    Args:
        messages: OpenAI 协议消息列表
        temperature: 0=死板/确定
        tools: 可选工具列表（OpenAI tools 协议格式）

    Yields:
        {"type": "token", "content": "..."}        # 流式 token
        {"type": "tool_call", "name": "...", "arguments": {...}}  # 工具调用
        {"type": "done", "finish_reason": "stop"}   # 结束
        {"type": "error", "message": "..."}         # 错误
    """
    if not LLM_API_KEY:
        # Mock 模式：API key 未设置时返回假数据
        for word in ["（Mock 模式：LLM_API_KEY 未设置）", " 这是一个测试回答，", "流式输出正常。"]:
            yield {"type": "token", "content": word}
        yield {"type": "done", "finish_reason": "stop"}
        return

    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "temperature": temperature,
        "stream": True,
    }
    if tools:
        payload["tools"] = tools

    try:
        resp = requests.post(
            f"{LLM_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {LLM_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            stream=True,
            timeout=60,
        )

        # 累积工具调用的 fragments
        tool_call_id = None
        tool_call_name = None
        tool_call_args = ""

        for line in resp.iter_lines():
            if not line:
                continue
            line_str = line.decode("utf-8")
            if not line_str.startswith("data: "):
                continue
            data_str = line_str[6:]
            if data_str.strip() == "[DONE]":
                break
            try:
                chunk = json.loads(data_str)
            except json.JSONDecodeError:
                continue

            if "error" in chunk:
                yield {"type": "error", "message": chunk["error"]}
                return

            choice = chunk.get("choices", [{}])[0]
            delta = choice.get("delta", {})
            finish_reason = choice.get("finish_reason")

            # 1. 普通 content token
            if delta.get("content"):
                yield {"type": "token", "content": delta["content"]}

            # 2. 工具调用（流式累积）
            if delta.get("tool_calls"):
                tc = delta["tool_calls"][0]
                if tc.get("id"):
                    tool_call_id = tc["id"]
                if tc.get("function", {}).get("name"):
                    tool_call_name = tc["function"]["name"]
                if tc.get("function", {}).get("arguments"):
                    tool_call_args += tc["function"]["arguments"]

            # 3. 流结束
            if finish_reason:
                if tool_call_name:
                    try:
                        args = json.loads(tool_call_args) if tool_call_args else {}
                    except json.JSONDecodeError:
                        args = {"_raw": tool_call_args}
                    yield {
                        "type": "tool_call",
                        "id": tool_call_id,
                        "name": tool_call_name,
                        "arguments": args,
                    }
                yield {"type": "done", "finish_reason": finish_reason}
                return
    except requests.RequestException as e:
        yield {"type": "error", "message": str(e)}


if __name__ == "__main__":
    # 测试：直接跑这个文件就能用
    answer = ask_llm([
        {"role": "system", "content": "你是报价员助手，回复必须包含 emoji"},
        {"role": "user", "content": "1+1=?"}
    ], temperature=0)
    print(f"💬 {answer}")
