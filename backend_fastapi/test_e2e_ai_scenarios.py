"""E2E 场景测试：5 个真实业务问句端到端跑通

模拟真实用户使用 AI 助手的完整流程：
1. 用户登录
2. 问业务问题（覆盖读/写/混合场景）
3. 验证返回内容合理 + 调用了正确的工具
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DEEPSEEK_API_KEY", "dummy")

import requests

BASE = "http://localhost:5001/api"


def login(username="admin", password="admin123"):
    r = requests.post(f"{BASE}/auth/login", json={"username": username, "password": password}, timeout=5)
    r.raise_for_status()
    return r.json()["access_token"]


def ask(token, query, max_steps=8, timeout=90):
    """发送流式问句，返回 (steps, answer_text, tool_names)"""
    resp = requests.post(
        f"{BASE}/ai/ask/stream",
        headers={"Authorization": f"Bearer {token}"},
        json={"query": query, "max_steps": max_steps},
        stream=True, timeout=timeout,
    )
    resp.raise_for_status()
    full = ""
    steps = 0
    tools = []
    for line in resp.iter_lines():
        if not line:
            continue
        d = json.loads(line.decode().lstrip("data: "))
        t = d.get("type", "")
        if t == "token":
            full += d["content"]
        elif t == "tool_call":
            if d.get("name"):
                tools.append(d["name"])
        elif t == "tool_result":
            pass
        elif t == "done":
            steps = d.get("steps", 0)
            break
        elif t == "error":
            return -1, d.get("message", ""), []
    return steps, full, tools


# ============== 场景 1：新人查资料（读） ==============

def test_scenario_1_knowledge_search():
    """新人问业务规范"""
    print("\n=== 场景 1: 新人问业务规范 ===")
    token = login()
    steps, ans, tools = ask(token, "知识库里关于运输费的计费规则是什么？")

    assert steps > 0, "应该调用工具"
    assert "search_knowledge" in tools or "search_knowledge_hybrid" in tools, \
        f"应该调知识搜索工具，实际调了 {tools}"
    assert "运输" in ans or "运费" in ans, "回答应包含运输相关内容"
    print(f"✅ Steps={steps}, Tools={tools}")
    print(f"   Answer: {ans[:150]}...")


# ============== 场景 2：日常工作（读） ==============

def test_scenario_2_daily_dashboard():
    """业务员的日常工作台"""
    print("\n=== 场景 2: 业务员的日常工作台 ===")
    token = login()
    steps, ans, tools = ask(token, "我今天有什么待办？")

    assert steps > 0
    assert "list_pending_tasks" in tools, f"应调 list_pending_tools，实际 {tools}"
    print(f"✅ Steps={steps}, Tools={tools}")
    print(f"   Answer: {ans[:150]}...")


# ============== 场景 3：完整查询（多工具组合） ==============

def test_scenario_3_full_quotation():
    """查询报价单完整信息"""
    print("\n=== 场景 3: 报价单完整查询 ===")
    token = login()
    steps, ans, tools = ask(token, "报价单 14 的完整信息，包括模块物料和差旅费")

    # 应该调 get_quotation_full 一次拿到所有数据
    assert steps <= 6, f"应该 ≤6 步（实际 {steps}）"
    assert "get_quotation_full" in tools, f"应调 get_quotation_full，实际 {tools}"
    print(f"✅ Steps={steps}, Tools={tools}")
    print(f"   Answer: {ans[:200]}...")


# ============== 场景 4：组合查询（多个工具） ==============

def test_scenario_4_material_search():
    """物料多维搜索"""
    print("\n=== 场景 4: 物料搜索 ===")
    token = login()
    steps, ans, tools = ask(token, "所有标准件物料有哪些？")

    assert "search_materials_v2" in tools or "list_material_categories" in tools, \
        f"应调物料工具，实际 {tools}"
    print(f"✅ Steps={steps}, Tools={tools}")
    print(f"   Answer: {ans[:150]}...")


# ============== 场景 5：权限拒绝 ==============

def test_scenario_5_permission_denied():
    """viewer 尝试改状态被拒绝"""
    print("\n=== 场景 5: viewer 改状态被拒 ===")
    # 找一个非 admin 账号
    for u, p in [("viewer", "viewer123"), ("RS7281", "123456")]:
        try:
            token = login(u, p)
            user = u
            break
        except Exception:
            continue
    else:
        print("⚠️  无 viewer 账号，跳过")
        return

    steps, ans, tools = ask(token, "把报价单 14 改成 draft 状态")

    assert "update_quotation_status" in tools, f"应尝试调 update_quotation_status，实际 {tools}"
    assert "权限" in ans or "拒绝" in ans or "不足" in ans, \
        f"回答应提及权限拒绝，实际: {ans[:200]}"
    print(f"✅ Steps={steps}, Tools={tools}, user={user}")
    print(f"   Answer: {ans[:200]}...")


# ============== 运行所有 ==============

if __name__ == "__main__":
    # 等后端 ready
    print("⏳ 等待后端...")
    for i in range(15):
        try:
            r = requests.get(f"{BASE}/ai/health", timeout=2)
            if r.status_code == 200:
                break
        except Exception:
            pass
        time.sleep(1)

    tests = [
        test_scenario_1_knowledge_search,
        test_scenario_2_daily_dashboard,
        test_scenario_3_full_quotation,
        test_scenario_4_material_search,
        test_scenario_5_permission_denied,
    ]

    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except AssertionError as e:
            print(f"❌ {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {t.__name__} (异常): {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"总计: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)