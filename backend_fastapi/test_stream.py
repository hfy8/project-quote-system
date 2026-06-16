"""阶段 3 测试 - 流式 + 多轮 + 鉴权"""
import requests, json, time

BASE = "http://localhost:5001"

# 1. 登录
r = requests.post(f"{BASE}/api/auth/login", json={"username":"admin","password":"admin123"})
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print(f"登录: {r.status_code}")

# 2. /ask 非流式（带 conversation_id）
print("\n=== /ask 非流式 (多轮) ===")
conv_id = None
for q in ["物料库有哪些酒精棉片？", "那它单价多少？", "对比下其他医用耗材"]:
    r = requests.post(f"{BASE}/api/ai/ask", headers=headers, json={"query": q, "conversation_id": conv_id}, timeout=30)
    d = r.json()
    conv_id = d.get("conversation_id")
    print(f"Q: {q}")
    print(f"A: {d.get('answer', '')[:150]}...")
    print(f"   conv_id: {conv_id[:8]}, success: {d.get('success')}")
    print()

# 3. /ask/stream 流式
print("=== /ask/stream 流式 ===")
r = requests.post(
    f"{BASE}/api/ai/ask/stream",
    headers=headers,
    json={"query": "你好，介绍下自己", "conversation_id": conv_id},
    stream=True,
    timeout=30,
)
print(f"HTTP: {r.status_code}, Content-Type: {r.headers.get('Content-Type')}")
start = time.time()
first_token_time = None
full_answer = ""
for line in r.iter_lines():
    if not line:
        continue
    line = line.decode("utf-8")
    if not line.startswith("data: "):
        continue
    data_str = line[6:]
    if not data_str.strip():
        continue
    try:
        ev = json.loads(data_str)
    except:
        continue
    etype = ev.get("type")
    if etype == "token":
        if first_token_time is None:
            first_token_time = time.time() - start
        full_answer += ev.get("content", "")
    elif etype == "done":
        print(f"done event: answer={ev.get('answer', '')[:200]}")
    elif etype == "error":
        print(f"error: {ev}")
print(f"\n首 token 延迟: {first_token_time:.3f}s (越低越好)")
print(f"完整回答: {full_answer}")

# 4. 健康检查（看 active_conversations）
r = requests.get(f"{BASE}/api/ai/health")
print(f"\n健康: {r.json()}")

# 5. 鉴权检查
print("\n=== 鉴权测试 ===")
r = requests.post(f"{BASE}/api/ai/ask/stream", json={"query": "test"}, stream=True)
print(f"未登录: {r.status_code}")
r = requests.post(f"{BASE}/api/ai/ask", json={"query": "test"})
print(f"未登录 /ask: {r.status_code}")

# 6. 清会话
r = requests.delete(f"{BASE}/api/ai/conversation/{conv_id}", headers=headers)
print(f"清会话: {r.json()}")
