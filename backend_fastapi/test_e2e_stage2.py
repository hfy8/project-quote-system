"""阶段 2 端到端 API 测试 - 10 个新工具"""
import requests, json

BASE = "http://localhost:5001"

# 登录
r = requests.post(f"{BASE}/api/auth/login", json={"username":"admin","password":"admin123"})
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print(f"登录: {r.status_code}, token: {token[:30]}...")

# 块 1：审计
print("\n" + "=" * 50)
print("块 1：AI 审计")
print("=" * 50)

tests_b1 = [
    ("audit_quotation", {"quotation_id": 15}, "审报价单 15"),
    ("audit_materials_price", {"category": ""}, "审全部物料"),
    ("audit_labor_hours", {"quotation_id": 15}, "审工时(15)"),
    ("audit_labor_hours", {"quotation_id": None}, "审全部工时"),
]

# 块 2：分析
print("\n" + "=" * 50)
print("块 2：业务分析")
print("=" * 50)

tests_b2 = [
    ("analyze_profitability", {"limit": 3}, "毛利分析"),
    ("analyze_trends", {"months": 4}, "趋势分析"),
]

# 块 3：模拟
print("\n" + "=" * 50)
print("块 3：调整模拟")
print("=" * 50)

tests_b3 = [
    ("simulate_quotation_change", {"quotation_id": 15, "discount_rate": 0.05, "target_profit_rate": 0.10}, "降价5%保持10%毛利"),
]

# 块 4：RAG
print("\n" + "=" * 50)
print("块 4：RAG 知识库")
print("=" * 50)

tests_b4 = [
    ("search_knowledge", {"query": "毛利", "doc_type": ""}, "搜毛利"),
    ("search_knowledge", {"query": "运输", "doc_type": "spec"}, "搜运输(规范)"),
    ("add_knowledge", {"title": "E2E测试", "content": "API测试添加", "doc_type": "faq", "keywords": "e2e,api"}, "添加知识"),
]

# 用 LLM 跑端到端
all_tests = tests_b1 + tests_b2 + tests_b3 + tests_b4
passed = 0
for tool_name, args, desc in all_tests:
    # 构造自然语言 query
    if tool_name == "audit_quotation":
        q = f"帮我审一下报价单 {args['quotation_id']}"
    elif tool_name == "audit_materials_price":
        q = "审一下所有物料价格"
    elif tool_name == "audit_labor_hours":
        if args.get("quotation_id"):
            q = f"审一下报价单 {args['quotation_id']} 的工时"
        else:
            q = "审一下所有工时"
    elif tool_name == "analyze_profitability":
        q = "看下毛利分析"
    elif tool_name == "analyze_trends":
        q = "看下最近趋势"
    elif tool_name == "simulate_quotation_change":
        q = f"报价单 {args['quotation_id']} 降价 {int(args['discount_rate']*100)}% 还能保持 {int(args['target_profit_rate']*100)}% 毛利吗"
    elif tool_name == "search_knowledge":
        q = f"查一下 '{args['query']}' 相关的业务知识"
    elif tool_name == "add_knowledge":
        q = f"记一下：{args['title']} - {args['content']}"
    else:
        q = tool_name

    r = requests.post(f"{BASE}/api/ai/ask", headers=headers, json={"query": q}, timeout=60)
    if r.status_code == 200:
        d = r.json()
        if d.get("success"):
            tools_used = d.get("tools_used", [])
            if tool_name in tools_used:
                print(f"✅ {tool_name}: {desc}")
                print(f"   回答: {d.get('answer', '')[:200]}")
                passed += 1
            else:
                print(f"⚠️  {tool_name}: 调了别的工具 {tools_used}")
        else:
            print(f"❌ {tool_name}: 失败 - {d.get('error', '?')}")
    else:
        print(f"❌ {tool_name}: HTTP {r.status_code}")

print(f"\n{'='*50}")
print(f"端到端测试: {passed}/{len(all_tests)} 通过")
