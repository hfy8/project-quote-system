"""AI 黄金集评测脚本

用法:
    python3 tests/ai_eval/run_eval.py                    # 跑全部 10 题
    python3 tests/ai_eval/run_eval.py --ids Q01 Q02     # 跑指定题
    python3 tests/ai_eval/run_eval.py --model both      # 跑两个模型

输出:
    - 控制台彩色报告
    - tests/ai_eval/results/eval_YYYYMMDD_HHMMSS.json
    - tests/ai_eval/results/eval_YYYYMMDD_HHMMSS.md (Markdown 报告)
"""
import sys
import os
import json
import time
import argparse
import requests
from datetime import datetime
from pathlib import Path

# 让 main 能 import
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'backend_fastapi'))

BASE = os.environ.get('PQS_BASE', 'http://localhost:5001')


def load_golden_set():
    with open(ROOT / 'backend_fastapi' / 'tests' / 'ai_eval' / 'golden_set.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def login():
    r = requests.post(f'{BASE}/api/auth/login',
                      json={'username': 'admin', 'password': 'admin123'}, timeout=5)
    r.raise_for_status()
    return r.json()['access_token']


def ask_question(token, question, model='auto', max_wait=60):
    """问 AI 一次，返回 (answer, tool_calls, steps_count, duration_ms)"""
    H = {'Authorization': f'Bearer {token}'}
    body = {
        'query': question,
        'model': model,
    }
    t0 = time.time()
    r = requests.post(f'{BASE}/api/ai/ask', headers=H, json=body, timeout=max_wait)
    dt = (time.time() - t0) * 1000
    if r.status_code != 200:
        return f'[ERROR {r.status_code}] {r.text[:200]}', [], 0, dt
    data = r.json()
    return (
        data.get('answer', ''),
        data.get('tools_used', []),
        data.get('steps', 0),
        dt,
    )


def evaluate_one(token, q, verbose=True):
    """评测单个黄金问题"""
    answer, tool_calls, steps, duration = ask_question(token, q['question'])

    # 评分
    expected_tools = set(q.get('expected_tools', []))
    actual_tools = set(tool_calls)
    tool_hit = expected_tools.issubset(actual_tools) if expected_tools else True

    expected_keywords = q.get('expected_answer_contains', [])
    keyword_hit = all(kw in answer for kw in expected_keywords)

    ok = tool_hit and keyword_hit

    if verbose:
        icon = '✅' if ok else '❌'
        print(f"  {icon} {q['id']} ({q['difficulty']}) {q['category']}")
        print(f"     Q: {q['question']}")
        print(f"     Tools: {tool_calls} (expected ≥{list(expected_tools)})")
        print(f"     Answer: {answer[:150]}{'...' if len(answer)>150 else ''}")
        print(f"     Steps: {steps} | Duration: {duration:.0f}ms")
        if not tool_hit:
            print(f"     ❌ 工具不匹配: 缺 {expected_tools - actual_tools}")
        if not keyword_hit:
            miss = [kw for kw in expected_keywords if kw not in answer]
            print(f"     ❌ 关键词缺失: {miss}")
        print()

    return {
        'id': q['id'],
        'category': q['category'],
        'difficulty': q['difficulty'],
        'question': q['question'],
        'expected_tools': list(expected_tools),
        'actual_tools': tool_calls,
        'expected_keywords': expected_keywords,
        'answer_preview': answer[:200],
        'steps': steps,
        'duration_ms': round(duration, 1),
        'tool_hit': tool_hit,
        'keyword_hit': keyword_hit,
        'ok': ok,
    }


def print_summary(results):
    """打印汇总报告"""
    total = len(results)
    passed = sum(1 for r in results if r['ok'])
    pct = passed / total * 100 if total else 0

    print(f"\n{'='*60}")
    print(f"📊 评测结果: {passed}/{total} 通过 ({pct:.0f}%)")
    print(f"{'='*60}")

    # 按分类
    cats = {}
    for r in results:
        cats.setdefault(r['category'], []).append(r)
    for cat, rs in cats.items():
        ok = sum(1 for r in rs if r['ok'])
        print(f"  {cat}: {ok}/{len(rs)} 通过")

    # 按难度
    diffs = {}
    for r in results:
        diffs.setdefault(r['difficulty'], []).append(r)
    print()
    for d, rs in diffs.items():
        ok = sum(1 for r in rs if r['ok'])
        print(f"  {d}: {ok}/{len(rs)} 通过")

    # 平均耗时
    avg_steps = sum(r['steps'] for r in results) / total if total else 0
    avg_ms = sum(r['duration_ms'] for r in results) / total if total else 0
    print(f"\n  平均步数: {avg_steps:.1f}")
    print(f"  平均耗时: {avg_ms:.0f}ms")


def save_report(results, model):
    """保存报告到文件"""
    out_dir = ROOT / 'backend_fastapi' / 'tests' / 'ai_eval' / 'results'
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    prefix = out_dir / f'eval_{model}_{ts}'

    # JSON
    with open(f'{prefix}.json', 'w', encoding='utf-8') as f:
        json.dump({
            'model': model,
            'timestamp': ts,
            'total': len(results),
            'passed': sum(1 for r in results if r['ok']),
            'results': results,
        }, f, ensure_ascii=False, indent=2)

    # Markdown
    md = [f"# AI 评测报告 ({model})", '', f"时间: {ts}", '', f"通过: {sum(1 for r in results if r['ok'])}/{len(results)}", '']
    md.append('| ID | 分类 | 难度 | 通过 | 工具命中 | 关键词命中 | 步数 | 耗时 |')
    md.append('|----|------|------|------|----------|------------|------|------|')
    for r in results:
        md.append(f"| {r['id']} | {r['category']} | {r['difficulty']} | {'✅' if r['ok'] else '❌'} | "
                  f"{'✅' if r['tool_hit'] else '❌'} | {'✅' if r['keyword_hit'] else '❌'} | "
                  f"{r['steps']} | {r['duration_ms']:.0f}ms |")
    with open(f'{prefix}.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))

    print(f"\n📁 报告: {prefix}.json + .md")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ids', nargs='+', help='只跑指定 ID (e.g. Q01 Q02)')
    parser.add_argument('--model', default='auto', help='auto / minimax / deepseek')
    args = parser.parse_args()

    questions = load_golden_set()
    if args.ids:
        questions = [q for q in questions if q['id'] in args.ids]
        if not questions:
            print(f"❌ 没找到 IDs: {args.ids}")
            return

    print(f"🚀 开始评测 (model={args.model}, {len(questions)} 题)")
    print(f"   Base: {BASE}\n")

    token = login()
    print(f"✅ 登录成功\n")

    results = []
    for q in questions:
        try:
            r = evaluate_one(token, q)
            results.append(r)
        except Exception as e:
            print(f"  ❌ {q['id']} 异常: {e}\n")
            results.append({
                'id': q['id'], 'category': q['category'], 'difficulty': q['difficulty'],
                'ok': False, 'error': str(e),
            })

    print_summary(results)
    save_report(results, args.model)


if __name__ == '__main__':
    main()
