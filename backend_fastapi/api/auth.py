"""FastAPI 路由 - Auth（v4 修复：所有 model import 在 endpoint 函数内）

为什么不能在模块顶部 import？
- main.py 启动时 create_flask_app() 已经把 31 个 model 注册到 metadata 一次
- 如果 auth.py 模块顶部 `from core.models import User` 会再次触发 User 类的 metaclass
- SQLAlchemy 抛 "Table 'users' is already defined"

解决：模块顶部只 import 与 model 无关的东西（logger 类、Action/Module 枚举常量）
endpoint 函数内用 `with _flask_app.app_context():` 包裹，确保 import 时也在 context 内
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from main import get_db, create_access_token, get_current_user_id
from core.schemas import LoginRequest, ChangePasswordRequest


router = APIRouter()


# ============== 异常 ==============
class AuthError(Exception):
    def __init__(self, message, code=401):
        self.message = message
        self.code = code


class NotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        self.code = 404


class BadRequestError(Exception):
    def __init__(self, message):
        self.message = message
        self.code = 400


# ============== 路由（每个函数内按需 import model） ==============
@router.post("/login", summary="用户登录")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    """用户登录，返回 JWT access_token + 用户信息"""
    # 进入 app context 后再 import model（db.session 已经在 context 内）
    from core.models import User
    from utils.logger import log_operation_manual
    from core.models.operation_log import Action, Module

    try:
        if not body.username or not body.password:
            raise BadRequestError('请提供用户名和密码')

        user = User.query.filter_by(username=username).first() if False else User.query.filter_by(username=body.username).first()
        if not user or not user.check_password(body.password):
            raise AuthError('用户名或密码错误')

        log_operation_manual(
            user_id=user.id,
            username=user.username,
            action=Action.LOGIN,
            module=Module.AUTH,
            resource_type='user',
            resource_id=str(user.id),
            detail=f'用户 "{user.username}" 登录成功',
        )

        token = create_access_token(identity=str(user.id))
        return {
            "code": 0,
            "access_token": token,
            "user": user.to_dict(),
        }
    except (AuthError, NotFoundError, BadRequestError) as e:
        raise HTTPException(status_code=e.code, detail=e.message)


@router.post("/logout", summary="用户登出")
def logout(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    from core.models import User
    from utils.logger import log_operation_manual
    from core.models.operation_log import Action, Module

    try:
        user = User.query.get(user_id)
        if user:
            log_operation_manual(
                user_id=user.id,
                username=user.username,
                action=Action.LOGOUT,
                module=Module.AUTH,
                resource_type='user',
                resource_id=str(user.id),
                detail=f'用户 "{user.username}" 登出',
            )
        return {'message': '登出成功'}
    except (AuthError, NotFoundError, BadRequestError) as e:
        raise HTTPException(status_code=e.code, detail=e.message)


@router.get("/me", summary="获取当前用户信息")
def me(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    from core.models import User, Role

    try:
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError('用户不存在')
        user_data = user.to_dict()
        # 权限
        if user.role:
            role = Role.query.filter_by(code=user.role).first()
            if role:
                if role.code == 'admin':
                    user_data['permissions'] = ['*']
                else:
                    user_data['permissions'] = [p.code for p in role.permissions]
            else:
                user_data['permissions'] = []
        else:
            user_data['permissions'] = []
        return user_data
    except (AuthError, NotFoundError, BadRequestError) as e:
        raise HTTPException(status_code=e.code, detail=e.message)


@router.post("/change-password", summary="修改密码")
def change_password(
    body: ChangePasswordRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    from core.models import User
    from db import db as flask_db

    try:
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError('用户不存在')
        if not body.old_password or not body.new_password:
            raise BadRequestError('请提供旧密码和新密码')
        if not user.check_password(body.old_password):
            raise AuthError('旧密码错误')
        user.set_password(body.new_password)
        flask_db.session.commit()
        return {'message': '密码修改成功'}
    except (AuthError, NotFoundError, BadRequestError) as e:
        raise HTTPException(status_code=e.code, detail=e.message)