#!/usr/bin/env python3
"""Rewrite llm_client with MiniMax→DeepSeek fallback"""
import os
import logging
import json
from typing import List, Dict, Iterator
import requests
from dotenv import load_dotenv

load_dotenv()

# === Primary: MiniMax ===
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY") or os.getenv("LLM_API_KEY")
MINIMAX_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.minimax.chat/v1")
MINIMAX_MODEL = os.getenv("MINIMAX_MODEL", os.getenv("LLM_MODEL", "MiniMax-M2.7"))

# === Fallback: DeepSeek ===
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

# === Backward-compat exports ===
LLM_API_KEY = MINIMAX_API_KEY
LLM_BASE_URL = MINIMAX_BASE_URL
LLM_MODEL = MINIMAX_MODEL


# === 过滤推理模型的 <think> 块 ===
# Qwen3 / DeepSeek-R1 等模型把"思考"放在 content 字段里（不是 OpenAI 标准的 reasoning_content）
# 流式响应时，token 跨多个 chunk 到达，要正确处理跨 chunk 的 <think> 边界
import re
_THINK_OPEN = "<think>"
_THINK_CLOSE = "</think>"
_in_think_block = False  # 模块级状态，跨 chunk 保留

def _split_think_tokens(content: str):
    """把 content 切成若干片段，跳过 <think>...</think> 部分。

    返回「不在 think 块里」的内容片段列表（可能为空）。
    """
    global _in_think_block
    out = []
    rest = content
    while rest:
        if _in_think_block:
            # 已经在 think 块里：找下一个 </think>
            idx = rest.find(_THINK_CLOSE)
            if idx == -1:
                # 整个 rest 都在 think 里，丢掉
                return out
            rest = rest[idx + len(_THINK_CLOSE):]
            _in_think_block = False
        else:
            # 不在 think 块里：找下一个 <think>
            idx = rest.find(_THINK_OPEN)
            if idx == -1:
                # 整段都是正常内容
                out.append(rest)
                return out
            # think 之前的部分是正常内容
            out.append(rest[:idx])
            rest = rest[idx + len(_THINK_OPEN):]
            _in_think_block = True
    return out

logger = logging.getLogger(__name__)


def _is_rate_limit(data: dict) -> bool:
    """Check if the API error is a rate limit / quota exhaustion"""
    err = data.get("error", {})
    if isinstance(err, str):
        err = {"message": err}
    code = err.get("code", "")
    http_code = err.get("http_code", 0)
    msg = err.get("message", "")
    return any([
        http_code == 429,
        "rate_limit" in str(code),
        "用量上限" in msg,
        "quota" in msg.lower(),
        "rate limit" in msg.lower(),
    ])


def _call_provider(base_url: str, api_key: str, model: str,
                   messages: list, temperature: float, timeout: int = 30,
                   stream: bool = False, tools: list = None) -> requests.Response:
    """Make a request to a provider's chat completions endpoint"""
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    if stream:
        payload["stream"] = True
    if tools:
        payload["tools"] = tools

    # DeepSeek uses api.deepseek.com/chat/completions (no /v1)
    if "api.deepseek.com" in base_url and not base_url.endswith("/v1"):
        url = f"{base_url.rstrip('/')}/chat/completions"
    else:
        url = f"{base_url.rstrip('/')}/chat/completions"

    return requests.post(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        stream=stream,
        timeout=timeout,
    )


def ask_llm(messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
    """问 LLM + fallback: MiniMax → DeepSeek"""
    # --- Primary: MiniMax ---
    if MINIMAX_API_KEY:
        try:
            resp = requests.post(
                f"{MINIMAX_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {MINIMAX_API_KEY}", "Content-Type": "application/json"},
                json={"model": MINIMAX_MODEL, "messages": messages, "temperature": temperature},
                timeout=30,
            )
            data = resp.json()
            if "error" in data and _is_rate_limit(data):
                logger.warning(f"⚠️ MiniMax 额度不足，切换到 DeepSeek")
            elif "error" in data:
                raise RuntimeError(f"MiniMax 报错: {data['error']}")
            else:
                return data["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            logger.warning(f"⚠️ MiniMax 请求失败 ({e})，切换到 DeepSeek")
    else:
        logger.info("ℹ️ 未配置 MiniMax API key")

    # --- Fallback: DeepSeek ---
    if not DEEPSEEK_API_KEY:
        raise RuntimeError("未设置 MINIMAX_API_KEY 或 DEEPSEEK_API_KEY")

    logger.info(f"🔄 Fallback → DeepSeek ({DEEPSEEK_MODEL})")
    resp = _call_provider(
        base_url=DEEPSEEK_BASE_URL,
        api_key=DEEPSEEK_API_KEY,
        model=DEEPSEEK_MODEL,
        messages=messages,
        temperature=temperature,
    )
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"DeepSeek 报错: {data['error']}")
    return data["choices"][0]["message"]["content"]


def ask_llm_stream(messages: List[Dict[str, str]], temperature: float = 0.7,
                   tools: List[Dict] = None) -> Iterator[Dict]:
    """流式调用 LLM + fallback: MiniMax → DeepSeek"""
    # --- Primary: MiniMax ---
    if MINIMAX_API_KEY:
        try:
            yield {"type": "provider", "provider": "minimax"}
            payload = {
                "model": MINIMAX_MODEL,
                "messages": messages,
                "temperature": temperature,
                "stream": True,
            }
            if tools:
                payload["tools"] = tools

            resp = requests.post(
                f"{MINIMAX_BASE_URL}/chat/completions",
                headers={"Authorization": f"Bearer {MINIMAX_API_KEY}", "Content-Type": "application/json"},
                json=payload,
                stream=True,
                timeout=60,
            )
            data_json = {}
            try:
                # Peek first byte to see if it's an error
                data_json = resp.json()
            except (json.JSONDecodeError, ValueError):
                pass  # not JSON = streaming response, good

            if resp.status_code == 429 or (data_json and "error" in data_json and _is_rate_limit(data_json)):
                logger.warning("⚠️ MiniMax 额度不足，切换到 DeepSeek")
                raise FallbackTrigger("rate_limit")
            if "error" in data_json:
                yield {"type": "error", "message": f"MiniMax 报错: {data_json['error']}"}
                return

            # Normal streaming
            yield from _stream_events(resp)
            return
        except FallbackTrigger:
            pass  # fall through to DeepSeek
        except requests.RequestException as e:
            logger.warning(f"⚠️ MiniMax 请求失败 ({e})，切换到 DeepSeek")
    else:
        logger.info("ℹ️ 未配置 MiniMax API key")

    # --- Fallback: DeepSeek ---
    if not DEEPSEEK_API_KEY:
        for word in ["（Mock 模式：已无可用 API key）"]:
            yield {"type": "token", "content": word}
        yield {"type": "done", "finish_reason": "stop"}
        return

    yield {"type": "provider", "provider": "deepseek"}
    logger.info(f"🔄 Fallback → DeepSeek ({DEEPSEEK_MODEL})")

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "temperature": temperature,
        "stream": True,
    }
    if tools:
        payload["tools"] = tools

    try:
        resp = _call_provider(
            base_url=DEEPSEEK_BASE_URL,
            api_key=DEEPSEEK_API_KEY,
            model=DEEPSEEK_MODEL,
            messages=messages,
            temperature=temperature,
            stream=True,
            tools=tools,
        )
    except requests.RequestException as e:
        yield {"type": "error", "message": str(e)}
        return

    yield from _stream_events(resp)


def _stream_events(resp: requests.Response) -> Iterator[Dict]:
    """Parse SSE stream from a chat completions response"""
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
            yield {"type": "done", "finish_reason": "stop"}
            return
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

        # 1. Normal content token — 过滤 Qwen/DeepSeek 推理模型的 <think>...</think> 块
        content = delta.get("content")
        if content:
            # 检测是否开始/结束 <think> 块
            for piece in _split_think_tokens(content):
                if piece:
                    yield {"type": "token", "content": piece}

        # 2. Tool calls (streaming accumulation)
        if delta.get("tool_calls"):
            tc = delta["tool_calls"][0]
            if tc.get("id"):
                tool_call_id = tc["id"]
            if tc.get("function", {}).get("name"):
                tool_call_name = tc["function"]["name"]
            if tc.get("function", {}).get("arguments"):
                tool_call_args += tc["function"]["arguments"]

        # 3. Stream end
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


class FallbackTrigger(Exception):
    """Exception to trigger fallback from MiniMax to DeepSeek"""
    pass


if __name__ == "__main__":
    # Test
    answer = ask_llm([
        {"role": "system", "content": "你是报价员助手，回复必须包含 emoji"},
        {"role": "user", "content": "1+1=?"}
    ], temperature=0)
    print(f"💬 {answer}")
