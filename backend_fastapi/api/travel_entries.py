"""FastAPI 路由 - Travel Entries (包装/差旅条目, 迁移版)"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.models.travel_entry import PackingEntry, TravelPersonDays, TravelPersonTrip
from core.models.travel import TravelPersonTripFee, TravelCategory
from core.auth import get_db, get_current_user_id
from api.quotations import _check_permission
from utils.log_helpers import record_crud

router = APIRouter()


# ===== Packing Entry =====

class PackingEntryUpsert(BaseModel):
    quotation_id: int
    packing_type_id: int
    quantity: int = 0
    unit_price: Optional[float] = None
    remark: Optional[str] = None


class PackingEntryUpdate(BaseModel):
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    remark: Optional[str] = None


@router.get("/packing-entries")
def get_packing_entries(quotation_id: Optional[int] = Query(None), db=Depends(get_db)):
    if not quotation_id:
        return JSONResponse(content=[])
    items = db.query(PackingEntry).filter_by(quotation_id=quotation_id).all()
    return JSONResponse(content=[e.to_dict() for e in items])


@router.post("/packing-entries")
def upsert_packing_entry(
    body: PackingEntryUpsert,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.edit')
    entry = db.query(PackingEntry).filter_by(
        quotation_id=body.quotation_id, packing_type_id=body.packing_type_id
    ).first()
    if entry:
        _action = 'update'
        entry.quantity = body.quantity
        entry.unit_price = body.unit_price
        entry.remark = body.remark
    else:
        _action = 'create'
        entry = PackingEntry(
            quotation_id=body.quotation_id,
            packing_type_id=body.packing_type_id,
            quantity=body.quantity,
            unit_price=body.unit_price,
            remark=body.remark,
        )
        db.add(entry)
    db.commit()
    record_crud(
        int(user_id), 'travel', _action,
        f'{"更新" if _action == "update" else "添加"} 运输包装 (报价单#{body.quotation_id}, 包装类型#{body.packing_type_id}, 数量={body.quantity}, 单价={body.unit_price})',
        resource_type='travel_packing', resource_id=str(entry.id),
    )
    return JSONResponse(content=entry.to_dict())


@router.put("/packing-entries/{eid}")
def update_packing_entry(
    eid: int, body: PackingEntryUpdate,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.edit')
    entry = db.query(PackingEntry).get(eid)
    if not entry:
        raise HTTPException(status_code=404, detail="包装条目不存在")
    data = body.model_dump(exclude_unset=True)
    for key in ("quantity", "unit_price", "remark"):
        if key in data:
            setattr(entry, key, data[key])
    db.commit()
    record_crud(
        int(user_id), 'travel', 'update',
        f'更新 运输包装 #{entry.id} (数量={entry.quantity}, 单价={entry.unit_price})',
        resource_type='travel_packing', resource_id=str(entry.id),
    )
    return JSONResponse(content=entry.to_dict())


@router.delete("/packing-entries/{eid}")
def delete_packing_entry(
    eid: int,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.edit')
    entry = db.query(PackingEntry).get(eid)
    if not entry:
        raise HTTPException(status_code=404, detail="包装条目不存在")
    _rid = str(entry.id)
    _qty = entry.quantity
    db.delete(entry)
    db.commit()
    record_crud(
        int(user_id), 'travel', 'delete',
        f'删除 运输包装 #{_rid} (数量={_qty})',
        resource_type='travel_packing', resource_id=_rid,
    )
    return JSONResponse(content={"message": "删除成功"})


# ===== Travel Person Days =====

class PersonDaysUpsert(BaseModel):
    quotation_id: int
    travel_category_id: int
    person_days: int = 0
    unit_price: Optional[float] = None
    remark: Optional[str] = None


class PersonDaysUpdate(BaseModel):
    person_days: Optional[int] = None
    unit_price: Optional[float] = None
    remark: Optional[str] = None


@router.get("/travel-person-days")
def get_travel_person_days(quotation_id: Optional[int] = Query(None), db=Depends(get_db)):
    if not quotation_id:
        return JSONResponse(content=[])
    items = db.query(TravelPersonDays).filter_by(quotation_id=quotation_id).all()
    return JSONResponse(content=[e.to_dict() for e in items])


@router.post("/travel-person-days")
def upsert_travel_person_days(
    body: PersonDaysUpsert,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.edit')
    entry = db.query(TravelPersonDays).filter_by(
        quotation_id=body.quotation_id, travel_category_id=body.travel_category_id
    ).first()
    if entry:
        _action = 'update'
        entry.person_days = body.person_days
        entry.unit_price = body.unit_price
        entry.remark = body.remark
    else:
        _action = 'create'
        entry = TravelPersonDays(
            quotation_id=body.quotation_id,
            travel_category_id=body.travel_category_id,
            person_days=body.person_days,
            unit_price=body.unit_price,
            remark=body.remark,
        )
        db.add(entry)
    db.commit()
    record_crud(
        int(user_id), 'travel', _action,
        f'{"更新" if _action == "update" else "添加"} 差旅人天 (报价单#{body.quotation_id}, 差旅类别#{body.travel_category_id}, 人天={body.person_days}, 单价={body.unit_price})',
        resource_type='person_days', resource_id=str(entry.id),
    )
    return JSONResponse(content=entry.to_dict())


@router.put("/travel-person-days/{eid}")
def update_travel_person_days(
    eid: int, body: PersonDaysUpdate,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.edit')
    entry = db.query(TravelPersonDays).get(eid)
    if not entry:
        raise HTTPException(status_code=404, detail="差旅人天条目不存在")
    data = body.model_dump(exclude_unset=True)
    for key in ("person_days", "unit_price", "remark"):
        if key in data:
            setattr(entry, key, data[key])
    db.commit()
    record_crud(
        int(user_id), 'travel', 'update',
        f'更新 差旅人天 #{entry.id} (人天={entry.person_days}, 单价={entry.unit_price})',
        resource_type='person_days', resource_id=str(entry.id),
    )
    return JSONResponse(content=entry.to_dict())


@router.delete("/travel-person-days/{eid}")
def delete_travel_person_days(
    eid: int,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.edit')
    entry = db.query(TravelPersonDays).get(eid)
    if not entry:
        raise HTTPException(status_code=404, detail="差旅人天条目不存在")
    _rid = str(entry.id)
    _pd = entry.person_days
    db.delete(entry)
    db.commit()
    record_crud(
        int(user_id), 'travel', 'delete',
        f'删除 差旅人天 #{_rid} (人天={_pd})',
        resource_type='person_days', resource_id=_rid,
    )
    return JSONResponse(content={"message": "删除成功"})


# ===== Travel Person Trips =====

class PersonTripUpsert(BaseModel):
    quotation_id: int
    travel_category_id: int
    travel_mode_id: int
    person_count: int = 0
    unit_price: Optional[float] = None
    visa_fee: Optional[float] = None
    remark: Optional[str] = None


class PersonTripUpdate(BaseModel):
    person_count: Optional[int] = None
    unit_price: Optional[float] = None
    visa_fee: Optional[float] = None
    remark: Optional[str] = None


@router.get("/travel-person-trips")
def get_travel_person_trips(quotation_id: Optional[int] = Query(None), db=Depends(get_db)):
    if not quotation_id:
        return JSONResponse(content=[])
    trips = db.query(TravelPersonTrip).filter_by(quotation_id=quotation_id).all()
    result = []
    for trip in trips:
        d = trip.to_dict()
        fee = db.query(TravelPersonTripFee).filter_by(
            travel_category_id=trip.travel_category_id,
            travel_mode_id=trip.travel_mode_id,
            is_active=True,
        ).first()
        if fee:
            # 项目层未自定义 (NULL/0) 时才用系统默认费率, 已自定义的优先保留
            if not trip.unit_price:
                d['unit_price'] = float(fee.unit_price) if fee.unit_price else 0
            if not trip.visa_fee:
                d['visa_fee'] = float(fee.visa_fee) if fee.visa_fee else 0
            d['subtotal'] = d['person_count'] * d['unit_price']
            cat = db.query(TravelCategory).get(trip.travel_category_id)
            if cat and cat.code != 'domestic':
                d['subtotal'] += d['person_count'] * d['visa_fee']
        result.append(d)
    return JSONResponse(content=result)


@router.post("/travel-person-trips")
def upsert_travel_person_trip(
    body: PersonTripUpsert,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.edit')
    trip = db.query(TravelPersonTrip).filter_by(
        quotation_id=body.quotation_id,
        travel_category_id=body.travel_category_id,
        travel_mode_id=body.travel_mode_id,
    ).first()
    if trip:
        _action = 'update'
        trip.person_count = body.person_count
        trip.unit_price = body.unit_price
        trip.visa_fee = body.visa_fee
        trip.remark = body.remark
    else:
        _action = 'create'
        trip = TravelPersonTrip(
            quotation_id=body.quotation_id,
            travel_category_id=body.travel_category_id,
            travel_mode_id=body.travel_mode_id,
            person_count=body.person_count,
            unit_price=body.unit_price,
            visa_fee=body.visa_fee,
            remark=body.remark,
        )
        db.add(trip)
    db.commit()
    record_crud(
        int(user_id), 'travel', _action,
        f'{"更新" if _action == "update" else "添加"} 差旅人次 (报价单#{body.quotation_id}, 差旅类别#{body.travel_category_id}, 出行方式#{body.travel_mode_id}, 人次={body.person_count}, 单价={body.unit_price}, 签证费={body.visa_fee})',
        resource_type='person_trips', resource_id=str(trip.id),
    )
    return JSONResponse(content=trip.to_dict())


@router.put("/travel-person-trips/{tid}")
def update_travel_person_trip(
    tid: int, body: PersonTripUpdate,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.edit')
    trip = db.query(TravelPersonTrip).get(tid)
    if not trip:
        raise HTTPException(status_code=404, detail="差旅人次条目不存在")
    data = body.model_dump(exclude_unset=True)
    for key in ("person_count", "unit_price", "visa_fee", "remark"):
        if key in data:
            setattr(trip, key, data[key])
    db.commit()
    db.refresh(trip)
    record_crud(
        int(user_id), 'travel', 'update',
        f'更新 差旅人次 #{trip.id} (人次={trip.person_count}, 单价={trip.unit_price}, 签证费={trip.visa_fee})',
        resource_type='person_trips', resource_id=str(trip.id),
    )
    return JSONResponse(content=trip.to_dict())


@router.delete("/travel-person-trips/{tid}")
def delete_travel_person_trip(
    tid: int,
    db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id),
):
    _check_permission(db, int(user_id), 'quotation.edit')
    trip = db.query(TravelPersonTrip).get(tid)
    if not trip:
        raise HTTPException(status_code=404, detail="差旅人次条目不存在")
    _rid = str(trip.id)
    _pc = trip.person_count
    db.delete(trip)
    db.commit()
    record_crud(
        int(user_id), 'travel', 'delete',
        f'删除 差旅人次 #{_rid} (人次={_pc})',
        resource_type='person_trips', resource_id=_rid,
    )
    return JSONResponse(content={"message": "删除成功"})
