"""FastAPI 路由 - 参与者类型权限 (迁移版)"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.models.participant_type_permission import ParticipantTypePermission
from api_app.main import get_db, get_current_user_id

router = APIRouter(prefix="/api/participant-type-permissions")


class PtpCreate(BaseModel):
    participant_type: str
    tab_name: str
    tab_label: Optional[str] = None
    description: Optional[str] = ""
    type_name: Optional[str] = None
    sort_order: Optional[int] = 0
    is_disabled: Optional[bool] = False


class PtpUpdate(BaseModel):
    tab_label: Optional[str] = None
    description: Optional[str] = None
    type_name: Optional[str] = None
    sort_order: Optional[int] = None
    is_disabled: Optional[bool] = None


@router.get("")
def get_all(
    participant_type: Optional[str] = Query(None, description="按参与者类型过滤"),
    db=Depends(get_db),
):
    """获取所有类型权限配置，可按 participant_type 过滤"""
    q = db.query(ParticipantTypePermission)
    if participant_type:
        q = q.filter_by(participant_type=participant_type)
    permissions = q.order_by(
        ParticipantTypePermission.participant_type,
        ParticipantTypePermission.sort_order,
    ).all()
    return JSONResponse(content=[p.to_dict() for p in permissions])


@router.post("", status_code=201)
def create(body: PtpCreate, db=Depends(get_db)):
    """添加一条 Tab 权限记录"""
    if not body.participant_type or not body.tab_name:
        raise HTTPException(status_code=400, detail="participant_type 和 tab_name 不能为空")
    p = ParticipantTypePermission(
        participant_type=body.participant_type,
        tab_name=body.tab_name,
        tab_label=body.tab_label or body.tab_name,
        description=body.description or "",
        type_name=body.type_name,
        sort_order=body.sort_order or 0,
        is_disabled=body.is_disabled if body.is_disabled is not None else False,
    )
    db.add(p)
    db.commit()
    return JSONResponse(content=p.to_dict(), status_code=201)


@router.put("/{id}")
def update(id: int, body: PtpUpdate, db=Depends(get_db)):
    """更新权限配置"""
    p = db.query(ParticipantTypePermission).get(id)
    if not p:
        raise HTTPException(status_code=404, detail="记录不存在")
    data = body.model_dump(exclude_unset=True)
    for key in ("tab_label", "description", "type_name", "sort_order", "is_disabled"):
        if key in data:
            setattr(p, key, data[key])
    db.commit()
    return JSONResponse(content=p.to_dict())


@router.delete("/{id}")
def delete(id: int, db=Depends(get_db)):
    """删除单条权限配置"""
    p = db.query(ParticipantTypePermission).get(id)
    if not p:
        raise HTTPException(status_code=404, detail="记录不存在")
    db.delete(p)
    db.commit()
    return JSONResponse(content={"message": "删除成功"})


class PtpCreateType(BaseModel):
    participant_type: str
    type_name: str = ""


@router.post("/types", status_code=201)
def create_type(body: PtpCreateType, db=Depends(get_db)):
    """创建新参与类型"""
    if not body.participant_type:
        raise HTTPException(status_code=400, detail="participant_type 不能为空")
    existing = db.query(ParticipantTypePermission).filter_by(participant_type=body.participant_type).first()
    if existing:
        raise HTTPException(status_code=400, detail="该类型已存在")
    p = ParticipantTypePermission(
        participant_type=body.participant_type,
        tab_name="__type__",
        tab_label=body.type_name or body.participant_type,
        type_name=body.type_name or body.participant_type,
        description="类型标记",
        sort_order=0,
        is_disabled=False,
    )
    db.add(p)
    db.commit()
    return {"message": "创建成功", "participant_type": body.participant_type}

@router.delete("/types/{ptype}")
def delete_type(ptype: str, db=Depends(get_db)):
    """删除某类型的所有权限配置"""
    db.query(ParticipantTypePermission).filter_by(participant_type=ptype).delete()
    db.commit()
    return {"message": "删除成功"}
