"""FastAPI 路由 - 角色管理 (迁移版)"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.auth import get_db, get_current_user_id
from api.quotations import _check_permission

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
    from core.models import Role

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
def create_role(
    body: RoleCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """创建新角色"""
    _check_permission(db, int(user_id), 'role.create')
    from core.models import Role, Permission, User

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

    from utils.log_helpers import record_crud
    record_crud(
        user_id, 'role', 'create',
        f'创建角色 {role.name} (代码={role.code or "-"})',
        resource_type='role', resource_id=str(role.id),
    )

    return JSONResponse(content=role.to_dict(), status_code=201)


# ──────────────────────────────────────────────
# 2a. GET /api/roles/permissions — 获取所有可用权限（按分组）
# 必须在 /{role_id} 路由之前注册（Starlette 按注册顺序匹配，
# "permissions" 会被 /{role_id} 当作 role_id 吃掉）
# ──────────────────────────────────────────────

@router.get("/permissions")
def get_all_permissions(db=Depends(get_db)):
    """获取所有可用权限列表（按分组）"""
    from core.models import Permission
    return JSONResponse(content={"items": [p.to_dict() for p in db.query(Permission).all()]})


# ──────────────────────────────────────────────
# 2b. POST /api/roles/seed — 初始化/重置权限和角色数据
# 必须在 /{role_id} 路由之前注册（同上）
# ──────────────────────────────────────────────

@router.post("/seed")
def seed_permissions_and_roles_endpoint(
    db=Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """初始化/重置权限和角色数据"""
    from core.models import User
    from utils.permissions import seed_permissions_and_roles, has_permission

    user = db.query(User).get(int(user_id))
    if not has_permission(user.role, 'role.create'):
        raise HTTPException(status_code=403, detail="没有权限")
    seed_permissions_and_roles()
    return JSONResponse(content={"message": "初始化完成"})


# ──────────────────────────────────────────────
# 3a. GET /api/roles/{role_id} — 获取角色详情
# ──────────────────────────────────────────────

@router.get("/{role_id}")
def get_role(role_id: int, db=Depends(get_db)):
    """获取单个角色详情"""
    from core.models import Role
    role = db.query(Role).get(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")
    return JSONResponse(content=role.to_dict())


# ──────────────────────────────────────────────
# 3. PUT /api/roles/{role_id} — 更新角色
# ──────────────────────────────────────────────

@router.put("/{role_id}")
def update_role(
    role_id: int,
    body: RoleUpdate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """更新角色信息（名称、描述、权限）"""
    _check_permission(db, int(user_id), 'role.edit')
    from core.models import Role, Permission

    role = db.query(Role).get(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    changed = []
    if body.name is not None and role.name != body.name:
        changed.append('name')
        role.name = body.name
    if body.description is not None and role.description != body.description:
        changed.append('description')
        role.description = body.description

    # 更新权限
    perm_changed = False
    if body.permissions is not None:
        # 解析新权限对象列表
        new_perm_objs = []
        for perm_code in (body.permissions or []):
            if perm_code == "*":
                continue
            perm = db.query(Permission).filter_by(code=perm_code).first()
            if perm:
                new_perm_objs.append(perm)

        # 取当前权限快照（lazy='select' 直接是 list）
        current_codes = {p.code for p in role.permissions}
        new_codes = {p.code for p in new_perm_objs}
        if current_codes != new_codes:
            perm_changed = True
            changed.append('permissions')

        # 显式 diff 应用：只 DELETE 不存在的 + INSERT 新增的
        current_perms = list(role.permissions)
        to_remove = [p for p in current_perms if p.code not in new_codes]
        to_add = [p for p in new_perm_objs if p.code not in current_codes]

        for p in to_remove:
            role.permissions.remove(p)
        for p in to_add:
            role.permissions.append(p)

    db.commit()

    from utils.log_helpers import record_diff_update
    suffix = f' (变更前 {len(role.permissions)} 项)' if perm_changed else ''
    record_diff_update(
        user_id, 'role', f'角色 {role.name}', changed,
        resource_type='role', resource_id=str(role_id),
        detail_suffix=suffix,
    )

    return JSONResponse(content=role.to_dict())


# ──────────────────────────────────────────────
# 4. DELETE /api/roles/{role_id} — 删除角色
# ──────────────────────────────────────────────

@router.delete("/{role_id}")
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """删除角色（角色下有用户时禁止删除）"""
    _check_permission(db, int(user_id), 'role.delete')
    from core.models import Role, User

    role = db.query(Role).get(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    if db.query(User).filter_by(role=role.code).count() > 0:
        raise HTTPException(status_code=400, detail="该角色下有用户，无法删除")

    role.permissions = []
    role_name = role.name
    db.delete(role)
    db.commit()

    from utils.log_helpers import record_crud
    record_crud(
        user_id, 'role', 'delete',
        f'删除角色 {role_name}',
        resource_type='role', resource_id=str(role_id),
    )

    return JSONResponse(content={"message": "删除成功"})


# ──────────────────────────────────────────────
# 5. GET /api/roles/{role_id}/permissions — 角色权限明细
# ──────────────────────────────────────────────

@router.get("/{role_id}/permissions")
def get_role_permissions(role_id: int, db=Depends(get_db)):
    """获取指定角色的权限列表"""
    from core.models import Role

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
def update_role_permissions(
    role_id: int,
    body: RolePermissionsUpdate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """更新指定角色的权限列表"""
    _check_permission(db, int(user_id), 'role.edit')
    from core.models import Role, Permission

    role = db.query(Role).get(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    # 解析新权限对象
    new_perm_objs = []
    for perm_code in (body.permissions or []):
        if perm_code == "*":
            continue
        perm = db.query(Permission).filter_by(code=perm_code).first()
        if perm:
            new_perm_objs.append(perm)

    # 显式 diff 应用
    new_codes = {p.code for p in new_perm_objs}
    current_perms = list(role.permissions)
    to_remove = [p for p in current_perms if p.code not in new_codes]
    to_add = [p for p in new_perm_objs if p.code not in {pp.code for pp in current_perms}]

    for p in to_remove:
        role.permissions.remove(p)
    for p in to_add:
        role.permissions.append(p)

    db.commit()

    from utils.log_helpers import record_crud
    record_crud(
        user_id, 'role', 'update',
        f'角色 {role.name} 权限变更为 {len(new_perm_objs)} 项',
        resource_type='role', resource_id=str(role_id),
    )

    return JSONResponse(content={
        "role_id": role.id,
        "role_name": role.name,
        "permissions": [p.to_dict() for p in role.permissions],
    })

