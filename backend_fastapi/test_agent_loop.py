"""Agent 多步失控修复验证"""
import requests
import json
import time

BASE = "http://localhost:5001"

# 登录
r = requests.post(f"{BASE}/api/auth/login", json={"username": "admin", "password": "admin123"})
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}


def test_query(query, label):
    print(f"\n{'=' * 60}")
    print(f"[{label}] {query}")
    print("=" * 60)
    r = requests.post(
        f"{BASE}/api/ai/ask/stream",
        headers={**headers, "Accept": "text/event-stream"},
        json={"query": query, "max_steps": 20},
        stream=True, timeout=120,
    )
    tool_calls = []
    warnings = []
    start_time = time.time()
    answer_preview = ""

    for raw_line in r.iter_lines(decode_unicode=True):
        if not raw_line or not raw_line.startswith("data: "):
            continue
        try:
            event = json.loads(raw_line[6:])
        except json.JSONDecodeError:
            continue

        etype = event.get("type")
        if etype == "tool_call":
            tool_calls.append(event["name"])
            print(f"  🔧 step {len(tool_calls)}: {event['name']}({event.get('arguments', {})})")
        elif etype == "tool_executing":
            print(f"  ⚙️  执行 {event['name']}")
        elif etype == "tool_result":
            preview = event.get("result", "")[:60]
            print(f"  ✅ result: {preview}...")
        elif etype == "warning":
            warnings.append(event["message"])
            print(f"  ⚠️  WARNING: {event['message']}")
        elif etype == "done":
            answer_preview = event.get("answer", "")[:200]
            elapsed = time.time() - start_time
            print(f"\n  📊 统计:")
            print(f"    工具调用次数: {len(tool_calls)}")
            print(f"    tools_used: {event.get('tools_used')}")
            print(f"    steps: {event.get('steps')}")
            print(f"    耗时: {elapsed:.2f}s")
            print(f"    warnings: {len(warnings)}")
            print(f"  📝 答案预览:")
            print(f"    {answer_preview}")
            return len(tool_calls), event.get("steps"), warnings

    return len(tool_calls), -1, warnings


# 测试 1: 之前会失控的 query（"列模块 + 算成本"）
tc1, steps1, w1 = test_query("列出所有模块，再算一个材料 5000 元 240 工时的报价", "测试1")

# 测试 2: 单步查询（应该 1 步搞定）
tc2, steps2, w2 = test_query("物料库有哪些酒精棉片？", "测试2")

# 测试 3: 对比（应该 1 步搞定）
tc3, steps3, w3 = test_query("对比报价单 15 和 13", "测试3")

# 总结
print("\n" + "=" * 60)
print("总评：")
print("=" * 60)
results = [
    ("测试1 (列模块+算成本)", tc1, steps1, w1),
    ("测试2 (单步查询)", tc2, steps2, w2),
    ("测试3 (对比)", tc3, steps3, w3),
]
ok = True
for label, tc, steps, w in results:
    status = "✅" if tc <= 5 else "❌"
    print(f"  {status} {label}: {tc} 次工具调用, steps={steps}, warnings={len(w)}")
    if tc > 5:
        ok = False

if ok:
    print("\n🎉 所有测试通过！Agent 多步失控已修复。")
else:
    print("\n⚠️ 仍有失控场景")
