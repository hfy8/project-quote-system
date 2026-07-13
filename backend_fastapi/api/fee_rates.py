"""FastAPI 路由 - FeeRates (迁移版)"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from core.models.fee_rate import FeeRate
from core.auth import get_db, get_current_user_id
from utils.log_helpers import record_crud, record_diff_update

router = APIRouter()


class FeeRateCreate(BaseModel):
    category: str
    rate: float = 1.0
    description: Optional[str] = None


class FeeRateUpdate(BaseModel):
    rate: Optional[float] = None
    description: Optional[str] = None


@router.get("/fee_rates")
def get_fee_rates(db=Depends(get_db)):
    rates = db.query(FeeRate).all()
    return JSONResponse(content=[r.to_dict() for r in rates])


@router.post("/fee_rates", status_code=201)
def create_fee_rate(
    body: FeeRateCreate,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    rate = FeeRate(category=body.category, rate=body.rate, description=body.description)
    db.add(rate)
    db.commit()

    record_crud(
        user_id, 'fee_rate', 'create',
        f'创建费用系数 {rate.category}={rate.rate}',
        resource_type='fee_rate', resource_id=str(rate.id),
    )
    return JSONResponse(content=rate.to_dict(), status_code=201)


@router.put("/fee_rates/{rate_id}")
def update_fee_rate(
    rate_id: int,
    body: FeeRateUpdate,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    rate = db.query(FeeRate).get(rate_id)
    if not rate:
        raise HTTPException(status_code=404, detail="费率不存在")
    changed_fields = []
    if body.rate is not None:
        rate.rate = body.rate
        changed_fields.append('rate')
    if body.description is not None:
        rate.description = body.description
        changed_fields.append('description')
    db.commit()

    record_diff_update(
        user_id, 'fee_rate', f'费用系数 {rate.category}={rate.rate}',
        changed_fields,
        resource_type='fee_rate', resource_id=str(rate_id),
    )
    return JSONResponse(content=rate.to_dict())


@router.delete("/fee_rates/{rate_id}")
def delete_fee_rate(
    rate_id: int,
    user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    rate = db.query(FeeRate).get(rate_id)
    if not rate:
        raise HTTPException(status_code=404, detail="费率不存在")
    # 删除前快照
    rate_category = rate.category
    rate_value = rate.rate
    db.delete(rate)
    db.commit()

    record_crud(
        user_id, 'fee_rate', 'delete',
        f'删除费用系数 {rate_category}={rate_value}',
        resource_type='fee_rate', resource_id=str(rate_id),
    )
    return JSONResponse(content={"message": "删除成功"})


@router.get("/fee_rates/category/{category}")
def get_fee_rate_by_category(category: str, db=Depends(get_db)):
    rate = db.query(FeeRate).filter(FeeRate.category == category).first()
    if not rate:
        raise HTTPException(status_code=404, detail="费率不存在")
    return JSONResponse(content=rate.to_dict())
