import json
from typing import List, Dict, Any
TOOL_FUNCTIONS = {}
def tool(name: str):
    """装饰器：把函数注册到 TOOL_FUNCTIONS"""
    def decorator(func):
        TOOL_FUNCTIONS[name] = func
        return func
    return decorator
    
@tool("search_materials")
def search_materials(keyword: str,limit: int = 5) -> str:
    """在物料库中搜索物料

    Args:
        keyword: 物料名称关键词（如 "铝合金"、"螺丝"）
        limit: 最多返回几条

    Returns:
        JSON 字符串：[{"id": 1, "name": "...", "unit_price": 28.5, ...}, ...]
    """
    from core.models.material import Material  # 延迟导入避免循环
    from db import db_session_factory

    session = db_session_factory()
    try:
        materials = session.query(Material).filter(
            Material.name.contains(keyword)
        ).limit(limit).all()
        print(f"{materials}")
        return json.dumps([{
              "id": m.id,
              "spec": m.spec,            # ← 改这里
              "name": m.name,
              "category": m.category,
              "unit": m.unit,
              "unit_price": float(m.unit_price) if m.unit_price else 0,
        } for m in materials], ensure_ascii=False)
    finally:
        session.close()
@tool("get_quotation_summary")   
def get_quotation_summary(quotation_id: int) -> str:
    """查报价单的摘要信息

    Args:
        quotation_id: 报价单 ID

    Returns:
        JSON 字符串：报价单的名称、状态、总价、毛利率
    """
    from core.models.quotation import Quotation
    from db import db_session_factory

    session = db_session_factory()
    try:
        q = session.query(Quotation).filter_by(id=quotation_id).first()
        if not q:
            return json.dumps({"error": f"报价单 #{quotation_id} 不存在"})

        return json.dumps({
            "id": q.id,
            "name": q.name,
            "type": q.type,
            "status": q.status,
            "scheme_no": q.scheme_no,
            "profit_rate": float(q.profit_rate) if q.profit_rate else 0,
            "currency": q.currency,
        }, ensure_ascii=False)
    finally:
        session.close()
        
# ============== 工具定义（OpenAI 协议格式） ==============
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_materials",
            "description": "在物料库中搜索物料。返回物料的 id、名称、单价、单位等信息。",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "物料名称关键词，如 '铝合金'、'螺丝'、'铝板'"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "最多返回几条结果，默认 5",
                        "default": 5
                    }
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_quotation_summary",
            "description": "根据报价单 ID 查报价单摘要信息（名称、状态、总价、毛利率）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "quotation_id": {
                        "type": "integer",
                        "description": "报价单 ID（数字）"
                    }
                },
                "required": ["quotation_id"]
            }
        }
    }
]

def execute_tool(name: str, arguments: Dict[str, Any]) -> str:
    """根据工具名 + 参数，执行对应的工具函数"""
    func = TOOL_FUNCTIONS.get(name)
    if not func:
        return f"未知工具: {name}"
    return func(**arguments)