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
        entry.quantity = body.quantity
        entry.unit_price = body.unit_price
        entry.remark = body.remark
    else:
        entry = PackingEntry(
            quotation_id=body.quotation_id,
            packing_type_id=body.packing_type_id,
            quantity=body.quantity,
            unit_price=body.unit_price,
            remark=body.remark,
        )
        db.add(entry)
    db.commit()
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
    db.delete(entry)
    db.commit()
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
        entry.person_days = body.person_days
        entry.unit_price = body.unit_price
        entry.remark = body.remark
    else:
        entry = TravelPersonDays(
            quotation_id=body.quotation_id,
            travel_category_id=body.travel_category_id,
            person_days=body.person_days,
            unit_price=body.unit_price,
            remark=body.remark,
        )
        db.add(entry)
    db.commit()
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
    db.delete(entry)
    db.commit()
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
        trip.person_count = body.person_count
        trip.unit_price = body.unit_price
        trip.visa_fee = body.visa_fee
        trip.remark = body.remark
    else:
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
    db.delete(trip)
    db.commit()
    return JSONResponse(content={"message": "删除成功"})
