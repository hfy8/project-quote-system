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
        
@tool("recommend_materials_for_module")
def recommend_materials_for_module(module_id: int, limit: int = 10) -> str:
    """根据模块 ID 推荐常用物料（从历史报价中找出现频率最高的物料）

    Args:
        module_id: 模块 ID
        limit: 最多返回几条

    Returns:
        JSON 字符串：[{"material_id": 1, "name": "铝合金板", "avg_qty": 1.5, "usage_count": 5}, ...]
    """
    from core.models.material import ModuleMaterial
    from core.models.material import Material
    from db import db_session_factory
    from sqlalchemy import func

    session = db_session_factory()
    try:
        rows = session.query(
            Material.id,
            Material.name,
            Material.spec,
            Material.unit,
            Material.unit_price,
            func.avg(ModuleMaterial.quantity).label('avg_qty'),
            func.count(ModuleMaterial.id).label('usage_count'),
        ).join(
            ModuleMaterial, ModuleMaterial.material_id == Material.id
        ).filter(
            ModuleMaterial.module_id == module_id,
            Material.status == 'active',
        ).group_by(
            Material.id, Material.name, Material.spec, Material.unit, Material.unit_price
        ).order_by(
            func.count(ModuleMaterial.id).desc()
        ).limit(limit).all()

        return json.dumps([{
            "material_id": r.id,
            "name": r.name,
            "spec": r.spec,
            "unit": r.unit,
            "unit_price": float(r.unit_price) if r.unit_price else 0,
            "avg_quantity": round(float(r.avg_qty), 2),
            "usage_count": r.usage_count,
        } for r in rows], ensure_ascii=False)
    finally:
        session.close()


@tool("list_modules")
def list_modules(keyword: str = "", limit: int = 20) -> str:
    """列出报价单下的模块（可按关键词筛选）

    Args:
        keyword: 模块名关键词（如 "散热"、"机柜"），空字符串返回所有
        limit: 最多返回几条

    Returns:
        JSON 字符串：[{"id": 1, "quotation_id": 15, "name": "散热主体", "code": "M01"}, ...]
    """
    from core.models.module import Module
    from db import db_session_factory

    session = db_session_factory()
    try:
        q = session.query(Module)
        if keyword:
            q = q.filter(Module.name.contains(keyword))
        modules = q.order_by(Module.quotation_id.desc()).limit(limit).all()

        return json.dumps([{
            "id": m.id,
            "quotation_id": m.quotation_id,
            "name": m.name,
            "code": m.code,
            "name_en": m.name_en,
        } for m in modules], ensure_ascii=False)
    finally:
        session.close()


@tool("estimate_labor_hours")
def estimate_labor_hours(quotation_id: int = None) -> str:
    """估算工时（从历史报价单的人工工时数据中算）

    Args:
        quotation_id: 指定报价单 ID（查该单的实际工时）

    Returns:
        JSON 字符串：{"total_hours": 240, "avg_hourly_rate": 100, "source": "..."}
    """
    from core.models.labor_hour import LaborHour
    from db import db_session_factory
    from sqlalchemy import func

    session = db_session_factory()
    try:
        if quotation_id:
            rows = session.query(
                func.sum(LaborHour.hours).label('total_hours'),
                func.avg(LaborHour.unit_price).label('avg_rate'),
            ).filter(
                LaborHour.quotation_id == quotation_id
            ).first()

            if rows and rows.total_hours:
                return json.dumps({
                    "quotation_id": quotation_id,
                    "total_hours": float(rows.total_hours),
                    "avg_hourly_rate": float(rows.avg_rate or 0),
                    "source": f"报价单 #{quotation_id} 实际工时",
                }, ensure_ascii=False)

        # 没指定 ID 或该单没工时，查所有已批准报价单的平均
        rows = session.query(
            func.avg(LaborHour.hours * LaborHour.unit_price).label('avg_total'),
            func.avg(LaborHour.unit_price).label('avg_rate'),
            func.count(LaborHour.id).label('count'),
        ).first()

        return json.dumps({
            "total_hours": 0,
            "avg_hourly_rate": float(rows.avg_rate or 100),
            "sample_count": rows.count or 0,
            "source": "数据库中所有报价单的平均费率（无工时数据）",
        }, ensure_ascii=False)
    finally:
        session.close()


@tool("calculate_quotation_cost")
def calculate_quotation_cost(
    material_cost: float,
    labor_hours: float,
    hourly_rate: float = 100,
    profit_rate: float = 0.15,
    tax_rate: float = 0.13,
) -> str:
    """计算报价单成本（材料 + 工时 + 利润 + 税）

    Args:
        material_cost: 材料总成本（元）
        labor_hours: 工时数
        hourly_rate: 时薪（元/小时，默认 100）
        profit_rate: 利润率（默认 0.15 = 15%）
        tax_rate: 税率（默认 0.13 = 13% 增值税）

    Returns:
        JSON 字符串：{"material_cost": ..., "labor_cost": ..., "subtotal": ..., "profit": ..., "tax": ..., "total": ...}
    """
    material_cost = float(material_cost)
    labor_hours = float(labor_hours)
    labor_cost = labor_hours * hourly_rate
    subtotal = material_cost + labor_cost
    profit = subtotal * profit_rate
    tax = (subtotal + profit) * tax_rate
    total = subtotal + profit + tax

    return json.dumps({
        "material_cost": round(material_cost, 2),
        "labor_hours": labor_hours,
        "hourly_rate": hourly_rate,
        "labor_cost": round(labor_cost, 2),
        "subtotal": round(subtotal, 2),
        "profit_rate": profit_rate,
        "profit": round(profit, 2),
        "tax_rate": tax_rate,
        "tax": round(tax, 2),
        "total": round(total, 2),
    }, ensure_ascii=False)


@tool("get_quotation_compare")
def get_quotation_compare(quotation_id_1: int, quotation_id_2: int) -> str:
    """对比两个报价单的关键指标

    Args:
        quotation_id_1: 报价单 1 ID
        quotation_id_2: 报价单 2 ID

    Returns:
        JSON 字符串：两个报价单的名称、状态、利润、工时、对比差异
    """
    from core.models.quotation import Quotation
    from core.models.labor_hour import LaborHour
    from core.models.module import Module
    from db import db_session_factory
    from sqlalchemy import func

    session = db_session_factory()
    try:
        result = {}
        for qid in [quotation_id_1, quotation_id_2]:
            q = session.query(Quotation).filter_by(id=qid).first()
            if not q:
                result[f"quotation_{qid}"] = {"error": "不存在"}
                continue

            labor = session.query(
                func.sum(LaborHour.hours),
                func.sum(LaborHour.total),
            ).filter(LaborHour.quotation_id == qid).first()

            module_count = session.query(func.count(Module.id)).filter(
                Module.quotation_id == qid
            ).scalar() or 0

            result[f"quotation_{qid}"] = {
                "id": q.id,
                "name": q.name,
                "status": q.status,
                "profit_rate": float(q.profit_rate or 0),
                "total_hours": float(labor[0] or 0),
                "labor_cost": float(labor[1] or 0),
                "module_count": module_count,
                "currency": q.currency,
            }

        # 算差异
        q1 = result.get(f"quotation_{quotation_id_1}", {})
        q2 = result.get(f"quotation_{quotation_id_2}", {})
        if "error" not in q1 and "error" not in q2:
            result["diff"] = {
                "profit_rate_diff": round(q2["profit_rate"] - q1["profit_rate"], 4),
                "total_hours_diff": round(q2["total_hours"] - q1["total_hours"], 2),
                "labor_cost_diff": round(q2["labor_cost"] - q1["labor_cost"], 2),
            }

        return json.dumps(result, ensure_ascii=False)
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
    },
    {
        "type": "function",
        "function": {
            "name": "list_modules",
            "description": "列出报价单的产品组成模块（如 '设备框架'、'PLC模块'、'传送线体'）。模块≠物料，模块是产品组成部分，物料是原材料。当用户问有哪些模块、项目组成、产品拆解时调此工具。可按关键词筛选模块名。",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "模块名关键词，如 '设备'、'PLC'、'传送'，空字符串返回所有"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "最多返回几条，默认 20",
                        "default": 20
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "recommend_materials_for_module",
            "description": "根据模块 ID 推荐常用物料清单。从历史报价中找该模块下出现频率最高的物料，按使用次数排序。",
            "parameters": {
                "type": "object",
                "properties": {
                    "module_id": {
                        "type": "integer",
                        "description": "模块 ID（数字）"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "最多返回几条物料，默认 10",
                        "default": 10
                    }
                },
                "required": ["module_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "estimate_labor_hours",
            "description": "估算工时。可指定报价单 ID 查实际工时，否则返回数据库平均工时费率。",
            "parameters": {
                "type": "object",
                "properties": {
                    "quotation_id": {
                        "type": "integer",
                        "description": "报价单 ID（可选）。提供则查该单实际工时，否则返回平均费率"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_quotation_cost",
            "description": "计算报价单总成本。公式：material_cost + labor_hours*hourly_rate + 利润 + 税。返回各项明细和总价。",
            "parameters": {
                "type": "object",
                "properties": {
                    "material_cost": {
                        "type": "number",
                        "description": "材料总成本（元）"
                    },
                    "labor_hours": {
                        "type": "number",
                        "description": "工时数"
                    },
                    "hourly_rate": {
                        "type": "number",
                        "description": "时薪（元/小时），默认 100",
                        "default": 100
                    },
                    "profit_rate": {
                        "type": "number",
                        "description": "利润率，默认 0.15 = 15%",
                        "default": 0.15
                    },
                    "tax_rate": {
                        "type": "number",
                        "description": "增值税率，默认 0.13 = 13%",
                        "default": 0.13
                    }
                },
                "required": ["material_cost", "labor_hours"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_quotation_compare",
            "description": "对比两个报价单的关键指标（毛利率、工时、模块数等）和差异。",
            "parameters": {
                "type": "object",
                "properties": {
                    "quotation_id_1": {
                        "type": "integer",
                        "description": "报价单 1 ID"
                    },
                    "quotation_id_2": {
                        "type": "integer",
                        "description": "报价单 2 ID"
                    }
                },
                "required": ["quotation_id_1", "quotation_id_2"]
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