"""FastAPI 路由 - Travel Fees (包装类型/差旅配置, 迁移版)"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.models.packing import PackingType
from core.models.travel import TravelCategory, TravelDayRate, TravelMode, TravelPersonTripFee
from core.auth import get_db, get_current_user_id
from api.quotations import _check_permission
from utils.log_helpers import record_crud, record_diff_update

router = APIRouter()


class PackingTypeCreate(BaseModel):
    name: str
    name_en: Optional[str] = None
    unit_price: float = 0
    description: Optional[str] = None
    is_active: bool = True


class PackingTypeUpdate(BaseModel):
    name: Optional[str] = None
    name_en: Optional[str] = None
    unit_price: Optional[float] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class TravelCategoryCreate(BaseModel):
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True


class TravelCategoryUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


class TravelDayRateCreate(BaseModel):
    travel_category_id: int
    unit_price: float = 0
    currency: str = "CNY"
    description: Optional[str] = None
    is_active: bool = True


class TravelDayRateUpdate(BaseModel):
    travel_category_id: Optional[int] = None
    unit_price: Optional[float] = None
    currency: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class TravelModeCreate(BaseModel):
    name: str
    name_en: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True


class TravelModeUpdate(BaseModel):
    name: Optional[str] = None
    name_en: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class TripFeeCreate(BaseModel):
    travel_category_id: int
    travel_mode_id: int
    unit_price: float = 0
    visa_fee: float = 0
    currency: str = "CNY"
    description: Optional[str] = None
    is_active: bool = True


class TripFeeUpdate(BaseModel):
    travel_category_id: Optional[int] = None
    travel_mode_id: Optional[int] = None
    unit_price: Optional[float] = None
    visa_fee: Optional[float] = None
    currency: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


# === PackingType ===

@router.get("/packing-types")
def get_packing_types(db=Depends(get_db)):
    items = db.query(PackingType).filter_by(is_active=True).order_by(PackingType.id).all()
    return JSONResponse(content=[t.to_dict() for t in items])


@router.post("/packing-types", status_code=201)
def create_packing_type(
    body: PackingTypeCreate,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'travel_fee_config.edit')
    t = PackingType(**body.model_dump())
    db.add(t)
    db.commit()
    record_crud(
        int(user_id), 'travel', 'create',
        f'创建 差旅/运输费用配置 {t.name} (类型=包装类型, 单价={float(t.unit_price) if t.unit_price else 0})',
        resource_type='packing_type', resource_id=str(t.id),
    )
    return JSONResponse(content=t.to_dict(), status_code=201)


@router.put("/packing-types/{tid}")
def update_packing_type(
    tid: int, body: PackingTypeUpdate,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'travel_fee_config.edit')
    t = db.query(PackingType).get(tid)
    if not t:
        raise HTTPException(status_code=404, detail="包装类型不存在")
    data = body.model_dump(exclude_unset=True)
    changed = []
    for key in ("name", "name_en", "unit_price", "description", "is_active"):
        if key in data:
            if getattr(t, key) != data[key]:
                changed.append(key)
            setattr(t, key, data[key])
    db.commit()
    record_diff_update(
        int(user_id), 'travel', f'差旅/运输费用配置 {t.name} (类型=包装类型)',
        changed,
        resource_type='packing_type', resource_id=str(tid),
        detail_suffix=f' (单价={float(t.unit_price) if t.unit_price else 0})',
    )
    return JSONResponse(content=t.to_dict())


@router.delete("/packing-types/{tid}")
def delete_packing_type(
    tid: int,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'travel_fee_config.edit')
    t = db.query(PackingType).get(tid)
    if not t:
        raise HTTPException(status_code=404, detail="包装类型不存在")
    name = t.name
    type_label = '包装类型'
    t.is_active = False
    db.commit()
    record_crud(
        int(user_id), 'travel', 'delete',
        f'删除 差旅/运输费用配置 {name} (类型={type_label})',
        resource_type='packing_type', resource_id=str(tid),
    )
    return JSONResponse(content={"message": "已禁用"})


# === TravelCategory ===

@router.get("/travel-categories")
def get_travel_categories(db=Depends(get_db)):
    items = db.query(TravelCategory).filter_by(is_active=True).order_by(TravelCategory.sort_order).all()
    return JSONResponse(content=[t.to_dict() for t in items])


@router.post("/travel-categories", status_code=201)
def create_travel_category(
    body: TravelCategoryCreate,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'travel_fee_config.edit')
    t = TravelCategory(**body.model_dump())
    db.add(t)
    db.commit()
    record_crud(
        int(user_id), 'travel', 'create',
        f'创建 差旅/运输费用配置 {t.name} (类型=差旅分类, 编码={t.code or "-"})',
        resource_type='travel_category', resource_id=str(t.id),
    )
    return JSONResponse(content=t.to_dict(), status_code=201)


@router.put("/travel-categories/{tid}")
def update_travel_category(
    tid: int, body: TravelCategoryUpdate,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'travel_fee_config.edit')
    t = db.query(TravelCategory).get(tid)
    if not t:
        raise HTTPException(status_code=404, detail="差旅分类不存在")
    data = body.model_dump(exclude_unset=True)
    changed = []
    for key in ("name", "code", "description", "sort_order", "is_active"):
        if key in data:
            if getattr(t, key) != data[key]:
                changed.append(key)
            setattr(t, key, data[key])
    db.commit()
    record_diff_update(
        int(user_id), 'travel', f'差旅/运输费用配置 {t.name} (类型=差旅分类)',
        changed,
        resource_type='travel_category', resource_id=str(tid),
        detail_suffix=f' (编码={t.code or "-"}, 排序={t.sort_order or 0})',
    )
    return JSONResponse(content=t.to_dict())


@router.delete("/travel-categories/{tid}")
def delete_travel_category(
    tid: int,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'travel_fee_config.edit')
    t = db.query(TravelCategory).get(tid)
    if not t:
        raise HTTPException(status_code=404, detail="差旅分类不存在")
    name = t.name
    type_label = '差旅分类'
    t.is_active = False
    db.commit()
    record_crud(
        int(user_id), 'travel', 'delete',
        f'删除 差旅/运输费用配置 {name} (类型={type_label})',
        resource_type='travel_category', resource_id=str(tid),
    )
    return JSONResponse(content={"message": "已禁用"})


# === TravelDayRate ===

@router.get("/travel-day-rates")
def get_travel_day_rates(db=Depends(get_db)):
    rates = db.query(TravelDayRate).filter_by(is_active=True).all()
    return JSONResponse(content=[r.to_dict() for r in rates])


@router.post("/travel-day-rates", status_code=201)
def create_travel_day_rate(
    body: TravelDayRateCreate,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'travel_fee_config.edit')
    r = TravelDayRate(**body.model_dump())
    db.add(r)
    db.commit()
    # 获取分类名便于日志可读
    cat_name = r.travel_category.name if r.travel_category else f'分类ID={r.travel_category_id}'
    record_crud(
        int(user_id), 'travel', 'create',
        f'创建 差旅/运输费用配置 {cat_name} 人天单价 (类型=差旅人天单价, 单价={float(r.unit_price) if r.unit_price else 0}, 币种={r.currency or "CNY"})',
        resource_type='travel_day_rate', resource_id=str(r.id),
    )
    return JSONResponse(content=r.to_dict(), status_code=201)


@router.put("/travel-day-rates/{rid}")
def update_travel_day_rate(
    rid: int, body: TravelDayRateUpdate,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'travel_fee_config.edit')
    r = db.query(TravelDayRate).get(rid)
    if not r:
        raise HTTPException(status_code=404, detail="差旅人天单价不存在")
    data = body.model_dump(exclude_unset=True)
    changed = []
    for key in ("travel_category_id", "unit_price", "currency", "description", "is_active"):
        if key in data:
            if getattr(r, key) != data[key]:
                changed.append(key)
            setattr(r, key, data[key])
    db.commit()
    cat_name = r.travel_category.name if r.travel_category else f'分类ID={r.travel_category_id}'
    record_diff_update(
        int(user_id), 'travel', f'差旅/运输费用配置 {cat_name} 人天单价 (类型=差旅人天单价)',
        changed,
        resource_type='travel_day_rate', resource_id=str(rid),
        detail_suffix=f' (单价={float(r.unit_price) if r.unit_price else 0}, 币种={r.currency or "CNY"})',
    )
    return JSONResponse(content=r.to_dict())


@router.delete("/travel-day-rates/{rid}")
def delete_travel_day_rate(
    rid: int,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'travel_fee_config.edit')
    r = db.query(TravelDayRate).get(rid)
    if not r:
        raise HTTPException(status_code=404, detail="差旅人天单价不存在")
    cat_name = r.travel_category.name if r.travel_category else f'分类ID={r.travel_category_id}'
    type_label = '差旅人天单价'
    r.is_active = False
    db.commit()
    record_crud(
        int(user_id), 'travel', 'delete',
        f'删除 差旅/运输费用配置 {cat_name} 人天单价 (类型={type_label})',
        resource_type='travel_day_rate', resource_id=str(rid),
    )
    return JSONResponse(content={"message": "已禁用"})


# === TravelMode ===

@router.get("/travel-modes")
def get_travel_modes(db=Depends(get_db)):
    items = db.query(TravelMode).filter_by(is_active=True).all()
    return JSONResponse(content=[t.to_dict() for t in items])


@router.post("/travel-modes", status_code=201)
def create_travel_mode(
    body: TravelModeCreate,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'travel_fee_config.edit')
    t = TravelMode(**body.model_dump())
    db.add(t)
    db.commit()
    record_crud(
        int(user_id), 'travel', 'create',
        f'创建 差旅/运输费用配置 {t.name} (类型=出行方式, 编码={t.code or "-"})',
        resource_type='travel_mode', resource_id=str(t.id),
    )
    return JSONResponse(content=t.to_dict(), status_code=201)


@router.put("/travel-modes/{tid}")
def update_travel_mode(
    tid: int, body: TravelModeUpdate,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'travel_fee_config.edit')
    t = db.query(TravelMode).get(tid)
    if not t:
        raise HTTPException(status_code=404, detail="出行方式不存在")
    data = body.model_dump(exclude_unset=True)
    changed = []
    for key in ("name", "name_en", "code", "description", "is_active"):
        if key in data:
            if getattr(t, key) != data[key]:
                changed.append(key)
            setattr(t, key, data[key])
    db.commit()
    record_diff_update(
        int(user_id), 'travel', f'差旅/运输费用配置 {t.name} (类型=出行方式)',
        changed,
        resource_type='travel_mode', resource_id=str(tid),
        detail_suffix=f' (编码={t.code or "-"})',
    )
    return JSONResponse(content=t.to_dict())


@router.delete("/travel-modes/{tid}")
def delete_travel_mode(
    tid: int,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'travel_fee_config.edit')
    t = db.query(TravelMode).get(tid)
    if not t:
        raise HTTPException(status_code=404, detail="出行方式不存在")
    name = t.name
    type_label = '出行方式'
    t.is_active = False
    db.commit()
    record_crud(
        int(user_id), 'travel', 'delete',
        f'删除 差旅/运输费用配置 {name} (类型={type_label})',
        resource_type='travel_mode', resource_id=str(tid),
    )
    return JSONResponse(content={"message": "已禁用"})


# === TravelPersonTripFee ===

@router.get("/travel-person-trip-fees")
def get_travel_person_trip_fees(db=Depends(get_db)):
    fees = db.query(TravelPersonTripFee).filter_by(is_active=True).all()
    return JSONResponse(content=[f.to_dict() for f in fees])


@router.post("/travel-person-trip-fees", status_code=201)
def create_travel_person_trip_fee(
    body: TripFeeCreate,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'travel_fee_config.edit')
    f = TravelPersonTripFee(**body.model_dump())
    db.add(f)
    db.commit()
    cat_name = f.travel_category.name if f.travel_category else f'分类ID={f.travel_category_id}'
    mode_name = f.travel_mode.name if f.travel_mode else f'方式ID={f.travel_mode_id}'
    record_crud(
        int(user_id), 'travel', 'create',
        f'创建 差旅/运输费用配置 {cat_name}/{mode_name} (类型=差旅人次单价, 单价={float(f.unit_price) if f.unit_price else 0}, 签证费={float(f.visa_fee) if f.visa_fee else 0}, 币种={f.currency or "CNY"})',
        resource_type='travel_person_trip_fee', resource_id=str(f.id),
    )
    return JSONResponse(content=f.to_dict(), status_code=201)


@router.put("/travel-person-trip-fees/{fid}")
def update_travel_person_trip_fee(
    fid: int, body: TripFeeUpdate,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'travel_fee_config.edit')
    f = db.query(TravelPersonTripFee).get(fid)
    if not f:
        raise HTTPException(status_code=404, detail="差旅人次单价不存在")
    data = body.model_dump(exclude_unset=True)
    changed = []
    for key in ("travel_category_id", "travel_mode_id", "unit_price", "visa_fee", "currency", "description", "is_active"):
        if key in data:
            if getattr(f, key) != data[key]:
                changed.append(key)
            setattr(f, key, data[key])
    db.commit()
    cat_name = f.travel_category.name if f.travel_category else f'分类ID={f.travel_category_id}'
    mode_name = f.travel_mode.name if f.travel_mode else f'方式ID={f.travel_mode_id}'
    record_diff_update(
        int(user_id), 'travel', f'差旅/运输费用配置 {cat_name}/{mode_name} (类型=差旅人次单价)',
        changed,
        resource_type='travel_person_trip_fee', resource_id=str(fid),
        detail_suffix=f' (单价={float(f.unit_price) if f.unit_price else 0}, 签证费={float(f.visa_fee) if f.visa_fee else 0})',
    )
    return JSONResponse(content=f.to_dict())


@router.delete("/travel-person-trip-fees/{fid}")
def delete_travel_person_trip_fee(
    fid: int,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'travel_fee_config.edit')
    f = db.query(TravelPersonTripFee).get(fid)
    if not f:
        raise HTTPException(status_code=404, detail="差旅人次单价不存在")
    cat_name = f.travel_category.name if f.travel_category else f'分类ID={f.travel_category_id}'
    mode_name = f.travel_mode.name if f.travel_mode else f'方式ID={f.travel_mode_id}'
    type_label = '差旅人次单价'
    f.is_active = False
    db.commit()
    record_crud(
        int(user_id), 'travel', 'delete',
        f'删除 差旅/运输费用配置 {cat_name}/{mode_name} (类型={type_label})',
        resource_type='travel_person_trip_fee', resource_id=str(fid),
    )
    return JSONResponse(content={"message": "已禁用"})
