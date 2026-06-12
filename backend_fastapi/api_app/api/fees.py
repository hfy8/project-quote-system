"""FastAPI 路由 - Fees (迁移版)"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from api_app.app.models.fee import OtherFee, FeeType
from api_app.main import get_db, get_current_user_id

router = APIRouter()


class FeeCreate(BaseModel):
    module_id: Optional[int] = None
    fee_type: Optional[str] = None
    location: Optional[str] = ""
    amount: float = 0
    description: Optional[str] = None


class FeeUpdate(BaseModel):
    module_id: Optional[int] = None
    fee_type: Optional[str] = None
    location: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None


class FeeTypeCreate(BaseModel):
    name: str
    name_en: Optional[str] = None
    location: str = "厂内"
    is_active: bool = True


class FeeTypeUpdate(BaseModel):
    name: Optional[str] = None
    name_en: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None


# ---- OtherFee ----

@router.get("/quotations/{quotation_id}/fees")
def get_fees(quotation_id: int, db=Depends(get_db)):
    fees = db.query(OtherFee).filter_by(quotation_id=quotation_id).all()
    return JSONResponse(content=[f.to_dict() for f in fees])


@router.post("/quotations/{quotation_id}/fees", status_code=201)
def create_fee(quotation_id: int, body: FeeCreate, db=Depends(get_db)):
    fee = OtherFee(
        quotation_id=quotation_id,
        module_id=body.module_id,
        fee_type=body.fee_type,
        location=body.location,
        amount=body.amount,
        description=body.description,
    )
    db.add(fee)
    db.commit()
    return JSONResponse(content=fee.to_dict(), status_code=201)


@router.put("/fees/{fee_id}")
def update_fee(fee_id: int, body: FeeUpdate, db=Depends(get_db)):
    fee = db.query(OtherFee).get(fee_id)
    if not fee:
        raise HTTPException(status_code=404, detail="费用不存在")
    data = body.model_dump(exclude_unset=True)
    for key in ("module_id", "fee_type", "location", "amount", "description"):
        if key in data:
            setattr(fee, key, data[key])
    db.commit()
    return JSONResponse(content=fee.to_dict())


@router.delete("/fees/{fee_id}")
def delete_fee(fee_id: int, db=Depends(get_db)):
    fee = db.query(OtherFee).get(fee_id)
    if not fee:
        raise HTTPException(status_code=404, detail="费用不存在")
    db.delete(fee)
    db.commit()
    return JSONResponse(content={"message": "删除成功"})


# ---- FeeType ----

@router.get("/fee-types")
def get_fee_types(db=Depends(get_db)):
    types = db.query(FeeType).all()
    return JSONResponse(content=[f.to_dict() for f in types])


@router.post("/fee-types", status_code=201)
def create_fee_type(body: FeeTypeCreate, db=Depends(get_db)):
    ft = FeeType(name=body.name, name_en=body.name_en, location=body.location, is_active=True)
    db.add(ft)
    db.commit()
    return JSONResponse(content=ft.to_dict(), status_code=201)


@router.put("/fee-types/{fee_type_id}")
def update_fee_type(fee_type_id: int, body: FeeTypeUpdate, db=Depends(get_db)):
    ft = db.query(FeeType).get(fee_type_id)
    if not ft:
        raise HTTPException(status_code=404, detail="费用类型不存在")
    data = body.model_dump(exclude_unset=True)
    for key in ("name", "name_en", "location", "is_active"):
        if key in data:
            setattr(ft, key, data[key])
    db.commit()
    return JSONResponse(content=ft.to_dict())


@router.delete("/fee-types/{fee_type_id}")
def delete_fee_type(fee_type_id: int, db=Depends(get_db)):
    ft = db.query(FeeType).get(fee_type_id)
    if not ft:
        raise HTTPException(status_code=404, detail="费用类型不存在")
    db.delete(ft)
    db.commit()
    return JSONResponse(content={"message": "删除成功"})
