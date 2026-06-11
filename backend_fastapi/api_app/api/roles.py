"""FastAPI 路由 - 角色管理 (迁移版)"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from api_app.main import get_db

router = APIRouter(prefix='/api/roles')


class RoleCreate(BaseModel):
    name: str
    code: str = ""
    description: str = ""
    permissions: Optional[List[str]] = None


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[List[str]] = None


class RolePermissionsUpdate(BaseModel):
    permissions: List[str]


# ──────────────────────────────────────────────
# 1. GET /api/roles — 角色列表
# ──────────────────────────────────────────────

@router.get("")
def get_roles(
    page: int = Query(1, ge=1),
    pageSize: int = Query(10, ge=1, le=100),
    keyword: Optional[str] = Query(""),
    db=Depends(get_db),
):
    """获取角色列表（分页 + 关键字搜索）"""
    from app.models import Role

    query = db.query(Role)
    if keyword:
        query = query.filter(
            db.or_(
                Role.name.ilike(f"%{keyword}%"),
                Role.code.ilike(f"%{keyword}%"),
            )
        )

    total = query.count()
    items = query.order_by(Role.id).offset((page - 1) * pageSize).limit(pageSize).all()

    return JSONResponse(content={
        "items": [r.to_dict() for r in items],
        "total": total,
        "page": page,
        "pageSize": pageSize,
    })


# ──────────────────────────────────────────────
# 2. POST /api/roles — 创建角色
# ──────────────────────────────────────────────

@router.post("", status_code=201)
def create_role(body: RoleCreate, db=Depends(get_db)):
    """创建新角色"""
    from app.models import Role, Permission, User

    if not body.name:
        raise HTTPException(status_code=400, detail="角色名称不能为空")

    if body.code and db.query(Role).filter_by(code=body.code).first():
        raise HTTPException(status_code=400, detail="角色代码已存在")

    role = Role(
        name=body.name,
        code=body.code or "",
        description=body.description or "",
    )
    db.add(role)
    db.flush()

    # 设置权限
    for perm_code in (body.permissions or []):
        if perm_code == "*":
            continue
        perm = db.query(Permission).filter_by(code=perm_code).first()
        if perm:
            role.permissions.append(perm)

    db.commit()
    return JSONResponse(content=role.to_dict(), status_code=201)


# ──────────────────────────────────────────────
# 3. PUT /api/roles/{role_id} — 更新角色
# ──────────────────────────────────────────────

@router.put("/{role_id}")
def update_role(role_id: int, body: RoleUpdate, db=Depends(get_db)):
    """更新角色信息（名称、描述、权限）"""
    from app.models import Role, Permission

    role = db.query(Role).get(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    if body.name is not None:
        role.name = body.name
    if body.description is not None:
        role.description = body.description

    # 更新权限
    if body.permissions is not None:
        perm_objs = []
        for perm_code in (body.permissions or []):
            if perm_code == "*":
                continue
            perm = db.query(Permission).filter_by(code=perm_code).first()
            if perm:
                perm_objs.append(perm)
        role.permissions = perm_objs

    db.commit()
    return JSONResponse(content=role.to_dict())


# ──────────────────────────────────────────────
# 4. DELETE /api/roles/{role_id} — 删除角色
# ──────────────────────────────────────────────

@router.delete("/{role_id}")
def delete_role(role_id: int, db=Depends(get_db)):
    """删除角色（角色下有用户时禁止删除）"""
    from app.models import Role, User

    role = db.query(Role).get(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    if db.query(User).filter_by(role=role.code).count() > 0:
        raise HTTPException(status_code=400, detail="该角色下有用户，无法删除")

    role.permissions = []
    db.delete(role)
    db.commit()
    return JSONResponse(content={"message": "删除成功"})


# ──────────────────────────────────────────────
# 5. GET /api/roles/{role_id}/permissions — 角色权限明细
# ──────────────────────────────────────────────

@router.get("/{role_id}/permissions")
def get_role_permissions(role_id: int, db=Depends(get_db)):
    """获取指定角色的权限列表"""
    from app.models import Role

    role = db.query(Role).get(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    return JSONResponse(content={
        "role_id": role.id,
        "role_name": role.name,
        "permissions": [p.to_dict() for p in role.permissions],
    })


# ──────────────────────────────────────────────
# 6. PUT /api/roles/{role_id}/permissions — 更新角色权限
# ──────────────────────────────────────────────

@router.put("/{role_id}/permissions")
def update_role_permissions(role_id: int, body: RolePermissionsUpdate, db=Depends(get_db)):
    """更新指定角色的权限列表"""
    from app.models import Role, Permission

    role = db.query(Role).get(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    perm_objs = []
    for perm_code in (body.permissions or []):
        if perm_code == "*":
            continue
        perm = db.query(Permission).filter_by(code=perm_code).first()
        if perm:
            perm_objs.append(perm)

    role.permissions = perm_objs
    db.commit()

    return JSONResponse(content={
        "role_id": role.id,
        "role_name": role.name,
        "permissions": [p.to_dict() for p in role.permissions],
    })
