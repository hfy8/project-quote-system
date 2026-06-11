"""FastAPI 路由 - LaborHours (迁移版)"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.models.labor_hour import LaborHour
from app.models.quotation import Quotation
from api_app.main import get_db, get_current_user_id

router = APIRouter()


class LaborHourCreate(BaseModel):
    name: str = ""
    hours: float = 0
    unit_price: float = 0


class LaborHourUpdate(BaseModel):
    name: Optional[str] = None
    hours: Optional[float] = None
    unit_price: Optional[float] = None


@router.get("/quotations/{quotation_id}/labor-hours")
def get_labor_hours(quotation_id: int, db=Depends(get_db)):
    quotation = db.query(Quotation).get(quotation_id)
    if not quotation:
        raise HTTPException(status_code=404, detail="Not found")

    if quotation.type == 'line':
        child_ids = [c.id for c in quotation.children]
        all_ids = [quotation_id] + child_ids
        items = db.query(LaborHour).filter(LaborHour.quotation_id.in_(all_ids)).all()
        q_map = {q.id: q.name for q in db.query(Quotation).filter(Quotation.id.in_(all_ids)).all()}
        result = []
        for r in items:
            d = r.to_dict()
            d['quotation_name'] = q_map.get(r.quotation_id, '')
            result.append(d)
        return JSONResponse(content=result)

    items = db.query(LaborHour).filter_by(quotation_id=quotation_id).all()
    return JSONResponse(content=[r.to_dict() for r in items])


@router.post("/quotations/{quotation_id}/labor-hours", status_code=201)
def create_labor_hour(
    quotation_id: int, body: LaborHourCreate,
    db=Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    total = body.hours * body.unit_price
    item = LaborHour(
        quotation_id=quotation_id,
        name=body.name,
        hours=body.hours,
        unit_price=body.unit_price,
        total=total,
        created_by=int(user_id),
    )
    db.add(item)
    db.commit()
    return JSONResponse(content=item.to_dict(), status_code=201)


def _query_labor_item(db, quotation_id, item_id):
    """支持线体报价单：line 类型时允许子报价单的 labor hours"""
    quotation = db.query(Quotation).get(quotation_id)
    if quotation and quotation.type == 'line':
        child_ids = [c.id for c in quotation.children]
        all_ids = [quotation_id] + child_ids
        return db.query(LaborHour).filter(
            LaborHour.id == item_id,
            LaborHour.quotation_id.in_(all_ids)
        ).first()
    return db.query(LaborHour).filter_by(id=item_id, quotation_id=quotation_id).first()


@router.put("/quotations/{quotation_id}/labor-hours/{item_id}")
def update_labor_hour(
    quotation_id: int, item_id: int, body: LaborHourUpdate, db=Depends(get_db),
):
    item = _query_labor_item(db, quotation_id, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")

    if body.name is not None:
        item.name = body.name
    if body.hours is not None:
        item.hours = body.hours
    if body.unit_price is not None:
        item.unit_price = body.unit_price
    item.total = item.hours * item.unit_price
    db.commit()
    return JSONResponse(content=item.to_dict())


@router.delete("/quotations/{quotation_id}/labor-hours/{item_id}")
def delete_labor_hour(quotation_id: int, item_id: int, db=Depends(get_db)):
    item = _query_labor_item(db, quotation_id, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return JSONResponse(content={"message": "Deleted"})
