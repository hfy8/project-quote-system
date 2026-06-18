"""端到端测试：登录 + 流式问答（SSE），验证后端发的事件流"""
import requests
import json
import time

BASE = "http://localhost:5001"

# 1. 登录
r = requests.post(f"{BASE}/api/auth/login", json={"username": "admin", "password": "admin123"})
print(f"[1] 登录: {r.status_code}")
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 2. 流式调用（直接 fetch 验证 SSE 事件流）
print(f"\n[2] 流式问答（SSE 验证）...")
query = "物料库有哪些酒精棉片？"
url = f"{BASE}/api/ai/ask/stream"
r = requests.post(url, headers={**headers, "Accept": "text/event-stream"},
                  json={"query": query}, stream=True, timeout=60)
print(f"    HTTP 状态: {r.status_code}, Content-Type: {r.headers.get('Content-Type')}")

event_types = []
tools_used = []
content_parts = []
start_time = time.time()

for raw_line in r.iter_lines(decode_unicode=True):
    if not raw_line:
        continue
    line = raw_line.strip()
    if not line.startswith("data: "):
        continue
    data_str = line[6:]
    try:
        event = json.loads(data_str)
    except json.JSONDecodeError:
        continue
    etype = event.get("type")
    event_types.append(etype)
    if etype == "tool_call":
        tools_used.append(event["name"])
        print(f"    🔧 tool_call: {event['name']} args={event.get('arguments', {})}")
    elif etype == "tool_result":
        result_preview = event.get("result", "")[:80]
        print(f"    ✅ tool_result: {event['name']} → {result_preview}...")
    elif etype == "token":
        content_parts.append(event["content"])
    elif etype == "start":
        print(f"    ▶ start: query='{event.get('query')[:30]}...'")
    elif etype == "done":
        print(f"    ✓ done: steps={event.get('steps')}, tools={event.get('tools_used')}")
    elif etype == "error":
        print(f"    ✗ error: {event.get('message')}")

elapsed = time.time() - start_time
full_content = "".join(content_parts)

print(f"\n    [统计]")
print(f"    事件数: {len(event_types)}")
print(f"    事件类型分布: {dict((t, event_types.count(t)) for t in set(event_types))}")
print(f"    内容长度: {len(full_content)} 字符")
print(f"    耗时: {elapsed:.2f}s")
print(f"    tools_used: {tools_used}")

# 3. 验证 think 块（如果有推理模型）
if "___" in full_content or "思考" in full_content:
    print(f"\n    💭 含 think 块（已渲染为折叠）")
else:
    print(f"\n    [无 think 块（MiniMax-Text-01 可能不输出 think）]")

print(f"\n    内容预览:")
print(f"    {full_content[:200]}")

# 4. 多步测试（应该调 2+ 工具）
print(f"\n[3] 多步推理测试：列模块 + 算成本")
url = f"{BASE}/api/ai/ask/stream"
r = requests.post(url, headers={**headers, "Accept": "text/event-stream"},
                  json={"query": "列出所有模块，再算一个材料 5000 元 240 工时的报价"}, stream=True, timeout=90)
events_step = 0
tools_step = []
for raw_line in r.iter_lines(decode_unicode=True):
    if not raw_line:
        continue
    line = raw_line.strip()
    if not line.startswith("data: "):
        continue
    event = json.loads(line[6:])
    if event.get("type") == "tool_call":
        events_step += 1
        tools_step.append(event["name"])
        print(f"    步骤 {events_step}: {event['name']}")
    elif event.get("type") == "done":
        print(f"    完成: 共 {events_step} 步, tools={event.get('tools_used')}")

print(f"\n✅ SSE 端到端测试完成")
