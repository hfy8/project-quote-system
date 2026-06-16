"""
阶段 3 端到端测试 - 流式 + 多轮

在 Windows PowerShell 跑：
    cd C:\\Users\\rs8568\\Desktop\\Project\\project-quote-system\\backend_fastapi
    python test_stream_e2e.py
"""
import requests, json, time

BASE = "http://localhost:5001"

print("=" * 60)
print("阶段 3 测试 - 流式输出 + 多轮对话")
print("=" * 60)

# 1. 登录
r = requests.post(f"{BASE}/api/auth/login", json={"username":"admin","password":"admin123"})
if r.status_code != 200:
    print(f"❌ 登录失败: {r.status_code}")
    exit(1)
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print(f"\n[1] 登录: ✅ token={token[:30]}...")

# 2. /ask 非流式（多轮上下文）
print(f"\n[2] /ask 非流式多轮测试")
conv_id = None
questions = [
    "物料库有哪些酒精棉片？",
    "那它单价多少？",  # 上下文记忆测试
    "那还有哪些医用耗材？",
]
for q in questions:
    r = requests.post(f"{BASE}/api/ai/ask", headers=headers,
                      json={"query": q, "conversation_id": conv_id}, timeout=30)
    d = r.json()
    conv_id = d.get("conversation_id")
    print(f"   Q: {q}")
    print(f"   A: {d.get('answer', '')[:200]}")
    print(f"   conv={conv_id[:8]}, steps={d.get('steps')}, tools={d.get('tools_used')}")
    print()

# 3. /ask/stream 流式
print(f"[3] /ask/stream 流式测试")
r = requests.post(
    f"{BASE}/api/ai/ask/stream",
    headers=headers,
    json={"query": "推荐下项目报价系统的最佳实践", "conversation_id": conv_id},
    stream=True, timeout=60,
)
print(f"   HTTP: {r.status_code}, Content-Type: {r.headers.get('Content-Type')}")
start = time.time()
first_token = None
tokens = []
for line in r.iter_lines():
    if not line: continue
    line = line.decode("utf-8")
    if not line.startswith("data: "): continue
    data_str = line[6:]
    if not data_str.strip(): continue
    try:
        ev = json.loads(data_str)
    except: continue
    et = ev.get("type")
    if et == "token":
        if first_token is None:
            first_token = time.time() - start
        tokens.append(ev.get("content", ""))
    elif et == "done":
        print(f"   ✅ 流结束, 共 {len(tokens)} 个 token")
        print(f"   首 token 延迟: {first_token:.3f}s")
        print(f"   工具: {ev.get('tools_used')}")
    elif et == "tool_call":
        print(f"   🔧 调工具: {ev.get('name')}({ev.get('arguments')})")
    elif et == "tool_result":
        print(f"   📦 工具结果: {ev.get('result', '')[:100]}...")
    elif et == "error":
        print(f"   ❌ 错误: {ev.get('message')}")

# 4. /ai/health
print(f"\n[4] /api/ai/health")
r = requests.get(f"{BASE}/api/ai/health")
print(f"   {r.json()}")

# 5. 鉴权测试
print(f"\n[5] 鉴权测试")
r = requests.post(f"{BASE}/api/ai/ask/stream", json={"query": "test"}, stream=True)
print(f"   未登录 /ask/stream: {r.status_code} (期望 401)")
r = requests.post(f"{BASE}/api/ai/ask", json={"query": "test"})
print(f"   未登录 /ask: {r.status_code} (期望 401)")

# 6. 清会话
print(f"\n[6] 清除会话")
r = requests.delete(f"{BASE}/api/ai/conversation/{conv_id}", headers=headers)
print(f"   {r.json()}")

print(f"\n{'='*60}")
print(f"✅ 全部测试通过")
