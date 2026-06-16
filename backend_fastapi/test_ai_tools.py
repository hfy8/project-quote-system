"""快速测试 7 个 AI 工具"""
import sys
sys.path.insert(0, ".")

from core.services.ai_tools import TOOL_FUNCTIONS

print("=" * 60)
print("测试 7 个 AI 工具")
print("=" * 60)

tests = [
    ("list_modules", {"keyword": "", "limit": 5}, "列所有模块"),
    ("list_modules", {"keyword": "设备", "limit": 5}, "列模块(设备)"),
    ("search_materials", {"keyword": "酒精", "limit": 3}, "搜酒精"),
    ("search_materials", {"keyword": "服务器", "limit": 3}, "搜服务器"),
    ("estimate_labor_hours", {"quotation_id": 15}, "工时估算"),
    ("estimate_labor_hours", {}, "工时估算(无ID)"),
    ("calculate_quotation_cost", {"material_cost": 5000, "labor_hours": 240}, "算总价"),
    ("get_quotation_summary", {"quotation_id": 15}, "报价单摘要"),
    ("get_quotation_compare", {"quotation_id_1": 15, "quotation_id_2": 13}, "报价单对比(15vs13)"),
    ("recommend_materials_for_module", {"module_id": 51, "limit": 5}, "推荐物料(模块51)"),
    ("recommend_materials_for_module", {"module_id": 52, "limit": 5}, "推荐物料(模块52)"),
]

passed = 0
for name, args, desc in tests:
    print(f"\n【{tests.index((name, args, desc)) + 1}】{desc} ({name})")
    try:
        result = TOOL_FUNCTIONS[name](**args)
        if len(str(result)) > 200:
            print(f"  ✅ {str(result)[:200]}...")
        else:
            print(f"  ✅ {result}")
        passed += 1
    except Exception as e:
        print(f"  ❌ {e}")

print(f"\n{'=' * 60}")
print(f"通过 {passed}/{len(tests)}")
