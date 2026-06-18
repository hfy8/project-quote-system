"""检查后端 SSE 是否真的流式"""
import requests
import json
import time

BASE = "http://localhost:5001"

r = requests.post(f"{BASE}/api/auth/login", json={"username": "admin", "password": "admin123"})
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

print("发送 query...")
start = time.time()
r = requests.post(
    f"{BASE}/api/ai/ask/stream",
    headers=headers,
    json={"query": "你好，请简短回复"},
    stream=True,
    timeout=60,
)

print(f"状态码: {r.status_code}, Content-Type: {r.headers.get('content-type')}")
print(f"开始接收...")
print("---")

last_tok_time = start
token_times = []
for line in r.iter_lines():
    if not line:
        continue
    elapsed = time.time() - start
    if line.startswith(b"data: "):
        data = line[6:].decode("utf-8", errors="replace")
        if data.strip() == "[DONE]":
            print(f"[{elapsed:.3f}s] DONE")
            break
        try:
            evt = json.loads(data)
            etype = evt.get("type", "?")
            if etype == "token":
                content = evt.get("content", "")
                token_times.append((elapsed, content))
                print(f"[{elapsed:.3f}s] token: {repr(content)[:60]}")
            elif etype == "tool_call":
                print(f"[{elapsed:.3f}s] tool_call: {evt.get('name')}({evt.get('arguments')})")
            elif etype == "tool_result":
                print(f"[{elapsed:.3f}s] tool_result: {evt.get('name')}")
            elif etype == "warning":
                print(f"[{elapsed:.3f}s] ⚠️  warning: {evt.get('message')[:80]}")
            elif etype == "start":
                print(f"[{elapsed:.3f}s] start: {evt.get('query')[:30]}")
            elif etype == "done":
                print(f"[{elapsed:.3f}s] done: steps={evt.get('steps')}, answer前50字={repr(evt.get('answer',''))[:50]}")
        except Exception as e:
            print(f"[{elapsed:.3f}s] parse err: {data[:80]}")

print(f"---")
print(f"总 token 事件数: {len(token_times)}")
if len(token_times) >= 2:
    intervals = [token_times[i+1][0] - token_times[i][0] for i in range(len(token_times)-1)]
    print(f"token 间隔: min={min(intervals)*1000:.0f}ms, max={max(intervals)*1000:.0f}ms, avg={sum(intervals)/len(intervals)*1000:.0f}ms")
    if max(intervals) < 0.05:
        print("⚠️  所有 token 间隔 <50ms → 看起来像一次性发完")
    else:
        print("✅ 流式正常")
