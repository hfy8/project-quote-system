"""API 端到端测试"""
import requests
import json

BASE = "http://localhost:5001"

# 登录
r = requests.post(f"{BASE}/api/auth/login", json={"username":"admin","password":"admin123"})
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print(f"✅ 登录: {r.status_code}")

# 健康检查
r = requests.get(f"{BASE}/api/ai/health")
print(f"✅ 健康: {r.status_code} {r.json()}")

# 测试 1: 查模块（用新工具 list_modules）
print("\n【1】查所有模块")
r = requests.post(f"{BASE}/api/ai/ask", headers=headers,
                  json={"query": "列出物料库里的所有模块"}, timeout=60)
d = r.json()
print(f"  状态: {r.status_code}, 成功: {d.get('success')}, 步数: {d.get('steps')}")
print(f"  工具: {d.get('tools_used')}")
print(f"  回答: {d.get('answer', '')[:300]}...")

# 测试 2: 算成本（用 calculate_quotation_cost）
print("\n【2】算一个项目的成本")
r = requests.post(f"{BASE}/api/ai/ask", headers=headers,
                  json={"query": "材料 5000 元，需要 240 工时，算一下总价"}, timeout=60)
d = r.json()
print(f"  状态: {r.status_code}, 成功: {d.get('success')}, 步数: {d.get('steps')}")
print(f"  工具: {d.get('tools_used')}")
print(f"  回答: {d.get('answer', '')[:300]}...")

# 测试 3: 对比两个报价单
print("\n【3】对比报价单 15 和 13")
r = requests.post(f"{BASE}/api/ai/ask", headers=headers,
                  json={"query": "对比报价单 15 和 13 的毛利率和工时"}, timeout=60)
d = r.json()
print(f"  状态: {r.status_code}, 成功: {d.get('success')}, 步数: {d.get('steps')}")
print(f"  工具: {d.get('tools_used')}")
print(f"  回答: {d.get('answer', '')[:300]}...")

# 测试 4: 推荐物料（基于模块 52）
print("\n【4】模块 52 推荐什么物料")
r = requests.post(f"{BASE}/api/ai/ask", headers=headers,
                  json={"query": "模块 52 一般用什么物料？"}, timeout=60)
d = r.json()
print(f"  状态: {r.status_code}, 成功: {d.get('success')}, 步数: {d.get('steps')}")
print(f"  工具: {d.get('tools_used')}")
print(f"  回答: {d.get('answer', '')[:300]}...")

# 测试 5: 工时估算
print("\n【5】报价单 15 工时多少")
r = requests.post(f"{BASE}/api/ai/ask", headers=headers,
                  json={"query": "报价单 15 的工时是多少？"}, timeout=60)
d = r.json()
print(f"  状态: {r.status_code}, 成功: {d.get('success')}, 步数: {d.get('steps')}")
print(f"  工具: {d.get('tools_used')}")
print(f"  回答: {d.get('answer', '')[:300]}...")

# 测试 6: 多工具组合（高级）
print("\n【6】完整报价方案")
r = requests.post(f"{BASE}/api/ai/ask", headers=headers,
                  json={"query": "我要做一个工位项目，材料预算 8000 元，工时按 100 算，最后总价多少？毛利率多少？"}, timeout=60)
d = r.json()
print(f"  状态: {r.status_code}, 成功: {d.get('success')}, 步数: {d.get('steps')}")
print(f"  工具: {d.get('tools_used')}")
print(f"  回答: {d.get('answer', '')[:500]}...")

print("\n" + "=" * 60)
print("✅ API 端到端测试完成")
