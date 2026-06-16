"""块 1 工具测试"""
import sys
sys.path.insert(0, ".")

from core.services.ai_tools import TOOL_FUNCTIONS
import json

print("=" * 60)
print("块 1 工具测试 - AI 审计")
print("=" * 60)

# 1. audit_quotation(15) - 报价单 15 应该没问题
r = json.loads(TOOL_FUNCTIONS["audit_quotation"](15))
print(f"\n[1] audit_quotation(15)")
print(f"   报价单: {r.get('quotation_name')}")
print(f"   总结: {r.get('summary')}")
for i in r.get('issues', [])[:3]:
    print(f"   - [{i['severity']}] {i['description']}")

# 2. audit_quotation(16) - 不存在
r = json.loads(TOOL_FUNCTIONS["audit_quotation"](16))
print(f"\n[2] audit_quotation(16) - 不存在")
print(f"   错误: {r.get('error')}")

# 3. audit_materials_price() - 全物料库
r = json.loads(TOOL_FUNCTIONS["audit_materials_price"](""))
print(f"\n[3] audit_materials_price()")
print(f"   总结: {r.get('summary')}")
print(f"   异常数: {len(r.get('outliers', []))}")
for o in r.get('outliers', [])[:3]:
    print(f"   - [{o['severity']}] {o['name']} ¥{o['unit_price']:.0f} ({o['reason']})")

# 4. audit_labor_hours(15) - 单条
r = json.loads(TOOL_FUNCTIONS["audit_labor_hours"](15))
print(f"\n[4] audit_labor_hours(15)")
print(f"   总结: {r.get('summary')}")
print(f"   均值: {r.get('global_avg_hours')}h @ ¥{r.get('global_avg_rate')}")

# 5. audit_labor_hours() - 全部
r = json.loads(TOOL_FUNCTIONS["audit_labor_hours"](None))
print(f"\n[5] audit_labor_hours() - 全部")
print(f"   总结: {r.get('summary')}")
for i in r.get('issues', [])[:3]:
    print(f"   - {i['description']}")
