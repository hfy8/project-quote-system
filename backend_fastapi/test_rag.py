"""块 4 测试 - RAG 知识库 + 端到端"""
import sys, json
sys.path.insert(0, ".")

from core.services.ai_tools import TOOL_FUNCTIONS
from db import db_session_factory, ModuleBase, engine
from core.models.knowledge import KnowledgeDoc

print("=" * 60)
print("块 4 测试 - RAG 知识库")
print("=" * 60)

# 1. 表已建
print("\n[0] 检查 ai_knowledge_base 表")
ins = engine().dialect.inspector if hasattr(engine(), 'dialect') else None
from sqlalchemy import inspect
ins = inspect(engine())
print(f"   ai_knowledge_base 存在: {ins.has_table('ai_knowledge_base')}")

# 2. 清空 + 种子数据
session = db_session_factory()
session.query(KnowledgeDoc).delete()
session.commit()
session.close()

print("\n[1] 写入种子数据")
seeds = [
    ("报价单审批流程", "报价单需经过业务员填写→主管审核→总经理批准三个步骤。每单需附详细成本明细。", "spec", "审批,流程,报价单"),
    ("毛利率标准", "公司标准毛利率：标准件 15%，定制件 20%，老客户维护单不低于 10%。", "rule", "毛利,标准,利润"),
    ("运输费计费规则", "运输费按体积/重量计费，亚洲航线 50-100 元/kg，欧洲 150-200 元/kg。", "spec", "运输,差旅,费用"),
    ("新客户报价注意", "新客户首单需做信用调查 + 100% 预付款。", "experience", "新客户,风险,经验"),
    ("物料议价技巧", "单笔订单物料 > 1 万元的物料必须找 2 家以上供应商比价。", "faq", "物料,议价,采购"),
    ("差旅费报销", "差旅费凭发票实报实销，每日餐补 100 元/天。", "rule", "差旅,报销"),
    ("报价单作废", "已批准的报价单不可作废，需走变更流程。", "rule", "作废,变更"),
    ("常见问题：毛利为负", "毛利率为负通常是运输费/差旅费算错。检查运输费系数和税率。", "faq", "毛利,负,问题"),
]

session = db_session_factory()
for title, content, doc_type, keywords in seeds:
    doc = KnowledgeDoc(title=title, content=content, doc_type=doc_type, keywords=keywords, created_by="seed")
    session.add(doc)
session.commit()
print(f"   写入 {len(seeds)} 条种子数据")
session.close()

# 3. search_knowledge 测试
print("\n[2] search_knowledge('毛利')")
r = json.loads(TOOL_FUNCTIONS["search_knowledge"]("毛利"))
print(f"   summary: {r['summary']}")
for x in r['results'][:3]:
    print(f"   - [{x['score']}] {x['title']} ({x['doc_type']})")

# 4. search_knowledge 过滤类型
print("\n[3] search_knowledge('运输', doc_type='spec')")
r = json.loads(TOOL_FUNCTIONS["search_knowledge"]("运输", "spec"))
print(f"   summary: {r['summary']}")
for x in r['results']:
    print(f"   - {x['title']}")

# 5. add_knowledge 测试
print("\n[4] add_knowledge")
r = json.loads(TOOL_FUNCTIONS["add_knowledge"]("测试知识", "这是测试内容", "faq", "test,demo"))
print(f"   result: {r}")

# 6. 验证加进去后能搜到
print("\n[5] 再搜 'test'")
r = json.loads(TOOL_FUNCTIONS["search_knowledge"]("test"))
print(f"   summary: {r['summary']}")
for x in r['results']:
    print(f"   - {x['title']}")
