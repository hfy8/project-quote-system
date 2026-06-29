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
              "name": m.name,
              "spec": m.spec,
              "brand": m.brand,
              "category": m.category,
              "unit": m.unit,
              "unit_price": float(m.unit_price) if m.unit_price else 0,
              "param1": m.param1,
              "param2": m.param2,
              "param3": m.param3,
        } for m in materials], ensure_ascii=False)
    finally:
        session.close()
@tool("get_quotation_summary")
def get_quotation_summary(quotation_id: int) -> str:
    """查报价单的摘要信息

    Args:
        quotation_id: 报价单 ID

    Returns:
        JSON 字符串：报价单的名称、状态、对外利润率、币种

    注意：profit_rate 字段是「对外利润率」（= 利润 / 成本），不是「毛利率」。
    用户问"毛利率"时调 analyze_profitability_detail，不要用本工具的 profit_rate 字段。
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
            Material.brand,
            Material.unit,
            Material.unit_price,
            Material.param1,
            Material.param2,
            Material.param3,
            func.avg(ModuleMaterial.quantity).label('avg_qty'),
            func.count(ModuleMaterial.id).label('usage_count'),
        ).join(
            ModuleMaterial, ModuleMaterial.material_id == Material.id
        ).filter(
            ModuleMaterial.module_id == module_id,
            Material.status == 'active',
        ).group_by(
            Material.id, Material.name, Material.spec, Material.brand, Material.unit, Material.unit_price,
            Material.param1, Material.param2, Material.param3
        ).order_by(
            func.count(ModuleMaterial.id).desc()
        ).limit(limit).all()

        return json.dumps([{
            "material_id": r.id,
            "name": r.name,
            "spec": r.spec,
            "brand": r.brand,
            "unit": r.unit,
            "unit_price": float(r.unit_price) if r.unit_price else 0,
            "param1": r.param1,
            "param2": r.param2,
            "param3": r.param3,
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


# ============== 块 1：AI 审计 ==============
@tool("audit_quotation")
def audit_quotation(quotation_id: int) -> str:
    """审计单个报价单的所有异常（物料价格、工时、毛利率、字段完整性）

    Args:
        quotation_id: 报价单 ID

    Returns:
        JSON 字符串：{"quotation_id": 15, "issues": [{"type": "...", "severity": "high/medium/low", "description": "..."}], "summary": "..."}
    """
    from core.models.quotation import Quotation
    from core.models.labor_hour import LaborHour
    from core.models.module import Module
    from core.models.material import ModuleMaterial, Material
    from db import db_session_factory
    from sqlalchemy import func

    session = db_session_factory()
    try:
        issues = []

        q = session.query(Quotation).filter_by(id=quotation_id).first()
        if not q:
            return json.dumps({"error": f"报价单 #{quotation_id} 不存在"})

        # 1. 字段完整性（注意：profit_rate 字段是「对外利润率」不是「毛利率」）
        if q.profit_rate is None or q.profit_rate == 0:
            issues.append({
                "type": "missing_profit_rate",
                "severity": "high",
                "description": "对外利润率未填写或为 0",
            })
        if q.profit_rate is not None and q.profit_rate < 0:
            issues.append({
                "type": "negative_profit",
                "severity": "high",
                "description": f"对外利润率为负数: {q.profit_rate * 100:.1f}%",
            })
        if q.profit_rate is not None and q.profit_rate > 0.5:
            issues.append({
                "type": "high_profit_warning",
                "severity": "medium",
                "description": f"对外利润率过高: {q.profit_rate * 100:.1f}%，可能算错（一般 < 30%）",
            })

        # 2. 工时合理性（统计异常）
        labor_stats = session.query(
            func.avg(LaborHour.hours).label('avg_hours'),
            func.stddev(LaborHour.hours).label('std_hours'),
            func.count(LaborHour.id).label('count'),
        ).first()

        labor_data = session.query(
            func.sum(LaborHour.hours),
            func.sum(LaborHour.total),
        ).filter(LaborHour.quotation_id == quotation_id).first()

        if labor_data[0]:
            total_hours = float(labor_data[0])
            if labor_stats.avg_hours and labor_stats.std_hours:
                avg = float(labor_stats.avg_hours)
                std = float(labor_stats.std_hours)
                if std > 0 and abs(total_hours - avg) > 3 * std:
                    issues.append({
                        "type": "abnormal_labor_hours",
                        "severity": "high",
                        "description": f"工时 {total_hours:.0f}h 异常（平均 {avg:.0f}h ± {std:.0f}h）",
                    })
            if total_hours == 0 and q.status == "approved":
                issues.append({
                    "type": "missing_labor_data",
                    "severity": "medium",
                    "description": "已批准报价单没有工时数据",
                })

        # 3. 模块数 / 物料数检查
        module_count = session.query(func.count(Module.id)).filter(
            Module.quotation_id == quotation_id
        ).scalar() or 0
        if module_count == 0:
            issues.append({
                "type": "no_modules",
                "severity": "high",
                "description": "报价单没有任何模块",
            })

        material_count = session.query(func.count(ModuleMaterial.id)).join(
            Module, Module.id == ModuleMaterial.module_id
        ).filter(Module.quotation_id == quotation_id).scalar() or 0
        if module_count > 0 and material_count == 0:
            issues.append({
                "type": "no_materials",
                "severity": "high",
                "description": f"{module_count} 个模块都没有物料",
            })

        # 4. 物料价格异常
        material_prices = session.query(
            Material.unit_price, Material.name, Material.id
        ).join(
            ModuleMaterial, ModuleMaterial.material_id == Material.id
        ).join(
            Module, Module.id == ModuleMaterial.module_id
        ).filter(
            Module.quotation_id == quotation_id,
            Material.unit_price > 0,
        ).all()

        # 用 IQR 方法检测价格异常
        if len(material_prices) >= 4:
            prices = sorted([float(m.unit_price) for m in material_prices])
            n = len(prices)
            q1 = prices[n // 4]
            q3 = prices[3 * n // 4]
            iqr = q3 - q1
            upper = q3 + 1.5 * iqr
            lower = max(0, q1 - 1.5 * iqr)
            for m in material_prices:
                price = float(m.unit_price)
                if price > upper:
                    issues.append({
                        "type": "material_price_outlier_high",
                        "severity": "medium",
                        "description": f"物料 '{m.name}' 单价 ¥{price:.0f} 异常高（同模块其他物料最高 ¥{q3:.0f}）",
                    })
                elif price < lower and price > 0:
                    issues.append({
                        "type": "material_price_outlier_low",
                        "severity": "low",
                        "description": f"物料 '{m.name}' 单价 ¥{price:.0f} 异常低（同模块其他物料最低 ¥{q1:.0f}）",
                    })

        # 总结
        severity_count = {"high": 0, "medium": 0, "low": 0}
        for i in issues:
            severity_count[i["severity"]] = severity_count.get(i["severity"], 0) + 1

        if not issues:
            summary = "✅ 无异常"
        else:
            summary = f"发现 {len(issues)} 个问题（高: {severity_count['high']}, 中: {severity_count['medium']}, 低: {severity_count['low']}）"

        return json.dumps({
            "quotation_id": quotation_id,
            "quotation_name": q.name,
            "issues": issues,
            "summary": summary,
        }, ensure_ascii=False)
    finally:
        session.close()


@tool("audit_materials_price")
def audit_materials_price(category: str = "") -> str:
    """审计物料库中所有异常价格的物料（按类别筛选）

    Args:
        category: 可选类别（'大件'/'核心部件'/'其他件'），空字符串审计全部

    Returns:
        JSON 字符串：{"outliers": [...], "summary": "..."}
    """
    from core.models.material import Material
    from db import db_session_factory

    session = db_session_factory()
    try:
        q = session.query(Material).filter(
            Material.status == "active",
            Material.unit_price.isnot(None),
            Material.unit_price > 0,
        )
        if category:
            q = q.filter(Material.category == category)
        materials = q.all()

        if len(materials) < 4:
            return json.dumps({"outliers": [], "summary": "样本不足，无法审计"})

        # 按 category 分组做 IQR
        groups = {}
        for m in materials:
            cat = m.category or "未知"
            groups.setdefault(cat, []).append(m)

        outliers = []
        for cat, items in groups.items():
            if len(items) < 4:
                continue
            prices = sorted([float(m.unit_price) for m in items])
            n = len(prices)
            q1 = prices[n // 4]
            q3 = prices[3 * n // 4]
            iqr = q3 - q1
            upper = q3 + 1.5 * iqr
            lower = max(0, q1 - 1.5 * iqr)
            for m in items:
                price = float(m.unit_price)
                if price > upper:
                    outliers.append({
                        "material_id": m.id,
                        "name": m.name,
                        "category": cat,
                        "unit_price": price,
                        "reason": f"价格高于本类上限 ¥{upper:.0f}",
                        "severity": "medium",
                    })
                elif price < lower and price > 0:
                    outliers.append({
                        "material_id": m.id,
                        "name": m.name,
                        "category": cat,
                        "unit_price": price,
                        "reason": f"价格低于本类下限 ¥{lower:.0f}",
                        "severity": "low",
                    })

        return json.dumps({
            "outliers": outliers,
            "summary": f"扫描 {len(materials)} 条物料，发现 {len(outliers)} 个价格异常",
        }, ensure_ascii=False)
    finally:
        session.close()


@tool("audit_labor_hours")
def audit_labor_hours(quotation_id: int = None) -> str:
    """审计工时数据（单条或全部）

    Args:
        quotation_id: 指定报价单 ID（查该单）；空字符串则审计所有报价单

    Returns:
        JSON 字符串：{"issues": [...], "summary": "..."}
    """
    from core.models.labor_hour import LaborHour
    from core.models.quotation import Quotation
    from db import db_session_factory
    from sqlalchemy import func

    session = db_session_factory()
    try:
        # 1. 算全局均值和标准差
        stats = session.query(
            func.avg(LaborHour.hours).label('avg'),
            func.stddev(LaborHour.hours).label('std'),
            func.avg(LaborHour.unit_price).label('avg_rate'),
            func.count(LaborHour.id).label('count'),
        ).first()

        if not stats.avg or stats.count < 3:
            return json.dumps({"issues": [], "summary": "工时数据不足，无法审计"})

        avg = float(stats.avg)
        std = float(stats.std or 0)
        avg_rate = float(stats.avg_rate)

        issues = []

        if quotation_id:
            # 审计单条
            data = session.query(
                func.sum(LaborHour.hours),
                func.avg(LaborHour.unit_price),
            ).filter(LaborHour.quotation_id == quotation_id).first()

            if data[0] is None:
                return json.dumps({
                    "issues": [{"type": "no_labor_data", "severity": "high", "description": f"报价单 #{quotation_id} 没有工时数据"}],
                    "summary": f"报价单 #{quotation_id} 无工时",
                })

            total_hours = float(data[0])
            rate = float(data[1] or 0)

            if std > 0 and abs(total_hours - avg) > 3 * std:
                issues.append({
                    "type": "abnormal_hours",
                    "severity": "high",
                    "description": f"工时 {total_hours:.0f}h 异常（全局均值 {avg:.0f}h ± {std:.0f}h）",
                })
            if rate > 0 and abs(rate - avg_rate) / avg_rate > 0.5:
                issues.append({
                    "type": "abnormal_rate",
                    "severity": "medium",
                    "description": f"时薪 ¥{rate:.0f} 与均值 ¥{avg_rate:.0f} 偏差 {abs(rate - avg_rate) / avg_rate * 100:.0f}%",
                })
        else:
            # 审计所有 - 找异常工时
            all_labor = session.query(
                LaborHour.quotation_id,
                Quotation.name,
                func.sum(LaborHour.hours).label('total_hours'),
            ).join(Quotation, Quotation.id == LaborHour.quotation_id).group_by(
                LaborHour.quotation_id, Quotation.name
            ).all()

            for row in all_labor:
                hours = float(row.total_hours)
                if std > 0 and abs(hours - avg) > 3 * std:
                    issues.append({
                        "type": "abnormal_hours",
                        "quotation_id": row.quotation_id,
                        "quotation_name": row.name,
                        "severity": "high",
                        "description": f"工时 {hours:.0f}h 异常（均值 {avg:.0f}h ± {std:.0f}h）",
                    })

        return json.dumps({
            "issues": issues,
            "global_avg_hours": round(avg, 1),
            "global_avg_rate": round(avg_rate, 1),
            "summary": f"扫描 {stats.count} 条工时记录，发现 {len(issues)} 个异常" if not quotation_id else f"报价单 #{quotation_id} 审计：{len(issues)} 个问题",
        }, ensure_ascii=False)
    finally:
        session.close()


# ============== 块 2：AI 业务分析 ==============
@tool("analyze_profitability")
def analyze_profitability(limit: int = 5) -> str:
    """分析报价单的对外利润率分布、Top/Bottom 排名、统计概览

    注意：返的是「对外利润率」（profit_rate 字段）不是「毛利率」。
    如要看毛利率（含税前/后），用 analyze_profitability_detail 工具（单张）或算 gross_margin = profit_rate / (1 + profit_rate)。

    Args:
        limit: 返回 Top/Bottom 几个，默认 5

    Returns:
        JSON 字符串：{"overview": {...}, "top": [...], "bottom": [...], "insights": [...]}
    """
    from core.models.quotation import Quotation
    from db import db_session_factory
    from sqlalchemy import func, desc, asc

    session = db_session_factory()
    try:
        # 1. 全局概览
        overall = session.query(
            func.count(Quotation.id).label('count'),
            func.avg(Quotation.profit_rate).label('avg_profit'),
            func.max(Quotation.profit_rate).label('max_profit'),
            func.min(Quotation.profit_rate).label('min_profit'),
        ).filter(Quotation.profit_rate.isnot(None)).first()

        # 2. 按状态分组
        by_status = session.query(
            Quotation.status,
            func.count(Quotation.id).label('count'),
            func.avg(Quotation.profit_rate).label('avg_profit'),
        ).filter(Quotation.profit_rate.isnot(None)).group_by(Quotation.status).all()

        # 3. Top N 最高毛利
        top_rows = session.query(
            Quotation.id, Quotation.name, Quotation.profit_rate, Quotation.status
        ).filter(Quotation.profit_rate.isnot(None)).order_by(
            desc(Quotation.profit_rate)
        ).limit(limit).all()

        # 4. Bottom N 最低毛利
        bottom_rows = session.query(
            Quotation.id, Quotation.name, Quotation.profit_rate, Quotation.status
        ).filter(Quotation.profit_rate.isnot(None)).order_by(
            asc(Quotation.profit_rate)
        ).limit(limit).all()

        # 5. 自动洞察
        insights = []
        if overall.avg_profit is not None:
            avg_pct = float(overall.avg_profit) * 100
            insights.append(f"整体平均对外利润率 {avg_pct:.1f}%，共 {overall.count} 单有效数据")
            if overall.max_profit and overall.min_profit:
                spread = (overall.max_profit - overall.min_profit) * 100
                if spread > 30:
                    insights.append(f"对外利润率差异大（{spread:.0f} 个百分点），需关注低利润率报价单")

        # 6. 按状态明细
        status_breakdown = []
        for s in by_status:
            status_breakdown.append({
                "status": s.status or "未知",
                "count": s.count,
                "avg_profit_rate": round(float(s.avg_profit or 0) * 100, 1),
            })

        return json.dumps({
            "overview": {
                "total_quotations": overall.count or 0,
                "avg_profit_rate": round(float(overall.avg_profit or 0) * 100, 1),
                "max_profit_rate": round(float(overall.max_profit or 0) * 100, 1),
                "min_profit_rate": round(float(overall.min_profit or 0) * 100, 1),
            },
            "status_breakdown": status_breakdown,
            "top": [{
                "id": r.id, "name": r.name,
                "profit_rate": round(float(r.profit_rate) * 100, 1),
                "status": r.status,
            } for r in top_rows],
            "bottom": [{
                "id": r.id, "name": r.name,
                "profit_rate": round(float(r.profit_rate) * 100, 1),
                "status": r.status,
            } for r in bottom_rows],
            "insights": insights,
        }, ensure_ascii=False)
    finally:
        session.close()


@tool("analyze_hardware_ratio")
def analyze_hardware_ratio(quotation_id: int) -> str:
    """分析报价单中"硬件"（物料）成本占总报价的占比。

    计算逻辑：
    - 分子 = 物料×系数后的小计（即 material_total_with_rates，含 large/standard/other 各自的报价系数）
    - 分母 = 最终报价 grand_total（含物料×系数+工时+差旅+包装+其他费用+利润+税）
    - 同时按物料 category 拆解：standard / large / other 各自乘系数后的占比

    当用户问"硬件占比"、"物料占比"、"成本结构"时调此工具。
    """
    from core.models.quotation import Quotation
    from core.models.version import VersionSnapshot
    from core.services.export_service import get_version_snapshot_data, calculate_version_totals
    from db import db_session_factory
    from sqlalchemy import func as sa_func
    session = db_session_factory()
    try:
        q = session.query(Quotation).get(quotation_id)
        if not q:
            return json.dumps({"error": f"报价单 #{quotation_id} 不存在"}, ensure_ascii=False)

        # 1. 加载最新版本快照（含系数 + 完整模块/费用/工时/差旅）
        latest_version_no = session.query(sa_func.max(VersionSnapshot.version_no)).filter_by(
            quotation_id=q.id
        ).scalar()
        if not latest_version_no:
            return json.dumps({"error": f"报价单 #{quotation_id} 还没有版本快照"}, ensure_ascii=False)
        snapshot_data = get_version_snapshot_data(q.id, latest_version_no)

        # 2. 用现有算法算汇总（grand_total / material_with_rates / 各项费用 / 利润 / 税）
        totals = calculate_version_totals(snapshot_data)
        material_with_rates = float(totals.get("material_total_with_rates", 0))
        grand_total = float(totals.get("grand_total", 0))
        material_raw = float(totals.get("material_total", 0))
        fees_total = float(totals.get("fees_total", 0))
        labor_total = float(totals.get("labor_total", 0))
        profit_amount = float(totals.get("profit_amount", 0))
        tax_amount = float(totals.get("tax_amount", 0))
        fee_rates = totals.get("fee_rates", {}) or {}
        category_totals = {"large": 0.0, "standard": 0.0, "other": 0.0}

        # 3. 按 category 算占比（用系数后的小计）
        for module in snapshot_data.get("modules", []):
            for mm in module.get("materials", []):
                is_other = mm.get("is_other", False)
                if is_other:
                    up = float(mm.get("unit_price_override", 0) or 0)
                    if up == 0:
                        up = float(mm.get("unit_price", 0) or 0)
                else:
                    up = float(mm.get("unit_price", 0) or 0)
                qty = float(mm.get("quantity", 0) or 0)
                amount = up * qty
                cat = mm.get("category", "standard")
                if cat not in ("large", "standard"):
                    cat = "other"
                category_totals[cat] = category_totals.get(cat, 0) + amount

        # 4. 占比（物料×系数后 / 最终报价）
        ratio = material_with_rates / grand_total if grand_total > 0 else 0
        # 4.1 物料内部各 category 占比（基于物料×系数后）
        category_ratio_in_material = {
            cat: (category_totals[cat] * fee_rates.get(cat, 1.0) / material_with_rates)
            if material_with_rates > 0 else 0
            for cat in ("large", "standard", "other")
        }
        # 4.2 每个 category 在最终报价里的占比
        category_ratio_in_total = {
            cat: (category_totals[cat] * fee_rates.get(cat, 1.0) / grand_total)
            if grand_total > 0 else 0
            for cat in ("large", "standard", "other")
        }

        return json.dumps({
            "quotation_id": q.id,
            "quotation_name": q.name,
            "scheme_no": q.scheme_no,
            "currency": q.currency or "CNY",
            "分子说明": "物料×报价系数后的小计（material_total_with_rates）",
            "分母说明": "最终报价 grand_total（含物料×系数+工时+差旅+包装+其他费用+利润+税）",
            "coefficients": fee_rates,
            "material_raw_total": round(material_raw, 2),
            "material_with_rates": round(material_with_rates, 2),
            "grand_total": round(grand_total, 2),
            "hardware_ratio": round(ratio, 4),
            "hardware_ratio_pct": f"{ratio * 100:.1f}%",
            # 拆解
            "material_by_category_raw": {k: round(v, 2) for k, v in category_totals.items()},
            "category_ratio_in_material": {k: round(v, 4) for k, v in category_ratio_in_material.items()},
            "category_ratio_in_total": {k: round(v, 4) for k, v in category_ratio_in_total.items()},
            # 成本项参考
            "fees_total": round(fees_total, 2),
            "labor_total": round(labor_total, 2),
            "profit_amount": round(profit_amount, 2),
            "tax_amount": round(tax_amount, 2),
            "profit_rate": float(q.profit_rate or 0),
            "tax_rate": float(q.tax_rate or 0.13),
        }, ensure_ascii=False)
    finally:
        session.close()


@tool("get_quotation_gross_margin")
def get_quotation_gross_margin(quotation_id: int) -> str:
    """【用户问「毛利率/实际毛利率/销售毛利率」时调这个工具】

    报价单的「实际毛利率」= 销售视角的利润率 = 利润 / 销售价。

    ⚠️ 重要概念区分（不要搞混）：
    - **对外利润率**（profit_rate 字段）：成本上加的利润率。例 15% 表示「成本 100 元，加 15 元利润」
    - **毛利率**（用户业务上说的）：销售价中的利润占比。例 13% 表示「销售 100 元，13 元是利润」
    - 这两个数字**不一样**！毛利率 < 对外利润率

    返回三种数字：
    - 对外利润率（如 15%）— 来自 DB 字段
    - 销售毛利率（不含税）= 利润 / 不含税销售价（如 13.04%）
    - 含税毛利率 = 利润 / 含税总价（如 11.54%）

    用户问"毛利率"时优先用「销售毛利率（不含税）」。
    用户问"含税毛利率"时用「含税毛利率」。

    Args:
        quotation_id: 报价单 ID

    Returns:
        JSON 字符串：成本、利润、销售价、税额、对/含税毛利率
    """
    from core.models.quotation import Quotation
    from core.models.version import VersionSnapshot
    from core.services.export_service import get_version_snapshot_data, calculate_version_totals
    from db import db_session_factory
    from sqlalchemy import func as sa_func

    session = db_session_factory()
    try:
        q = session.query(Quotation).get(quotation_id)
        if not q:
            return json.dumps({"error": f"报价单 #{quotation_id} 不存在"}, ensure_ascii=False)

        # 必须有版本快照才能算汇总
        latest_version_no = session.query(sa_func.max(VersionSnapshot.version_no)).filter_by(
            quotation_id=q.id
        ).scalar()
        if not latest_version_no:
            return json.dumps({"error": f"报价单 #{quotation_id} 还没有版本快照，无法计算毛利率"}, ensure_ascii=False)

        snapshot_data = get_version_snapshot_data(q.id, latest_version_no)
        totals = calculate_version_totals(snapshot_data)

        # 取出所有相关金额
        cost = float(totals.get("subtotal", 0))                # 成本（物料×系数 + 费用 + 工时）
        profit = float(totals.get("profit_amount", 0))         # 利润
        sales_excl_tax = float(totals.get("subtotal_with_profit", 0))  # 销售价（不含税）
        tax = float(totals.get("tax_amount", 0))                # 税额
        grand = float(totals.get("grand_total", 0))            # 含税总价
        profit_rate = float(totals.get("profit_rate", 0) or 0) # 对外利润率
        tax_rate = float(totals.get("tax_rate", 0) or 0.13)    # 税率

        # 算两种毛利率
        gross_margin_excl_tax = profit / sales_excl_tax if sales_excl_tax > 0 else 0
        gross_margin_incl_tax = profit / grand if grand > 0 else 0

        return json.dumps({
            "quotation_id": q.id,
            "quotation_name": q.name,
            "scheme_no": q.scheme_no,
            "currency": q.currency or "CNY",
            "version_no": latest_version_no,

            # 概念解释（避免 LLM 搞混）
            "对外利润率": profit_rate,                  # DB 字段，cost × profit_rate = profit
            "对外利润率_pct": f"{profit_rate * 100:.2f}%",

            "销售毛利率": gross_margin_excl_tax,        # 用户问"毛利率"时优先用这个
            "销售毛利率_pct": f"{gross_margin_excl_tax * 100:.2f}%",

            "含税毛利率": gross_margin_incl_tax,         # 用户问"含税毛利率"时用这个
            "含税毛利率_pct": f"{gross_margin_incl_tax * 100:.2f}%",

            # 金额明细（让 LLM 能验证）
            "成本": round(cost, 2),
            "利润": round(profit, 2),
            "销售价(不含税)": round(sales_excl_tax, 2),
            "税额": round(tax, 2),
            "含税总价": round(grand, 2),
            "税率": tax_rate,
        }, ensure_ascii=False)
    finally:
        session.close()


@tool("analyze_trends")
def analyze_trends(months: int = 6) -> str:
    """分析最近 N 个月报价单的趋势（数量、毛利率、工时）

    Args:
        months: 最近几个月，默认 6

    Returns:
        JSON 字符串：{"trends": [{"period": "2026-01", "count": 5, "avg_profit": 0.15, "total_hours": 800}, ...], "insights": [...]}
    """
    from core.models.quotation import Quotation
    from core.models.labor_hour import LaborHour
    from db import db_session_factory
    from sqlalchemy import func

    session = db_session_factory()
    try:
        # 查所有报价单，按 created_at 分组
        rows = session.query(
            Quotation.id,
            Quotation.name,
            Quotation.profit_rate,
            Quotation.status,
        ).order_by(Quotation.id.asc()).all()

        # 用 quotation.id 大致代表时间顺序（id 越大越新）
        # 取最近 N*3 条数据（每月可能多单）
        recent = rows[-months * 5:] if len(rows) > months * 5 else rows

        # 按区间分桶
        bucket_size = max(1, len(recent) // months)
        trends = []
        for i in range(0, len(recent), bucket_size):
            chunk = recent[i:i + bucket_size]
            if not chunk:
                continue
            period_label = f"区间 {len(trends) + 1}"
            profits = [float(q.profit_rate) for q in chunk if q.profit_rate is not None]

            # 该区间的总工时
            qids = [q.id for q in chunk]
            total_hours = session.query(
                func.coalesce(func.sum(LaborHour.hours), 0)
            ).filter(LaborHour.quotation_id.in_(qids)).scalar() or 0

            trends.append({
                "period": period_label,
                "quotation_count": len(chunk),
                "avg_profit_rate": round(sum(profits) / len(profits) * 100, 1) if profits else 0,
                "total_hours": float(total_hours),
            })

        # 自动洞察
        insights = []
        if len(trends) >= 2:
            latest = trends[-1]["avg_profit_rate"]
            earliest = trends[0]["avg_profit_rate"]
            if latest > earliest * 1.1:
                insights.append(f"毛利率上升 {latest - earliest:.1f} 个百分点")
            elif latest < earliest * 0.9:
                insights.append(f"毛利率下降 {earliest - latest:.1f} 个百分点，需关注")
            else:
                insights.append("毛利率保持稳定")

        return json.dumps({
            "trends": trends,
            "insights": insights,
            "summary": f"分析了 {len(recent)} 条报价单，划分 {len(trends)} 个区间",
        }, ensure_ascii=False)
    finally:
        session.close()


# ============== 块 3：AI 报价调整模拟 ==============
@tool("simulate_quotation_change")
def simulate_quotation_change(quotation_id: int, discount_rate: float = 0.0, target_profit_rate: float = None) -> str:
    """模拟报价单调整（降价/目标毛利率）后需要怎么改才能达成目标

    Args:
        quotation_id: 报价单 ID
        discount_rate: 客户要求的降价幅度（如 0.05 = 5%）
        target_profit_rate: 目标毛利率（如 0.15 = 15%），不传则按当前保持

    Returns:
        JSON 字符串：{"current": {...}, "scenario": {...}, "adjustments": [...]}
    """
    from core.models.quotation import Quotation
    from core.models.labor_hour import LaborHour
    from core.models.module import Module
    from core.models.material import ModuleMaterial, Material
    from db import db_session_factory
    from sqlalchemy import func

    session = db_session_factory()
    try:
        q = session.query(Quotation).filter_by(id=quotation_id).first()
        if not q:
            return json.dumps({"error": f"报价单 #{quotation_id} 不存在"})

        # 1. 算当前成本
        material_data = session.query(
            func.coalesce(func.sum(ModuleMaterial.quantity * Material.unit_price), 0).label('material_cost'),
            func.coalesce(func.sum(LaborHour.total), 0).label('labor_cost'),
        ).select_from(Module).outerjoin(
            ModuleMaterial, ModuleMaterial.module_id == Module.id
        ).outerjoin(
            Material, Material.id == ModuleMaterial.material_id
        ).outerjoin(
            LaborHour, LaborHour.quotation_id == Module.quotation_id
        ).filter(
            Module.quotation_id == quotation_id
        ).first()

        material_cost = float(material_data.material_cost or 0)
        labor_cost = float(material_data.labor_cost or 0)
        subtotal = material_cost + labor_cost
        current_profit = float(q.profit_rate or 0)
        current_total = subtotal * (1 + current_profit) * 1.13  # 13% 税

        # 2. 应用客户降价
        new_subtotal = subtotal * (1 - discount_rate)

        # 3. 算保持原毛利需要的压缩
        if target_profit_rate is None:
            target_profit_rate = current_profit

        # 目标总价 = new_subtotal * (1 + target_profit_rate)
        # 现在实际总价（未降价）= subtotal * (1 + current_profit) * 1.13
        # 差额 = new_total - actual_total
        target_total = new_subtotal * (1 + target_profit_rate) * 1.13
        actual_total_no_discount = current_total
        diff = target_total - actual_total_no_discount

        # 4. 找可压缩的成本（列出最大的物料，按金额降序）
        big_materials = session.query(
            Material.id, Material.name, Material.unit_price,
            ModuleMaterial.quantity,
            (ModuleMaterial.quantity * Material.unit_price).label('total'),
        ).join(
            Module, Module.id == ModuleMaterial.module_id
        ).join(
            Material, Material.id == ModuleMaterial.material_id
        ).filter(
            Module.quotation_id == quotation_id,
        ).order_by(
            (ModuleMaterial.quantity * Material.unit_price).desc()
        ).limit(5).all()

        adjustments = []
        if diff < 0:
            # 缺钱 - 需要砍成本
            need_save = -diff
            adjustments.append({
                "type": "reduce_cost",
                "amount_needed": round(need_save, 2),
                "suggestion": f"需要压缩 ¥{need_save:.0f} 成本来保持 {target_profit_rate * 100:.1f}% 毛利率",
            })
            for m in big_materials[:3]:
                adjustments.append({
                    "type": "consider_renegotiate",
                    "material_id": m.id,
                    "name": m.name,
                    "current_cost": round(float(m.total), 2),
                    "hint": f"占总成本 {float(m.total) / subtotal * 100 if subtotal else 0:.0f}%，可议价",
                })
        else:
            adjustments.append({
                "type": "achievable",
                "amount_saved": round(diff, 2),
                "suggestion": f"降价 {discount_rate * 100:.0f}% 后仍有 ¥{diff:.0f} 利润空间",
            })

        return json.dumps({
            "quotation_id": quotation_id,
            "current": {
                "material_cost": round(material_cost, 2),
                "labor_cost": round(labor_cost, 2),
                "subtotal": round(subtotal, 2),
                "profit_rate": round(current_profit * 100, 1),
                "total_with_tax": round(current_total, 2),
            },
            "scenario": {
                "discount_rate": round(discount_rate * 100, 1),
                "target_profit_rate": round(target_profit_rate * 100, 1),
                "new_subtotal": round(new_subtotal, 2),
                "new_total_with_tax": round(target_total, 2),
            },
            "adjustments": adjustments,
        }, ensure_ascii=False)
    finally:
        session.close()


# ============== 块 4：RAG 知识库 ==============
@tool("search_knowledge")
def search_knowledge(query: str, doc_type: str = "", limit: int = 5) -> str:
    """在知识库中搜索相关业务知识（业务规范/FAQ/历史经验）

    Args:
        query: 搜索关键词
        doc_type: 可选文档类型（spec/faq/experience/rule），空字符串搜全部
        limit: 最多返回几条，默认 5

    Returns:
        JSON 字符串：{"results": [{"id": ..., "title": "...", "content": "...", "score": ...}], "summary": "..."}
    """
    from core.models.knowledge import KnowledgeDoc
    from db import db_session_factory

    session = db_session_factory()
    try:
        if not query:
            return json.dumps({"results": [], "summary": "搜索关键词不能为空"})

        # 关键词拆分（空格/逗号）
        keywords = [k for k in query.replace(',', ' ').split() if k]

        # 简单关键词匹配打分
        docs = session.query(KnowledgeDoc).all()
        if doc_type:
            docs = [d for d in docs if d.doc_type == doc_type]

        scored = []
        for d in docs:
            score = 0
            text = (d.title or '') + ' ' + (d.content or '') + ' ' + (d.keywords or '')
            for kw in keywords:
                if kw in d.title:
                    score += 10
                if kw in d.content:
                    score += 3
                if kw in (d.keywords or ''):
                    score += 5
            if score > 0:
                scored.append((score, d))

        scored.sort(key=lambda x: -x[0])
        scored = scored[:limit]

        results = [{
            "id": d.id,
            "title": d.title,
            "content": d.content[:500],  # 截断
            "doc_type": d.doc_type,
            "score": s,
        } for s, d in scored]

        return json.dumps({
            "results": results,
            "summary": f"找到 {len(results)} 条相关知识（搜 '{query}'）",
        }, ensure_ascii=False)
    finally:
        session.close()


@tool("add_knowledge")
def add_knowledge(title: str, content: str, doc_type: str = "faq", keywords: str = "", created_by: str = "ai_user") -> str:
    """添加一条知识到知识库

    Args:
        title: 标题
        content: 内容
        doc_type: 类型（spec=规范/faq=常见问题/experience=经验/rule=规则）
        keywords: 关键词（逗号分隔）
        created_by: 创建者

    Returns:
        JSON 字符串：{"id": ..., "title": "...", "status": "ok"}
    """
    from core.models.knowledge import KnowledgeDoc
    from db import db_session_factory

    session = db_session_factory()
    try:
        doc = KnowledgeDoc(
            title=title,
            content=content,
            doc_type=doc_type,
            keywords=keywords,
            created_by=created_by,
        )
        session.add(doc)
        session.commit()
        return json.dumps({
            "id": doc.id,
            "title": doc.title,
            "status": "ok",
        }, ensure_ascii=False)
    except Exception as e:
        session.rollback()
        return json.dumps({"error": str(e), "status": "failed"})
    finally:
        session.close()


# ============== 块 4b：RAG v2 向量混合检索 ==============
@tool("search_knowledge_hybrid")
def search_knowledge_hybrid(query: str, doc_type: str = "", limit: int = 5,
                            vector_weight: float = 0.4, keyword_weight: float = 0.6) -> str:
    """混合检索知识库（关键词 + 向量相似度）

    Args:
        query: 查询文本（支持中英文）
        doc_type: 可选类型筛选（spec/faq/experience/rule）
        limit: 返回数量
        vector_weight: 向量相似度权重（0-1）
        keyword_weight: 关键词权重（0-1）

    Returns:
        JSON 字符串：{"results": [{"id": ..., "title": "...", "content": "...", "hybrid_score": ..., "vector_score": ..., "keyword_score": ...}], "embedder": "..."}
    """
    from core.models.knowledge import KnowledgeDoc
    from db import db_session_factory
    from utils.embeddings import embed, cosine_similarity, get_embedder_info
    from datetime import datetime

    if not query or not query.strip():
        return json.dumps({"results": [], "summary": "查询不能为空"})

    session = db_session_factory()
    try:
        # 1. 取所有候选文档
        q = session.query(KnowledgeDoc)
        if doc_type:
            q = q.filter(KnowledgeDoc.doc_type == doc_type)
        docs = q.all()

        if not docs:
            return json.dumps({"results": [], "summary": "知识库为空"})

        # 2. 算 query embedding（一次性）
        query_vec = embed(query)
        embedder_info = get_embedder_info()

        # 3. 给每个文档打分（pgvector 存储的 numpy 向量用 Python 算余弦）
        scored = []
        for d in docs:
            # 3.1 关键词打分
            kw_score = _keyword_score(query, d)

            # 3.2 向量打分 - pgvector 存为 numpy.ndarray
            vec_score = 0.0
            if query_vec and d.embedding is not None:
                try:
                    doc_vec = list(d.embedding) if hasattr(d.embedding, '__iter__') else None
                    if doc_vec and len(doc_vec) == len(query_vec):
                        vec_score = max(0.0, float(cosine_similarity(query_vec, doc_vec)))
                except Exception:
                    vec_score = 0.0

            # 3.3 hybrid
            hybrid = float(keyword_weight * kw_score + vector_weight * vec_score)

            scored.append({
                "id": d.id,
                "title": d.title,
                "content": d.content,
                "doc_type": d.doc_type,
                "hybrid_score": round(hybrid, 3),
                "vector_score": round(float(vec_score), 3),
                "keyword_score": round(float(kw_score), 3),
            })

        # 4. 按 hybrid 排序，取 top
        scored.sort(key=lambda x: -x["hybrid_score"])
        scored = scored[:limit]

        # 5. 过滤掉 score 太低的（避免噪声）
        scored = [s for s in scored if s["hybrid_score"] > 0.05]

        return json.dumps({
            "results": scored,
            "summary": f"找到 {len(scored)} 条相关知识（搜 '{query}', embedder={embedder_info['type']}）",
            "embedder": embedder_info,
        }, ensure_ascii=False)
    finally:
        session.close()


def _keyword_score(query: str, doc) -> float:
    """算关键词相似度 0-1"""
    query_lower = query.lower()
    text = ((doc.title or "") + " " + (doc.content or "") + " " + (doc.keywords or "")).lower()

    # 拆分关键词
    keywords = [k for k in query_lower.replace(',', ' ').split() if k]

    if not keywords:
        return 0.0

    score = 0.0
    for kw in keywords:
        if kw in (doc.title or "").lower():
            score += 0.5  # 标题命中权重高
        if kw in (doc.content or "").lower():
            score += 0.2
        if kw in (doc.keywords or "").lower():
            score += 0.3

    # 归一化
    return min(1.0, score)


@tool("upsert_knowledge_embedding")
def upsert_knowledge_embedding(doc_id: int = None) -> str:
    """为知识库文档计算/更新 embedding

    Args:
        doc_id: 指定文档 ID（不传则处理所有缺失或更新过的文档）

    Returns:
        JSON 字符串：{"processed": N, "embedder": "...", "dim": ...}
    """
    from core.models.knowledge import KnowledgeDoc
    from db import db_session_factory
    from utils.embeddings import embed, get_embedder_info
    from datetime import datetime

    embedder_info = get_embedder_info()

    if embedder_info["type"] == "hash_mock":
        # 警告用户
        pass

    session = db_session_factory()
    try:
        if doc_id:
            docs = session.query(KnowledgeDoc).filter(KnowledgeDoc.id == doc_id).all()
        else:
            docs = session.query(KnowledgeDoc).all()

        if not docs:
            return json.dumps({"processed": 0, "message": "没找到文档"})

        processed = 0
        errors = []
        for d in docs:
            try:
                # 用 title + content 拼成 embedding 输入
                text = f"{d.title or ''}\n{d.content or ''}"
                vec = embed(text)
                if vec is None:
                    errors.append(f"doc {d.id}: embedding 失败")
                    continue
                d.embedding = vec  # pgvector Vector 类型直接存列表，自动转换
                d.embedding_model = embedder_info["type"]
                d.embedding_updated_at = datetime.utcnow()
                processed += 1
            except Exception as e:
                errors.append(f"doc {d.id}: {e}")

        session.commit()

        return json.dumps({
            "processed": processed,
            "total": len(docs),
            "errors": errors[:5] if errors else [],
            "embedder": embedder_info,
        }, ensure_ascii=False)
    finally:
        session.close()


@tool("get_knowledge_stats")
def get_knowledge_stats() -> str:
    """获取知识库统计信息（总数/各类型/有无 embedding/embedder 信息）

    Returns:
        JSON 字符串：{"total": N, "by_type": {...}, "with_embedding": N, "embedder": {...}}
    """
    from core.models.knowledge import KnowledgeDoc
    from db import db_session_factory
    from sqlalchemy import func
    from utils.embeddings import get_embedder_info

    session = db_session_factory()
    try:
        # 1. 总数 + 按类型
        total = session.query(func.count(KnowledgeDoc.id)).scalar() or 0
        by_type = dict(
            session.query(KnowledgeDoc.doc_type, func.count(KnowledgeDoc.id))
            .group_by(KnowledgeDoc.doc_type)
            .all()
        )
        # 2. 有 embedding 的
        with_emb = session.query(func.count(KnowledgeDoc.id)).filter(
            KnowledgeDoc.embedding.isnot(None)
        ).scalar() or 0
        # 3. 各 embedder 模型
        by_model = dict(
            session.query(KnowledgeDoc.embedding_model, func.count(KnowledgeDoc.id))
            .filter(KnowledgeDoc.embedding_model.isnot(None))
            .group_by(KnowledgeDoc.embedding_model)
            .all()
        )

        return json.dumps({
            "total": total,
            "by_type": by_type,
            "with_embedding": with_emb,
            "without_embedding": total - with_emb,
            "by_model": by_model,
            "embedder": get_embedder_info(),
        }, ensure_ascii=False)
    finally:
        session.close()


# ============== 阶段 5 新增工具 ==============

@tool("list_quotations_v2")
def list_quotations_v2(
    status: str = "",
    type: str = "",
    keyword: str = "",
    limit: int = 10
) -> str:
    """按多维度组合查询报价单列表。可指定状态(draft/approved)、类型(line/single)、关键词（名称/方案号）。不传参就查最新 10 条。
    """
    from core.models.quotation import Quotation
    from core.models.user import User
    from db import db_session_factory
    from sqlalchemy import or_

    session = db_session_factory()
    try:
        query = session.query(Quotation)
        if status:
            query = query.filter(Quotation.status == status)
        if type:
            query = query.filter(Quotation.type == type)
        if keyword:
            query = query.filter(
                or_(
                    Quotation.name.like(f'%{keyword}%'),
                    Quotation.scheme_no.like(f'%{keyword}%')
                )
            )
        # Default: exclude version children, newest first
        query = query.filter(Quotation.parent_id.is_(None))
        quotations = query.order_by(Quotation.created_at.desc()).limit(limit).all()

        result = []
        for q in quotations:
            # Fetch creator name
            creator = session.query(User).get(q.creator_id) if q.creator_id else None
            result.append({
                "id": q.id,
                "name": q.name,
                "scheme_no": q.scheme_no,
                "type": q.type,
                "status": q.status,
                "profit_rate": float(q.profit_rate) if q.profit_rate else None,
                "currency": q.currency or "CNY",
                "creator": creator.real_name if creator else "unknown",
                "created_at": str(q.created_at)[:19] if q.created_at else "",
            })
        if not result:
            return json.dumps({"message": "没有找到匹配的报价单", "total": 0})
        return json.dumps({"total": len(result), "quotations": result}, ensure_ascii=False)
    finally:
        session.close()


@tool("get_quotation_full")
def get_quotation_full(quotation_id: int) -> str:
    """获取报价单的完整信息：基本信息 + 模块列表 + 每个模块的物料清单 + 其他费用 + 工时 + 包装 + 差旅。
    当用户问'报价单详情'、'报价单完整信息'、'报价单全部内容'时调此工具。

    返回的 profit_rate 是「对外利润率」（成本上加的利润率），不是「毛利率」。
    如要毛利率，调 get_quotation_gross_margin 工具。
    """
    from core.models.quotation import Quotation
    from core.models.module import Module
    from core.models.material import ModuleMaterial, Material
    from core.models.fee import OtherFee
    from core.models.labor_hour import LaborHour
    from core.models.travel_entry import TravelPersonTrip, TravelPersonDays, PackingEntry
    from db import db_session_factory

    session = db_session_factory()
    try:
        q = session.query(Quotation).get(quotation_id)
        if not q:
            return json.dumps({"error": f"报价单 #{quotation_id} 不存在"})

        # 1. Basic info
        result = {
            "id": q.id,
            "name": q.name,
            "scheme_no": q.scheme_no,
            "type": q.type,
            "status": q.status,
            "currency": q.currency or "CNY",
            "tax_rate": q.tax_rate,
            "profit_rate": float(q.profit_rate) if q.profit_rate else None,
            "created_at": str(q.created_at)[:19] if q.created_at else "",
            "updated_at": str(q.updated_at)[:19] if q.updated_at else "",
        }

        # 2. Modules + Materials
        modules = session.query(Module).filter(Module.quotation_id == q.id).all()
        result["modules"] = []
        for m in modules:
            mod_data = {"id": m.id, "name": m.name, "code": m.code, "description": m.description}
            # Materials in this module
            mms = session.query(ModuleMaterial, Material).join(
                Material, ModuleMaterial.material_id == Material.id, isouter=True
            ).filter(ModuleMaterial.module_id == m.id).all()
            mod_data["materials"] = [{
                "material_id": mm.Material.id if mm.Material else None,
                "name": mm.Material.name if mm.Material else "(未知)",
                "spec": mm.Material.spec if mm.Material else "",
                "category": mm.Material.category if mm.Material else "",
                "brand": mm.Material.brand if mm.Material else "",
                "unit": mm.Material.unit if mm.Material else "",
                "quantity": float(mm.ModuleMaterial.quantity) if mm.ModuleMaterial.quantity else 0,
                "unit_price": float(mm.ModuleMaterial.unit_price_override or mm.Material.unit_price) if (mm.ModuleMaterial.unit_price_override or (mm.Material and mm.Material.unit_price)) else 0,
                "subtotal": (float(mm.ModuleMaterial.quantity) if mm.ModuleMaterial.quantity else 0) * (float(mm.ModuleMaterial.unit_price_override or mm.Material.unit_price) if (mm.ModuleMaterial.unit_price_override or (mm.Material and mm.Material.unit_price)) else 0),
            } for mm in mms]
            result["modules"].append(mod_data)

        # 3. Other fees
        fees = session.query(OtherFee).filter(OtherFee.quotation_id == q.id).all()
        result["other_fees"] = [{
            "id": f.id, "fee_type": f.fee_type, "amount": float(f.amount) if f.amount else 0,
            "description": f.description
        } for f in fees]

        # 4. Labor hours
        hours = session.query(LaborHour).filter(LaborHour.quotation_id == q.id).all()
        result["labor_hours"] = [{
            "id": h.id, "name": h.name, "hours": h.hours, "unit_price": float(h.unit_price) if h.unit_price else 0, "total": float(h.total) if h.total else 0
        } for h in hours]

        # 5. Packing
        packings = session.query(PackingEntry).filter(PackingEntry.quotation_id == q.id).all()
        result["packing"] = [{
            "id": p.id, "quantity": p.quantity, "unit_price": float(p.unit_price) if p.unit_price else 0
        } for p in packings]

        # 6. Travel
        trips = session.query(TravelPersonTrip).filter(TravelPersonTrip.quotation_id == q.id).all()
        result["travel_trips"] = [{
            "id": t.id, "person_count": t.person_count,
            "unit_price": float(t.unit_price) if t.unit_price else 0,
            "visa_fee": float(t.visa_fee) if t.visa_fee else 0,
        } for t in trips]
        days = session.query(TravelPersonDays).filter(TravelPersonDays.quotation_id == q.id).all()
        result["travel_days"] = [{
            "id": d.id, "person_days": float(d.person_days) if d.person_days else 0,
            "unit_price": float(d.unit_price) if d.unit_price else 0
        } for d in days]

        return json.dumps(result, ensure_ascii=False, default=str)
    finally:
        session.close()


@tool("update_quotation_status")
def update_quotation_status(quotation_id: int, new_status: str) -> str:
    """更新报价单状态。支持的状态转换：draft ↔ approved。
    当用户说'提交审批'、'批准'、'退回'、'改状态'时调此工具。
    """
    from core.models.quotation import Quotation
    from core.models.user import User
    from core.models.operation_log import OperationLog
    from db import db_session_factory

    valid_statuses = ["draft", "approved"]
    valid_transitions = {"draft": ["approved"], "approved": ["draft"]}

    if new_status not in valid_statuses:
        return json.dumps({"error": f"无效状态，可用值: {', '.join(valid_statuses)}"})

    session = db_session_factory()
    try:
        q = session.query(Quotation).get(quotation_id)
        if not q:
            return json.dumps({"error": f"报价单 #{quotation_id} 不存在"})

        if q.status == new_status:
            return json.dumps({"message": f"报价单已是 {new_status} 状态，无需修改"})

        if q.status not in valid_transitions or new_status not in valid_transitions.get(q.status, []):
            return json.dumps({"error": f"不能从 {q.status} 转换到 {new_status}"})

        old_status = q.status
        q.status = new_status
        session.commit()

        return json.dumps({
            "success": True,
            "message": f"报价单 #{quotation_id} 状态已从 {old_status} 变更为 {new_status}",
            "id": quotation_id,
            "new_status": new_status,
        }, ensure_ascii=False)
    except Exception as e:
        session.rollback()
        return json.dumps({"error": f"更新状态失败: {str(e)}"})
    finally:
        session.close()


@tool("find_user")
def find_user(keyword: str) -> str:
    """搜索用户。支持用户名、姓名、邮箱模糊匹配。返回用户 id、姓名、角色、部门。
    当用户问'谁负责'、'找一下 xxx'、'xxx 是谁'时调此工具。
    """
    from core.models.user import User
    from db import db_session_factory
    from sqlalchemy import or_

    session = db_session_factory()
    try:
        users = session.query(User).filter(
            or_(
                User.username.like(f'%{keyword}%'),
                User.real_name.like(f'%{keyword}%'),
            ),
            User.is_active == True,
        ).limit(10).all()

        result = [{
            "id": u.id,
            "username": u.username,
            "real_name": u.real_name,
            "role": u.role,
        } for u in users]
        if not result:
            return json.dumps({"message": f"没有找到匹配 '{keyword}' 的用户", "total": 0})
        return json.dumps({"total": len(result), "users": result}, ensure_ascii=False)
    finally:
        session.close()


@tool("list_pending_tasks")
def list_pending_tasks() -> str:
    """查看当前待办事项汇总：待处理的报价单审批、待处理的变更申请、待阅读的消息。
    当用户问'我有什么待办'、'我的工作台'、'今天要做什么'时调此工具。
    """
    from core.models.quotation import Quotation
    from core.models.change_request import ChangeRequest
    from core.models.user import User
    from db import db_session_factory

    session = db_session_factory()
    try:
        # 1. 待审批的报价单（状态 approved 的等待进一步处理）
        pending_quo = session.query(Quotation).filter(Quotation.status == "draft").count()

        # 2. 待处理的变更申请
        pending_cr = session.query(ChangeRequest).filter(
            ChangeRequest.status == "pending"
        ).count()

        # 3. 已处理的变更申请
        approved_cr = session.query(ChangeRequest).filter(
            ChangeRequest.status == "approved"
        ).count()

        # 4. 报价单总数
        total_quo = session.query(Quotation).filter(Quotation.parent_id.is_(None)).count()

        return json.dumps({
            "pending_quotations": pending_quo,
            "total_quotations": total_quo,
            "pending_change_requests": pending_cr,
            "approved_change_requests": approved_cr,
        }, ensure_ascii=False)
    finally:
        session.close()


# ============== 工具注册（OpenAI 协议格式） ==============



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
    },
    {
        "type": "function",
        "function": {
            "name": "audit_quotation",
            "description": "审计单个报价单的所有潜在问题（物料价格异常、工时异常、毛利率为负、字段缺失等）。当用户说审一下/查一下报价单/有没有问题/有错误吗时调此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "quotation_id": {
                        "type": "integer",
                        "description": "要审计的报价单 ID"
                    }
                },
                "required": ["quotation_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "audit_materials_price",
            "description": "审计物料库中所有异常价格的物料（用 IQR 方法按分类检测）。当用户说审一下物料/物料价格有没有问题/物料价格异常时调此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "可选物料类别（大件/核心部件/其他件），空字符串审计全部"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "audit_labor_hours",
            "description": "审计工时数据（单条报价单或全部报价单的工时是否合理）。用 ±3σ 统计学方法检测异常工时。当用户说审一下工时/工时有没有问题/工时异常时调此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "quotation_id": {
                        "type": "integer",
                        "description": "可选报价单 ID（查该单工时），空则审计所有报价单"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_hardware_ratio",
            "description": "分析指定报价单中『硬件』（物料）成本占总报价的占比。计算逻辑：分子 = 所有物料小计（quantity × unit_price），分母 = 最终报价（含物料系数+工时+差旅+包装+其他费用+利润+税）。同时按物料 category 拆解：standard / large / other 各占多少。当用户问『硬件占比』『物料占比』『成本结构』时调此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "quotation_id": {
                        "type": "integer",
                        "description": "报价单 ID"
                    }
                },
                "required": ["quotation_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_profitability",
            "description": "分析所有报价单的毛利率分布，给出 Top/Bottom 排名 + 业务洞察（最高/最低/平均/状态分布）。当用户问毛利率分析/哪单最赚/哪单亏了/毛利概览时调此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "返回 Top/Bottom 几个，默认 5",
                        "default": 5
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_trends",
            "description": "分析最近 N 个月报价单的趋势（数量、毛利率、工时）。当用户问趋势/最近几个月情况/业绩走势时调此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "months": {
                        "type": "integer",
                        "description": "最近几个月，默认 6",
                        "default": 6
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "simulate_quotation_change",
            "description": "模拟报价单调整后的场景（客户降价 X% + 保持目标毛利率），算需要压缩多少成本 + 哪些大额物料可议价。当用户问降价后怎么改/能不能降/降价 X% 还能赚钱吗/给我个调整方案时调此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "quotation_id": {
                        "type": "integer",
                        "description": "报价单 ID"
                    },
                    "discount_rate": {
                        "type": "number",
                        "description": "客户要求的降价幅度，0.05 表示 5%",
                        "default": 0.0
                    },
                    "target_profit_rate": {
                        "type": "number",
                        "description": "目标毛利率，0.15 表示 15%。不传则按当前毛利率保持"
                    }
                },
                "required": ["quotation_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "在知识库中搜索相关业务知识（业务规范/FAQ/历史经验/规则）。当用户问业务规范/怎么办/怎么操作/有什么经验/常见问题/规范是什么时调此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词"
                    },
                    "doc_type": {
                        "type": "string",
                        "description": "可选文档类型（spec=规范/faq=常见问题/experience=经验/rule=规则）",
                        "enum": ["", "spec", "faq", "experience", "rule"]
                    },
                    "limit": {
                        "type": "integer",
                        "description": "最多返回几条，默认 5",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_knowledge",
            "description": "添加一条新知识到知识库（业务规范/FAQ/经验/规则）。当用户说记一下/记一笔/加个规范/补充知识时调此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "知识标题"
                    },
                    "content": {
                        "type": "string",
                        "description": "知识内容"
                    },
                    "doc_type": {
                        "type": "string",
                        "description": "文档类型",
                        "enum": ["spec", "faq", "experience", "rule"],
                        "default": "faq"
                    },
                    "keywords": {
                        "type": "string",
                        "description": "检索关键词（逗号分隔）"
                    },
                    "created_by": {
                        "type": "string",
                        "description": "创建者",
                        "default": "ai_user"
                    }
                },
                "required": ["title", "content"]
            }
        }
    }
]

TOOLS += [
    {
        "type": "function",
        "function": {
            "name": "list_quotations_v2",
            "description": "按多维度组合查询报价单列表。可指定状态(draft/approved)、类型(line/single)、关键词。不传参返回最新 10 条。",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "报价单状态过滤：draft=草稿, approved=已批准。不传表示不限",
                        "default": ""
                    },
                    "type": {
                        "type": "string",
                        "description": "报价单类型：line=线体, single=单机。不传表示不限",
                        "default": ""
                    },
                    "keyword": {
                        "type": "string",
                        "description": "搜索关键词，匹配报价单名称或方案号",
                        "default": ""
                    },
                    "limit": {
                        "type": "integer",
                        "description": "最多返回条数，默认 10",
                        "default": 10
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_quotation_full",
            "description": "获取报价单完整信息：基本信息 + 模块 + 每个模块的物料 + 其他费用 + 工时 + 包装 + 差旅。一次调用替代多次 get_quotation_summary + list_modules 等。",
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
            "name": "update_quotation_status",
            "description": "更新报价单状态。支持转换：draft→approved（提交审批）、approved→draft（退回）。需要对应的操作权限。",
            "parameters": {
                "type": "object",
                "properties": {
                    "quotation_id": {
                        "type": "integer",
                        "description": "报价单 ID（数字）"
                    },
                    "new_status": {
                        "type": "string",
                        "enum": ["draft", "approved"],
                        "description": "目标状态：draft=草稿, approved=已批准"
                    }
                },
                "required": ["quotation_id", "new_status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_user",
            "description": "搜索用户。支持用户名、姓名模糊匹配。返回用户 id、真实姓名、角色。当用户问'谁'、'找个人'、'xx是谁'时调用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "用户名或真实姓名关键词"
                    }
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_pending_tasks",
            "description": "查看业务待办汇总：待审批报价单数、待处理变更申请数、总报价单数。当用户问'待办'、'今天要做什么'、'工作台'时调用。",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
]




# ============== 阶段 5-B 工具 ==============

@tool("search_materials_v2")
def search_materials_v2(
    keyword: str = "",
    category: str = "",
    min_price: float = 0,
    max_price: float = 0,
    limit: int = 10
) -> str:
    """物料库增强搜索。支持关键词、分类、价格区间组合过滤。
    已知分类：other=其他件, 标准件=standard, 大件=large, 其他件=其他件。
    当用户问"找一下 xxx 物料"、"xx 元以内的物料"时调用。
    """
    from core.models.material import Material
    from db import db_session_factory
    from sqlalchemy import or_

    session = db_session_factory()
    try:
        query = session.query(Material).filter(Material.status == "active")
        if keyword:
            query = query.filter(
                or_(
                    Material.name.like(f'%{keyword}%'),
                    Material.spec.like(f'%{keyword}%'),
                    Material.brand.like(f'%{keyword}%'),
                )
            )
        if category:
            query = query.filter(Material.category == category)
        if min_price > 0:
            query = query.filter(Material.unit_price >= min_price)
        if max_price > 0:
            query = query.filter(Material.unit_price <= max_price)

        materials = query.order_by(Material.id.desc()).limit(limit).all()
        result = [{
            "id": m.id,
            "name": m.name,
            "spec": m.spec,
            "brand": m.brand,
            "unit": m.unit,
            "unit_price": float(m.unit_price) if m.unit_price else 0,
            "category": m.category,
            "param1": m.param1,
            "param2": m.param2,
            "param3": m.param3,
        } for m in materials]
        if not result:
            return json.dumps({"message": "没有找到匹配的物料", "total": 0})
        return json.dumps({"total": len(result), "materials": result}, ensure_ascii=False)
    finally:
        session.close()


@tool("list_material_categories")
def list_material_categories() -> str:
    """列出系统中所有物料分类及其物料数量。
    当用户问"有哪些分类"、"物料分类"、"分类列表"时调用。
    """
    from core.models.material import Material
    from db import db_session_factory
    from sqlalchemy import func

    session = db_session_factory()
    try:
        rows = session.query(
            Material.category,
            func.count(Material.id).label("count")
        ).filter(Material.status == "active").group_by(Material.category).all()

        result = [{
            "category": r.category or "(未分类)",
            "count": r.count,
        } for r in rows]
        return json.dumps({"categories": result}, ensure_ascii=False)
    finally:
        session.close()


@tool("get_quotation_travel_cost")
def get_quotation_travel_cost(quotation_id: int) -> str:
    """获取报价单的差旅费用明细和总额：人/次、人/天、各分类。
    当用户问"差旅费怎么算"、"差旅明细"、"人天费用"时调用。
    """
    from core.models.quotation import Quotation
    from core.models.travel_entry import TravelPersonTrip, TravelPersonDays
    from core.models.travel import TravelCategory
    from db import db_session_factory

    session = db_session_factory()
    try:
        q = session.query(Quotation).get(quotation_id)
        if not q:
            return json.dumps({"error": f"报价单 #{quotation_id} 不存在"})

        trips = session.query(TravelPersonTrip).filter(TravelPersonTrip.quotation_id == q.id).all()
        days = session.query(TravelPersonDays).filter(TravelPersonDays.quotation_id == q.id).all()

        # 总额
        trip_total = sum(
            (float(t.unit_price or 0) * (t.person_count or 0)) + float(t.visa_fee or 0)
            for t in trips
        )
        days_total = sum(float(d.unit_price or 0) * float(d.person_days or 0) for d in days)
        grand = trip_total + days_total

        return json.dumps({
            "quotation_id": q.id,
            "name": q.name,
            "trip_count": len(trips),
            "day_count": len(days),
            "trip_total": round(trip_total, 2),
            "days_total": round(days_total, 2),
            "grand_total": round(grand, 2),
            "trips": [{
                "id": t.id,
                "category_id": t.travel_category_id,
                "person_count": t.person_count,
                "unit_price": float(t.unit_price) if t.unit_price else 0,
                "visa_fee": float(t.visa_fee) if t.visa_fee else 0,
            } for t in trips],
            "days": [{
                "id": d.id,
                "person_days": float(d.person_days) if d.person_days else 0,
                "unit_price": float(d.unit_price) if d.unit_price else 0,
                "category_id": d.travel_category_id,
            } for d in days],
        }, ensure_ascii=False)
    finally:
        session.close()


@tool("get_quotation_fees")
def get_quotation_fees(quotation_id: int) -> str:
    """获取报价单的所有其他费用明细：运输费、安装费、服务费等。
    当用户问"其他费用"、"服务费"、"运输费"时调用。
    """
    from core.models.quotation import Quotation
    from core.models.fee import OtherFee
    from db import db_session_factory

    session = db_session_factory()
    try:
        q = session.query(Quotation).get(quotation_id)
        if not q:
            return json.dumps({"error": f"报价单 #{quotation_id} 不存在"})

        fees = session.query(OtherFee).filter(OtherFee.quotation_id == q.id).all()
        total = sum(float(f.amount or 0) for f in fees)

        # Group by fee_type
        by_type = {}
        for f in fees:
            t = f.fee_type or "其他"
            by_type.setdefault(t, 0)
            by_type[t] += float(f.amount or 0)

        return json.dumps({
            "quotation_id": q.id,
            "name": q.name,
            "count": len(fees),
            "total": round(total, 2),
            "by_type": {k: round(v, 2) for k, v in by_type.items()},
            "fees": [{
                "id": f.id,
                "fee_type": f.fee_type,
                "location": f.location,
                "amount": float(f.amount) if f.amount else 0,
                "description": f.description,
            } for f in fees],
        }, ensure_ascii=False)
    finally:
        session.close()


@tool("list_org_structure")
def list_org_structure() -> str:
    """列出组织架构：部门树 + 各部门人数。
    当用户问"组织架构"、"部门列表"、"公司有哪些部门"时调用。
    """
    from core.models.department import Department
    from core.models.employee import Employee
    from db import db_session_factory
    from sqlalchemy import func

    session = db_session_factory()
    try:
        depts = session.query(Department).filter(Department.is_active == True).all()
        # 部门人数
        counts = dict(
            session.query(Employee.dept_id, func.count(Employee.id))
            .filter(Employee.is_active == True)
            .group_by(Employee.dept_id)
            .all()
        )
        result = []
        for d in depts:
            result.append({
                "id": d.id,
                "name": d.name,
                "parent_id": d.parent_id,
                "level": d.level,
                "employee_count": counts.get(d.id, 0),
            })
        # 找根部门（parent_id 为空）
        roots = [d for d in result if not d["parent_id"]]
        return json.dumps({
            "total_depts": len(result),
            "root_count": len(roots),
            "departments": result[:50],  # Limit to 50
        }, ensure_ascii=False)
    finally:
        session.close()


@tool("who_can_approve")
def who_can_approve(action: str = "approve") -> str:
    """查询谁能执行某个审批操作：返回有该权限的角色 + 用户数。
    action: approve=审批, view=查看, edit=编辑, delete=删除
    当用户问"谁能审批"、"谁能操作"、"权限查询"时调用。
    """
    from core.models.permission import Permission, Role
    from core.models.user import User
    from db import db_session_factory

    # 权限码映射：action -> 可能的权限 code
    perm_patterns = {
        "approve": ["quotation.approve", "quotation.edit", "*.approve"],
        "view": ["quotation.view", "*.view"],
        "edit": ["quotation.edit", "*.edit"],
        "delete": ["quotation.delete", "*.delete"],
    }

    patterns = perm_patterns.get(action, [action])
    session = db_session_factory()
    try:
        perms = session.query(Permission).filter(
            Permission.code.in_(patterns)
        ).all()

        if not perms:
            # 模糊匹配
            perms = session.query(Permission).filter(
                Permission.code.like(f'%{action}%')
            ).limit(10).all()

        result = []
        for p in perms:
            roles = p.roles.all() if hasattr(p.roles, 'all') else []
            user_count = 0
            for r in roles:
                # 简化：只统计有 role.code == r.code 的用户
                uc = session.query(User).filter(
                    User.role == r.code,
                    User.is_active == True,
                ).count()
                user_count += uc

            result.append({
                "permission": p.code,
                "name": p.name,
                "roles": [r.name for r in roles],
                "user_count": user_count,
            })

        if not result:
            return json.dumps({"message": f"没找到 '{action}' 相关权限", "action": action})
        return json.dumps({
            "action": action,
            "matches": result,
        }, ensure_ascii=False)
    finally:
        session.close()


# ============== 工具定义（OpenAI 协议格式） ==============


TOOLS += [
    {
        "type": "function",
        "function": {
            "name": "search_materials_v2",
            "description": "物料库增强搜索。支持关键词、分类、价格区间组合过滤。已知分类：other=其他件, standard=标准件, large=大件。当用户问'找一下物料'、'xx元以内的物料'时调用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "搜索关键词（匹配名称/规格/品牌）", "default": ""},
                    "category": {"type": "string", "description": "分类过滤：other/standard/large 等", "default": ""},
                    "min_price": {"type": "number", "description": "最低单价，0=不限", "default": 0},
                    "max_price": {"type": "number", "description": "最高单价，0=不限", "default": 0},
                    "limit": {"type": "integer", "description": "最多返回条数", "default": 10}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_material_categories",
            "description": "列出所有物料分类及其数量。问'有哪些分类'、'物料分类'时调用。",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_quotation_travel_cost",
            "description": "获取报价单的差旅费用明细：人/次、人/天、分类、总额。问'差旅费怎么算'、'差旅明细'时调用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "quotation_id": {"type": "integer", "description": "报价单 ID"}
                },
                "required": ["quotation_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_quotation_fees",
            "description": "获取报价单其他费用：运输费/安装费/服务费，按类型分组。问'其他费用'、'服务费'时调用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "quotation_id": {"type": "integer", "description": "报价单 ID"}
                },
                "required": ["quotation_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_org_structure",
            "description": "列出组织架构：部门树 + 部门人数。问'组织架构'、'部门列表'时调用。",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "who_can_approve",
            "description": "查询谁能执行审批操作：返回有该权限的角色 + 用户数。问'谁能审批'、'权限查询'时调用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["approve", "view", "edit", "delete"],
                        "description": "操作类型：approve=审批, view=查看, edit=编辑, delete=删除",
                        "default": "approve"
                    }
                },
                "required": []
            }
        }
    },
]





# ============== 阶段 5-C 工具 ==============

@tool("list_knowledge")
def list_knowledge(doc_type: str = "", limit: int = 20) -> str:
    """列出知识库中所有文档。按时间倒序，可按类型过滤。
    doc_type 可选：spec/faq/experience/rule。
    当用户问"知识库有哪些文档"、"列出知识"、"知识列表"时调用。
    """
    from core.models.knowledge import KnowledgeDoc
    from db import db_session_factory

    session = db_session_factory()
    try:
        query = session.query(KnowledgeDoc)
        if doc_type:
            query = query.filter(KnowledgeDoc.doc_type == doc_type)
        docs = query.order_by(KnowledgeDoc.created_at.desc()).limit(limit).all()
        result = [{
            "id": d.id,
            "doc_type": d.doc_type,
            "title": d.title,
            "keywords": d.keywords,
            "has_embedding": d.embedding is not None,
            "created_at": str(d.created_at)[:19] if d.created_at else "",
            "preview": (d.content or "")[:100],
        } for d in docs]
        return json.dumps({
            "total": len(result),
            "documents": result,
        }, ensure_ascii=False)
    finally:
        session.close()


@tool("delete_knowledge")
def delete_knowledge(doc_id: int) -> str:
    """删除一条知识。需要对应的知识库管理权限（ai.knowledge.edit）。
    当用户说"删除这条知识"、"删掉文档"时调用。
    """
    from core.models.knowledge import KnowledgeDoc
    from db import db_session_factory

    session = db_session_factory()
    try:
        doc = session.query(KnowledgeDoc).get(doc_id)
        if not doc:
            return json.dumps({"error": f"知识 #{doc_id} 不存在"})

        title = doc.title
        session.delete(doc)
        session.commit()
        return json.dumps({
            "success": True,
            "message": f"已删除知识 #{doc_id}: {title}",
        }, ensure_ascii=False)
    except Exception as e:
        session.rollback()
        return json.dumps({"error": f"删除失败: {str(e)}"})
    finally:
        session.close()


@tool("export_quotation")
def export_quotation(quotation_id: int, format: str = "excel") -> str:
    """生成报价单导出文件并返回下载链接。format: word/excel/pdf。
    当用户说"导出报价单"、"下载 Excel"、"生成 PDF"时调用。
    """
    valid_formats = ("word", "excel", "pdf")
    fmt = format.lower()
    if fmt not in valid_formats:
        return json.dumps({
            "error": f"不支持的格式: {format}。可用: {', '.join(valid_formats)}",
        })

    # 返回下载链接（前端可以直接用 /api/exports/quotations/{id}/export/{fmt}）
    base_url = "http://localhost:5001/api/exports"
    url = f"{base_url}/quotations/{quotation_id}/export/{fmt}"

    return json.dumps({
        "quotation_id": quotation_id,
        "format": fmt,
        "download_url": url,
        "message": f"报价单 #{quotation_id} {fmt.upper()} 导出链接已生成。请点击下载或复制链接。",
    }, ensure_ascii=False)


@tool("list_my_conversations")
def list_my_conversations(limit: int = 10) -> str:
    """列出当前用户的 AI 对话历史（基于内存会话存储，重启后清空）。
    当用户问"我之前问过什么"、"对话历史"、"聊天记录"时调用。
    """
    from api.ai import _CONVERSATIONS
    import time as _t

    result = []
    items = list(_CONVERSATIONS.items())
    # 按最新消息时间倒序
    def last_ts(conv_id):
        msgs = _CONVERSATIONS.get(conv_id, [])
        # Use insertion order as proxy
        return len(msgs)
    items.sort(key=lambda kv: last_ts(kv[0]), reverse=True)

    for cid, msgs in items[:limit]:
        # 第一条 user 消息做标题
        first_user = next((m["content"] for m in msgs if m["role"] == "user"), "")
        title = first_user[:30] + ("..." if len(first_user) > 30 else "")
        result.append({
            "id": cid,
            "title": title or f"对话 {cid[:8]}",
            "message_count": len(msgs),
        })
    return json.dumps({
        "total": len(result),
        "conversations": result,
        "note": "会话存储在内存中，重启服务后清空。",
    }, ensure_ascii=False)





# ============== 块 10：原始 SQL 查询 ==============
@tool("execute_sql")
def execute_sql(sql: str, limit: int = 50) -> str:
    """对数据库执行只读 SQL SELECT 查询。当需要的数据超过已有组合工具的能力范围时使用——跨表汇总、批量对比、复杂聚合。

    重要规则：
    1. 只允许 SELECT 开头
    2. limit 默认 50，最大 200
    3. 建议先了解表结构（看 db_schema_reference 模块）

    Args:
        sql: SELECT SQL 语句
        limit: 最大返回行数

    Returns:
        JSON: {"columns": [...], "rows": [[...], ...], "total_rows": N}
    """
    import re
    import json as _json
    sql_stripped = sql.strip()
    if not re.match(r'^\s*SELECT\b', sql_stripped, re.IGNORECASE):
        return _json.dumps({"error": "只允许 SELECT 查询"}, ensure_ascii=False)
    limit = min(limit, 200)
    from db import db_session_factory
    session = db_session_factory()
    try:
        from sqlalchemy import text
        result = session.execute(text(sql))
        columns = list(result.keys())
        rows = []
        for i, row in enumerate(result):
            if i >= limit:
                break
            rows.append([str(v) if v is not None else None for v in row])
        return _json.dumps({
            "columns": columns, "rows": rows, "total_rows": len(rows),
        }, ensure_ascii=False)
    except Exception as e:
        return _json.dumps({"error": str(e)}, ensure_ascii=False)
    finally:
        session.close()


# ============== 块 11：系统日志读取（admin/manager 限定） ==============
import os as _os
import re as _re
from datetime import datetime, timedelta as _td
from pathlib import Path as _Path

_LOG_FILE = _Path(__file__).resolve().parent.parent.parent / "logs" / "app.log"
# 兜底：可能在容器里 logs 路径不同
if not _LOG_FILE.parent.exists():
    _LOG_FILE = _Path("/home/rs8568/project-quote-system/backend_fastapi/logs/app.log")


def _parse_log_line_ts(line: str):
    """从日志行提取时间戳。uvicorn 默认格式: '2026-06-22 10:00:00,123 [INFO] uvicorn...'"""
    # 兼容多种格式
    m = _re.match(r'^(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:[.,]\d+)?)', line)
    if m:
        ts_str = m.group(1).replace('T', ' ').replace(',', '.')
        try:
            return datetime.fromisoformat(ts_str.split('.')[0])
        except ValueError:
            pass
    return None


def _level_in_line(line: str, level: str) -> bool:
    """判断日志行是否匹配级别。uvicorn 输出没显式级别，用关键词兜底。"""
    upper = line.upper()
    if level == 'ERROR':
        return 'ERROR' in upper or 'TRACEBACK' in upper or 'EXCEPTION' in upper
    if level == 'WARNING':
        return 'WARN' in upper or 'ERROR' in upper or 'TRACEBACK' in upper or 'EXCEPTION' in upper
    return True  # INFO / 空 = 全部


@tool("tail_app_logs")
def tail_app_logs(lines: int = 50, level: str = "") -> str:
    """读取后端应用日志的最后 N 行。

    Args:
        lines: 要返回的最后行数（默认 50，最大 500）
        level: 日志级别过滤：ERROR / WARNING / INFO / 空（全部）

    Returns:
        JSON: {lines: [...], file_size_mb, total_lines_read, level_filter}
    """
    import json as _json
    lines = max(1, min(int(lines or 50), 500))
    level = (level or "").upper()

    if not _LOG_FILE.exists():
        return _json.dumps({
            "error": f"日志文件不存在: {_LOG_FILE}",
            "hint": "请用 ./start.sh 启动后端，让日志重定向到 logs/app.log"
        }, ensure_ascii=False)

    try:
        # 高效读取最后 N 行：从文件末尾往前读 chunks
        file_size = _LOG_FILE.stat().st_size
        chunk_size = 8192
        blocks = []
        remaining = file_size
        with open(_LOG_FILE, 'rb') as f:
            while remaining > 0 and sum(len(b) for b in blocks) < lines * 200:
                read_size = min(chunk_size, remaining)
                f.seek(remaining - read_size)
                block = f.read(read_size)
                blocks.insert(0, block)
                remaining -= read_size
                if remaining <= 0:
                    break
            text = b''.join(blocks).decode('utf-8', errors='replace')
        all_lines = text.splitlines()
        # 重新从文件完整读取最后 N 行（避免 chunk 边界截断中间行）
        with open(_LOG_FILE, 'r', encoding='utf-8', errors='replace') as f:
            all_lines = f.readlines()
        tail = all_lines[-lines:] if len(all_lines) > lines else all_lines

        # 应用级别过滤
        if level:
            tail = [ln for ln in tail if _level_in_line(ln, level)]

        # 去除尾随换行符
        tail = [ln.rstrip('\n') for ln in tail]

        return _json.dumps({
            "lines": tail,
            "count": len(tail),
            "file": str(_LOG_FILE),
            "file_size_mb": round(file_size / (1024 * 1024), 3),
            "level_filter": level or "ALL",
        }, ensure_ascii=False)
    except Exception as e:
        return _json.dumps({"error": f"读取日志失败: {e}"}, ensure_ascii=False)


@tool("grep_app_logs")
def grep_app_logs(pattern: str, context_lines: int = 2, max_matches: int = 30) -> str:
    """在应用日志中搜索匹配 pattern 的行（支持正则）。

    Args:
        pattern: 要搜索的关键字或正则表达式
        context_lines: 每个匹配的前后上下文行数（默认 2）
        max_matches: 最大匹配条数（默认 30）

    Returns:
        JSON: {matches: [{line_no, content, context_before, context_after}], total_matches, ...}
    """
    import json as _json
    if not pattern:
        return _json.dumps({"error": "pattern 不能为空"}, ensure_ascii=False)
    context_lines = max(0, min(int(context_lines or 2), 20))
    max_matches = max(1, min(int(max_matches or 30), 200))

    if not _LOG_FILE.exists():
        return _json.dumps({"error": f"日志文件不存在: {_LOG_FILE}"}, ensure_ascii=False)

    try:
        regex = _re.compile(pattern, _re.IGNORECASE)
    except _re.error as e:
        return _json.dumps({"error": f"无效的正则: {e}"}, ensure_ascii=False)

    try:
        with open(_LOG_FILE, 'r', encoding='utf-8', errors='replace') as f:
            all_lines = f.readlines()
    except Exception as e:
        return _json.dumps({"error": f"读取日志失败: {e}"}, ensure_ascii=False)

    matches = []
    for i, line in enumerate(all_lines):
        if regex.search(line):
            ctx_before = ''.join(all_lines[max(0, i - context_lines):i]).rstrip('\n')
            ctx_after = ''.join(all_lines[i + 1:i + 1 + context_lines]).rstrip('\n')
            matches.append({
                "line_no": i + 1,
                "content": line.rstrip('\n'),
                "context_before": ctx_before,
                "context_after": ctx_after,
            })
            if len(matches) >= max_matches:
                break

    return _json.dumps({
        "matches": matches,
        "count": len(matches),
        "truncated": len(matches) >= max_matches,
        "total_lines_searched": len(all_lines),
        "pattern": pattern,
    }, ensure_ascii=False)


@tool("get_recent_errors")
def get_recent_errors(minutes: int = 30, include_warnings: bool = False) -> str:
    """提取最近 N 分钟内的错误/异常。

    Args:
        minutes: 回溯多少分钟（默认 30，最大 1440）
        include_warnings: 是否包含 WARNING 级别

    Returns:
        JSON: {errors: [...], count, time_range}
    """
    import json as _json
    minutes = max(1, min(int(minutes or 30), 1440))
    cutoff = datetime.now() - _td(minutes=minutes)

    if not _LOG_FILE.exists():
        return _json.dumps({"error": f"日志文件不存在: {_LOG_FILE}"}, ensure_ascii=False)

    try:
        with open(_LOG_FILE, 'r', encoding='utf-8', errors='replace') as f:
            all_lines = f.readlines()
    except Exception as e:
        return _json.dumps({"error": f"读取日志失败: {e}"}, ensure_ascii=False)

    errors = []
    # 倒序遍历（最新错误优先）
    for i in range(len(all_lines) - 1, -1, -1):
        line = all_lines[i]
        upper = line.upper()
        is_error = 'ERROR' in upper or 'TRACEBACK' in upper or 'EXCEPTION' in upper
        is_warning = 'WARN' in upper
        if is_error or (include_warnings and is_warning):
            ts = _parse_log_line_ts(line)
            if ts is None or ts >= cutoff:
                # 提取可能的 traceback 后续行（最多 5 行）
                ctx = [line.rstrip('\n')]
                for j in range(1, 6):
                    if i + j < len(all_lines) and all_lines[i + j].startswith((' ', '\t', 'File ', 'Traceback')):
                        ctx.append(all_lines[i + j].rstrip('\n'))
                    else:
                        break
                errors.append({
                    "line_no": i + 1,
                    "timestamp": ts.isoformat() if ts else None,
                    "content": '\n'.join(ctx),
                })
                if len(errors) >= 50:
                    break

    return _json.dumps({
        "errors": errors,
        "count": len(errors),
        "minutes": minutes,
        "cutoff": cutoff.isoformat(),
        "include_warnings": include_warnings,
        "file": str(_LOG_FILE),
    }, ensure_ascii=False)


# ============== 块 12：慢 SQL 监控 (admin/manager 限定) ==============
@tool("get_slow_queries")
def get_slow_queries(limit: int = 10, min_duration_ms: int = 0) -> str:
    """获取最近的慢 SQL 查询（执行时间 > SLOW_QUERY_THRESHOLD_MS 的 SQL）。

    用于定位性能瓶颈:
    - 问"系统有什么慢查询"、"最近慢 SQL"、"哪个接口最慢"时调用
    - 问"为什么这个 API 慢"、"DB 性能问题"时调 get_slow_queries(limit=20) 看具体 SQL
    - 也可以问"系统里有没有执行超过 1 秒的 SQL"

    Args:
        limit: 返回最近多少条（默认 10，最大 50）
        min_duration_ms: 过滤条件: 只返回 >= 该值的（默认 0 = 不过滤）

    Returns:
        JSON: {queries: [{timestamp, duration_ms, sql, params}], count, stats}
    """
    import json as _json
    from core.services.slow_query_monitor import slow_query_buffer

    limit = max(1, min(int(limit or 10), 50))
    min_ms = max(0, float(min_duration_ms or 0))

    queries = slow_query_buffer.get_recent(limit=limit, min_ms=min_ms)
    stats = slow_query_buffer.get_stats()

    return _json.dumps({
        "queries": queries,
        "count": len(queries),
        "limit": limit,
        "min_duration_ms": min_ms,
        "stats": stats,
        "log_file": "logs/slow_queries.log",
        "hint": "完整历史看 logs/slow_queries.log 文件 (用 grep_app_logs 搜索)",
    }, ensure_ascii=False)


@tool("get_slow_query_stats")
def get_slow_query_stats() -> str:
    """获取慢 SQL 统计汇总: 数量/平均/P95/最大。

    问"系统性能怎么样"、"DB 慢不慢"、"最近慢查询统计"时调。

    Returns:
        JSON: {total_recent, total_since_start, avg_ms, max_ms, p95_ms}
    """
    import json as _json
    from core.services.slow_query_monitor import slow_query_buffer
    return _json.dumps(slow_query_buffer.get_stats(), ensure_ascii=False)


# ============== 工具定义（OpenAI 协议格式） ==============


TOOLS += [
    {
        "type": "function",
        "function": {
            "name": "list_knowledge",
            "description": "列出知识库所有文档。按时间倒序，可按类型过滤（spec/faq/experience/rule）。问'知识库有哪些'、'列出知识'时调用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "doc_type": {
                        "type": "string",
                        "enum": ["", "spec", "faq", "experience", "rule"],
                        "description": "文档类型过滤，空=全部",
                        "default": ""
                    },
                    "limit": {"type": "integer", "default": 20, "description": "最多返回条数"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_knowledge",
            "description": "删除一条知识文档。需要 ai.knowledge.edit 权限。问'删除知识'、'删掉这条'时调用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "doc_id": {"type": "integer", "description": "知识文档 ID"}
                },
                "required": ["doc_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "export_quotation",
            "description": "生成报价单导出文件（word/excel/pdf）并返回下载链接。问'导出'、'下载 Excel'、'生成 PDF'时调用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "quotation_id": {"type": "integer", "description": "报价单 ID"},
                    "format": {
                        "type": "string",
                        "enum": ["word", "excel", "pdf"],
                        "description": "导出格式",
                        "default": "excel"
                    }
                },
                "required": ["quotation_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_hybrid",
            "description": "混合检索知识库（关键词 + 向量相似度）。当用户问业务规范/历史经验时调用。比 search_knowledge 更精确（带向量）。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "查询文本"},
                    "doc_type": {"type": "string", "enum": ["", "spec", "faq", "experience", "rule"], "default": "", "description": "类型过滤"},
                    "limit": {"type": "integer", "default": 5, "description": "返回数量"},
                    "vector_weight": {"type": "number", "default": 0.4},
                    "keyword_weight": {"type": "number", "default": 0.6}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "upsert_knowledge_embedding",
            "description": "为知识库文档计算/更新 embedding。内部维护用，业务场景很少直接调用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "doc_id": {"type": "integer", "description": "指定文档 ID，不传则处理所有"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_knowledge_stats",
            "description": "获取知识库统计：总数/各类型/有无 embedding/embedder 信息。问'知识库情况'时调用。",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_my_conversations",
            "description": "列出最近的 AI 对话历史。问'我之前问过什么'、'对话历史'、'聊天记录'时调用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "default": 10, "description": "最多返回条数"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_quotation_gross_margin",
            "description": "【用户问「毛利率/实际毛利率/销售毛利率」时调这个工具】报价单的实际毛利率=利润/销售价。区别于对外利润率(profit_rate=利润/成本)。返回三种数字：对外利润率、销售毛利率(不含税)、含税毛利率。金额明细包括成本、利润、销售价、税额、含税总价。",
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
            "name": "execute_sql",
            "description": "【最终手段-直接数据库查询】对PostgreSQL执行只读SELECT查询。",
            "parameters": {
                "type": "object",
                "properties": {
                    "sql": {
                        "type": "string",
                        "description": "SELECT SQL语句"
                    },
                    "limit": {
                        "type": "integer",
                        "default": 50,
                        "description": "最大返回行数(最多200)"
                    }
                },
                "required": ["sql"]
            }
        }
    },
    # ============== 块 11：系统日志读取（admin/manager 限定） ==============
    {
        "type": "function",
        "function": {
            "name": "tail_app_logs",
            "description": "【系统日志-查看最后N行】读取后端应用日志（logs/app.log）的最后 N 行。用于排查刚刚发生的错误或异常。需要 admin 权限。",
            "parameters": {
                "type": "object",
                "properties": {
                    "lines": {
                        "type": "integer",
                        "default": 50,
                        "description": "要返回的最后行数（默认 50，最大 500）"
                    },
                    "level": {
                        "type": "string",
                        "enum": ["", "ERROR", "WARNING", "INFO"],
                        "default": "",
                        "description": "日志级别过滤：ERROR=只看错误，WARNING=错误+警告，INFO=所有，空=所有"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "grep_app_logs",
            "description": "【系统日志-关键字搜索】在应用日志（logs/app.log）中搜索包含指定关键字的行，返回匹配内容+上下文。可用于查特定用户、特定错误码、特定 API 路径的访问记录。需要 admin 权限。",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "要搜索的关键字或正则表达式（支持 re 语法）"
                    },
                    "context_lines": {
                        "type": "integer",
                        "default": 2,
                        "description": "每个匹配的前后上下文行数（默认 2）"
                    },
                    "max_matches": {
                        "type": "integer",
                        "default": 30,
                        "description": "最大匹配条数（默认 30）"
                    }
                },
                "required": ["pattern"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_recent_errors",
            "description": "【系统日志-错误汇总】提取最近 N 分钟内的错误/异常堆栈。用于诊断'现在系统是不是有问题'。需要 admin 权限。",
            "parameters": {
                "type": "object",
                "properties": {
                    "minutes": {
                        "type": "integer",
                        "default": 30,
                        "description": "回溯多少分钟（默认 30，最大 1440=24小时）"
                    },
                    "include_warnings": {
                        "type": "boolean",
                        "default": False,
                        "description": "是否包含 WARNING 级别（默认只返回 ERROR）"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_slow_queries",
            "description": "【慢SQL监控-查询】获取最近的慢 SQL（执行时间 >500ms）。用于定位性能瓶颈: '系统有什么慢查询'、'最近慢 SQL'、'哪个接口最慢'。需要 admin 权限。",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "default": 10,
                        "description": "返回最近多少条（默认 10，最大 50）"
                    },
                    "min_duration_ms": {
                        "type": "integer",
                        "default": 0,
                        "description": "过滤条件: 只返回 >= 该毫秒值的（默认 0=不过滤；如想看 1秒+ 慢 SQL 传 1000）"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_slow_query_stats",
            "description": "【慢SQL监控-统计】获取慢 SQL 汇总: 总数/平均/P95/最大。问'系统性能怎么样'、'DB 慢不慢'时调。需要 admin 权限。",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


def execute_tool(name: str, arguments: Dict[str, Any], user_id: int = None) -> str:
    """根据工具名 + 参数，执行对应的工具函数。

    阶段 6 增强：写操作工具会先做权限校验（user_id 不能为空），
    然后记录操作日志到 OperationLog。
    """
    import json as _json
    func = TOOL_FUNCTIONS.get(name)
    if not func:
        return _json.dumps({"error": f"未知工具: {name}"}, ensure_ascii=False)

    # 权限校验（仅写操作）
    from core.services.ai_guard import check_tool_permission, log_tool_action, get_required_permission

    if get_required_permission(name):
        if not user_id:
            return _json.dumps({
                "error": f"工具 {name} 需要登录用户，但未传入 user_id"
            }, ensure_ascii=False)
        allowed, msg = check_tool_permission(user_id, name)
        if not allowed:
            # 记录失败日志
            log_tool_action(user_id, name, arguments, success=False, result_preview=msg)
            return _json.dumps({
                "error": f"权限不足：{msg}",
                "tool": name,
            }, ensure_ascii=False)

    # 执行工具
    try:
        result = func(**arguments)
        # 解析结果判断是否成功
        success = True
        try:
            parsed = _json.loads(result)
            if isinstance(parsed, dict) and parsed.get("error"):
                success = False
        except Exception:
            pass

        # 只对写操作记日志
        if get_required_permission(name):
            log_tool_action(user_id, name, arguments, success=success, result_preview=result)
        return result
    except Exception as e:
        if get_required_permission(name):
            log_tool_action(user_id, name, arguments, success=False, result_preview=str(e))
        return _json.dumps({"error": f"工具执行异常: {str(e)}"}, ensure_ascii=False)