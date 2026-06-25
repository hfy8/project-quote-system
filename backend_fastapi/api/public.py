
"""公开访问的接口（无需登录）

主要用于第三方系统查询报价单的汇总数据。
"""
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func

from core.auth import get_db
from core.models.quotation import Quotation
from core.models.labor_hour import LaborHour

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/public", tags=["公开查询"])


@router.get("/quotations/labor-hours/total")
def get_quotation_labor_hours_total(
    scheme_no: str = Query(..., min_length=1, max_length=50, description="报价方案号"),
    db=Depends(get_db),
):
    """通过方案号查询报价单(含子报价单)的人力工时总和

    无需登录。返回:
    - 主报价单信息 (id/name/type/status)
    - 子报价单列表 (id/scheme_no/name)
    - 每层 labor_hours 聚合 (hours/total/count)
    - 所有层合计

    工时数据来源: labor_hours 表 (quotation_id 直接关联)
    """
    # 1) 找主报价
    main_q = db.query(Quotation).filter(Quotation.scheme_no == scheme_no).first()
    if not main_q:
        raise HTTPException(status_code=404, detail=f"方案号 {scheme_no} 不存在")

    # 2) 找所有子报价
    children = db.query(Quotation).filter(Quotation.parent_id == main_q.id).all()

    # 3) 聚合主报价 + 子报价的 labor_hours
    all_ids = [main_q.id] + [c.id for c in children]

    rows = db.query(
        LaborHour.quotation_id,
        func.coalesce(func.sum(LaborHour.hours), 0).label("hours"),
        func.coalesce(func.sum(LaborHour.total), 0).label("total"),
        func.count(LaborHour.id).label("count"),
    ).filter(
        LaborHour.quotation_id.in_(all_ids)
    ).group_by(
        LaborHour.quotation_id
    ).all()

    # 建 map: quotation_id -> {hours, total, count}
    agg_by_qid = {r.quotation_id: {
        "hours": round(float(r.hours), 2),
        "total": round(float(r.total), 2),
        "count": int(r.count),
    } for r in rows}

    # 4) 组装响应
    main_agg = agg_by_qid.get(main_q.id, {"hours": 0.0, "total": 0.0, "count": 0})
    child_aggs = []
    for c in children:
        cagg = agg_by_qid.get(c.id, {"hours": 0.0, "total": 0.0, "count": 0})
        child_aggs.append({
            "quotation_id": c.id,
            "scheme_no": c.scheme_no,
            "name": c.name,
            "type": c.type,
            **cagg,
        })

    total_hours = main_agg["hours"] + sum(x["hours"] for x in child_aggs)
    total_amount = main_agg["total"] + sum(x["total"] for x in child_aggs)
    total_count = main_agg["count"] + sum(x["count"] for x in child_aggs)

    return {
        "scheme_no": scheme_no,
        "main_quotation": {
            "id": main_q.id,
            "name": main_q.name,
            "type": main_q.type,
            "status": main_q.status,
            **main_agg,
        },
        "children": child_aggs,
        "summary": {
            "quotation_count": len(all_ids),
            "labor_hours_count": total_count,
            "total_hours": round(total_hours, 2),
            "total_amount": round(total_amount, 2),
        },
    }


# ============== 项目落地状态 (webhook + 监控) ==============

@router.post("/landing-projects/webhook")
async def landing_project_webhook(payload: dict):
    """外部项目管理系统 webhook (无 auth)

    触发场景: 项目状态变化时主动通知 (减少轮询延迟)
    Body 格式: 自由 JSON, 内部存到 full_data 并按 scheme_no UPSERT

    简单实现: 收到 webhook 后立即触发一次 DB 同步 + cache 重载
    """
    try:
        from core.services.project_sync import project_sync
        # 同步一次 DB
        project_sync._sync_db()
        # 重载 cache
        project_sync.reload_cache()
        return {"ok": True, "message": "已同步"}
    except Exception as e:
        return JSONResponse(
            content={"ok": False, "error": str(e)},
            status_code=500,
        )


@router.get("/landing-projects/sync-stats")
async def landing_project_sync_stats():
    """同步状态查询 (公开接口, 仅返回统计信息)"""
    from core.services.project_sync import project_sync
    return project_sync.get_stats()
