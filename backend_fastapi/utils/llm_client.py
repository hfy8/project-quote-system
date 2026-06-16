import os                          # 读环境变量
import logging                      # 打印日志
from typing import List, Dict       # 类型注解，让代码更清晰
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

if __name__ == "__main__":
    # 测试：直接跑这个文件就能用
    answer = ask_llm([
    {"role": "system", "content": "你是报价员助手，回复必须包含 emoji"},
    {"role": "user", "content": "1+1=?"}
], temperature=0)
    print(f"💬 {answer}")