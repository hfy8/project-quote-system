"""FastAPI 路由 - Users (迁移版)"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.models.user import User
from api_app.main import get_db, get_current_user_id

router = APIRouter(prefix='/api/users')


# ============== Pydantic Schemas ==============


class UserCreate(BaseModel):
    username: str
    password: str = "123456"
    real_name: Optional[str] = None
    role: str = "business"
    dept_id: Optional[int] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    real_name: Optional[str] = None
    role: Optional[str] = None
    dept_id: Optional[int] = None
    password: Optional[str] = None


class ResetPasswordBody(BaseModel):
    old_password: str
    new_password: str


class AdminResetPasswordBody(BaseModel):
    user_id: int
    new_password: str = "123456"


class StatusUpdate(BaseModel):
    is_active: bool


# ============== Routes ==============
# IMPORTANT: static paths must be declared BEFORE dynamic paths like /{user_id}
# so that /me, /reset-password, /admin-reset-password don't get captured
# by the {user_id} segment.


@router.get("/me")
def get_current_user_info(user_id: str = Depends(get_current_user_id), db=Depends(get_db)):
    """获取当前登录用户信息"""
    user = db.query(User).get(int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return JSONResponse(content=user.to_dict())


@router.get("")
def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    keyword: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    db=Depends(get_db),
):
    """获取用户列表（分页、过滤）

    - page: 页码，从 1 开始
    - page_size: 每页条数，默认 20
    - keyword: 搜索关键字（匹配用户名或真实姓名）
    - role: 按角色筛选
    """
    query = db.query(User)

    if role:
        query = query.filter(User.role == role)

    if keyword:
        query = query.filter(
            User.real_name.ilike(f"%{keyword}%")
            | User.username.ilike(f"%{keyword}%")
        )

    # 只显示活跃用户
    query = query.filter(User.is_active == True)

    total = query.count()
    items = (
        query.order_by(User.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    pages = (total + page_size - 1) // page_size if total > 0 else 0

    return JSONResponse(
        content={
            "items": [u.to_dict() for u in items],
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": pages,
        }
    )


@router.post("", status_code=201)
def create_user(
    body: UserCreate,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    """创建用户"""
    # 检查用户名是否已存在
    existing = db.query(User).filter_by(username=body.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")

    user = User(
        username=body.username,
        real_name=body.real_name or body.username,
        role=body.role,
        dept_id=body.dept_id,
    )
    user.set_password(body.password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return JSONResponse(content=user.to_dict(), status_code=201)


@router.put("/{user_id}")
def update_user(
    user_id: int,
    body: UserUpdate,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    """更新用户信息"""
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    if body.username is not None:
        # 检查新用户名是否被其他用户占用
        conflict = (
            db.query(User)
            .filter(User.username == body.username, User.id != user_id)
            .first()
        )
        if conflict:
            raise HTTPException(status_code=400, detail="用户名已被其他用户使用")
        user.username = body.username
    if body.real_name is not None:
        user.real_name = body.real_name
    if body.role is not None:
        user.role = body.role
    if body.dept_id is not None:
        user.dept_id = body.dept_id
    if body.password:
        user.set_password(body.password)

    db.commit()
    db.refresh(user)

    return JSONResponse(content=user.to_dict())


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    """删除用户"""
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    db.delete(user)
    db.commit()

    return JSONResponse(content={"message": "删除成功"})


@router.post("/reset-password")
def reset_own_password(
    body: ResetPasswordBody,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    """用户自己修改密码（需验证旧密码）"""
    user = db.query(User).get(int(current_user_id))
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    if not user.check_password(body.old_password):
        raise HTTPException(status_code=400, detail="旧密码不正确")

    user.set_password(body.new_password)
    db.commit()

    return JSONResponse(content={"message": "密码修改成功"})


@router.post("/admin-reset-password")
def admin_reset_password(
    body: AdminResetPasswordBody,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    """管理员重置指定用户的密码"""
    admin = db.query(User).get(int(current_user_id))
    if not admin or admin.role != "admin":
        raise HTTPException(status_code=403, detail="无权限，仅管理员可重置他人密码")

    target = db.query(User).get(body.user_id)
    if not target:
        raise HTTPException(status_code=404, detail="目标用户不存在")

    target.set_password(body.new_password)
    db.commit()

    return JSONResponse(
        content={"message": f"用户 '{target.username}' 的密码已重置"}
    )


@router.put("/{user_id}/status")
def toggle_user_status(
    user_id: int,
    body: StatusUpdate,
    current_user_id: str = Depends(get_current_user_id),
    db=Depends(get_db),
):
    """启用/禁用用户"""
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    user.is_active = body.is_active
    db.commit()
    db.refresh(user)

    status_text = "启用" if body.is_active else "禁用"
    return JSONResponse(
        content={
            "message": f"用户 '{user.username}' 已{status_text}",
            "user": user.to_dict(),
        }
    )
