import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import json
from typing import TypedDict, List, Dict, Annotated
from langgraph.graph import StateGraph, END
import operator
from utils.llm_client import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL
from core.services.ai_tools import TOOLS, execute_tool
import requests
# ============== 1. 定义 Agent 状态 ==============
class AgentState(TypedDict):
    """Agent 状态机 - 一次对话的所有数据"""
    user_query: str                       # 用户问题
    messages: List[Dict]                  # 消息历史（喂给 LLM 的）
    intent: str                           # 理解出的意图（"search_materials" / "answer" / ...）
    tool_name: str                        # 决定要调的工具
    tool_args: Dict                       # 工具参数
    tool_result: str                      # 工具返回
    final_answer: str                     # 最终答案
    step_count: int                       # 步数（防死循环）
# ============== 2. 节点函数 ==============
def call_llm_node(state: AgentState) -> AgentState:
    """节点 1：调 LLM，让它决策"""
    print(f"\n--- [call_llm] step={state['step_count']} ---")

    resp = requests.post(
        f"{LLM_BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type": "application/json"},
        json={
            "model": LLM_MODEL,
            "messages": state["messages"],
            "tools": TOOLS,
            "temperature": 0,
        },
        timeout=30,
    )
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"LLM 报错: {data['error']}")

    message = data["choices"][0]["message"]
    state["messages"].append(message)
    print(message)
    # 如果 LLM 想调工具，提取决策
    if message.get("tool_calls"):
        tool_call = message["tool_calls"][0]
        state["tool_name"] = tool_call["function"]["name"]
        state["tool_args"] = json.loads(tool_call["function"]["arguments"])
        print(f"  → 决定调: {state['tool_name']}({state['tool_args']})")
    else:
        state["tool_name"] = ""
        state["tool_args"] = {}
        state["final_answer"] = message.get("content", "")
        print(f"  → 直接给答案")

        state["step_count"] += 1
    return state
def execute_tool_node(state: AgentState) -> AgentState:
    """节点 2：执行工具"""
    print(f"--- [execute_tool] {state['tool_name']} ---")

    result = execute_tool(state["tool_name"], state["tool_args"])
    state["tool_result"] = result
    print(f"  → 返回: {result[:150]}...")

    # 把工具结果塞回 messages（让 LLM 下一步看到）
    state["messages"].append({
        "role": "tool",
        "tool_call_id": state["messages"][-1]["tool_calls"][0]["id"],
        "content": result,
    })
    return state
def should_continue(state: AgentState) -> str:
    """路由函数：决定下一步去哪"""
    # 超过 5 步强制结束
    if state["step_count"] >= 10:
        return "end"

    # LLM 没调工具，说明直接给答案了
    if not state["tool_name"]:
        return "end"

    # LLM 调了工具，去执行
    return "execute"
# ============== 3. 构建状态机 ==============
def build_agent():
    """构建 LangGraph 状态机"""
    workflow = StateGraph(AgentState)

    # 加节点
    workflow.add_node("call_llm", call_llm_node)
    workflow.add_node("execute_tool", execute_tool_node)

    # 入口
    workflow.set_entry_point("call_llm")

    # 边：call_llm 之后看 should_continue 决定去哪
    workflow.add_conditional_edges(
        "call_llm",
        should_continue,
        {
            "execute": "execute_tool",   # 去执行工具
            "end": END,                    # 结束
        }
    )

    # 边：execute_tool 之后回 call_llm（让 LLM 看工具结果再决策）
    workflow.add_edge("execute_tool", "call_llm")

    return workflow.compile()
# ============== 4. 运行入口 ==============
def run_agent(user_query: str) -> str:
    """跑 Agent"""
    # 初始状态
    initial_state = {
        "user_query": user_query,
        "messages": [
            {"role": "system", "content": "你是报价员助手，善用工具查真实数据。"},
            {"role": "user", "content": user_query}
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

    # 找最后一条 assistant 消息
    for msg in reversed(final_state["messages"]):
        if msg.get("role") == "assistant":
            content = msg.get("content", "")
            if content and not msg.get("tool_calls"):
                return content

    return final_state.get("final_answer", "未生成答案")
if __name__ == "__main__":
    print("🚀 启动 LangGraph Agent\n")
    result = run_agent("物料库里有哪些酒精棉片？")
    print(f"\n✅ 最终回答:\n{result}")