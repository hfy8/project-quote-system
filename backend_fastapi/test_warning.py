"""验证 warning 事件能从后端发出"""
import requests
import json
import time

BASE = "http://localhost:5001"

# 登录
r = requests.post(f"{BASE}/api/auth/login", json={"username": "admin", "password": "admin123"})
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}


def test_warning(query, label):
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
    answer_preview = ""
    start_time = time.time()

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
        elif etype == "warning":
            warnings.append(event["message"])
            print(f"  ⚠️  WARNING: {event['message']}")
        elif etype == "done":
            answer_preview = (event.get("answer") or "")[:150]
            elapsed = time.time() - start_time
            print(f"\n  📊 统计:")
            print(f"    工具调用: {len(tool_calls)}")
            print(f"    warnings: {len(warnings)}")
            print(f"    steps: {event.get('steps')}")
            print(f"    耗时: {elapsed:.2f}s")
            if warnings:
                print(f"    ✅ 警告事件已发出：{warnings}")
            else:
                print(f"    (本次未触发 warning - 说明 LLM 没失控)")
            return

    return


# 测试 1: 简单查询（应该 1 步搞定，无 warning）
test_warning("物料库有哪些酒精棉片？", "测试1 - 简单查询")

# 测试 2: 模糊查询（看 LLM 是否会重复调工具）
# 这个测试可能/可能不触发 warning，取决于 LLM 行为
test_warning("算一个项目的成本，材料 5000 元，工时 240 小时", "测试2 - 单步成本")

# 测试 3: 复杂任务 - 多步推理
test_warning("列出所有模块，再算一个材料 8000 元、工时 100 小时的报价", "测试3 - 复合任务")

print("\n" + "=" * 60)
print("✅ warning 事件测试完成")
print("=" * 60)
