"""第 3 课：Agent v2 - 用 OpenAI tools 协议"""
import os
import json
import requests
from typing import List, Dict
from utils.llm_client import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL  # 复用第 1 课的配置
from core.services.ai_tools import TOOLS, execute_tool
def call_llm_with_tools(messages: List[Dict], tools: List[Dict]) -> Dict:
    """调 LLM，带上 tools 协议"""
    resp = requests.post(
        f"{LLM_BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {LLM_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": LLM_MODEL,
            "messages": messages,
            "tools": tools,
            "temperature": 0,
        },
        timeout=30,
    )
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"LLM 报错: {data['error']}")
    return data
def run_agent(user_query: str, max_steps: int = 10) -> str:
    """Agent 主循环 - 用 OpenAI tools 协议"""
    messages = [
        {"role": "system", "content": "你是报价员助手，善用工具查真实数据。"},
        {"role": "user", "content": user_query}
    ]

    for step in range(max_steps):
        print(f"\n--- Step {step + 1} ---")

        # 1. 调 LLM（带 tools）
        data = call_llm_with_tools(messages, TOOLS)
        message = data["choices"][0]["message"]

        # 2. 检查 LLM 是否想调工具
        if message.get("tool_calls"):
            # LLM 决定调工具
              tool_call = message["tool_calls"][0]
              tool_name = tool_call["function"]["name"]
              tool_args = json.loads(tool_call["function"]["arguments"])

              print(f"🔧 LLM 想调工具: {tool_name}({tool_args})")

              # 3. 执行工具
              tool_result = execute_tool(tool_name, tool_args)
              print(f"📊 工具返回: {tool_result[:200]}...")  # 截断显示

              # 4. 把"工具调用 + 工具结果"塞回 messages，让 LLM 继续想
              messages.append(message)  # 工具调用消息
              messages.append({
                  "role": "tool",
                  "tool_call_id": tool_call["id"],
                  "content": tool_result,
              })
        else:
              # LLM 直接给答案了
              answer = message.get("content", "")
              print(f"💬 LLM 回答: {answer[:200]}...")
              return answer

    return "达到最大步数，强制结束"
if __name__ == "__main__":
    print("🚀 启动 Agent v2（tools 协议）")
    result = run_agent("报价单 15 毛利率多少？")
    print(f"\n✅ 最终回答:\n{result}")