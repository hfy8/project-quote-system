"""权限检查工具"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity


def has_permission(role_code, permission):
    """检查角色是否拥有某权限（查DB）"""
    if not role_code:
        return False
    from app.models import Role
    role = Role.query.filter_by(code=role_code).first()
    if not role:
        return False
    # admin 特殊处理
    if role.code == 'admin':
        return True
    return any(p.code == permission for p in role.permissions)


def check_permission(required_permission):
    """装饰器：检查用户是否有指定权限"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from app.models import User
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': '用户不存在'}), 401
            if not has_permission(user.role, required_permission):
                return jsonify({'error': '没有权限'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def check_any_permission(*required_permissions):
    """装饰器：检查用户是否有任意一个权限"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from app.models import User
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': '用户不存在'}), 401
            for perm in required_permissions:
                if has_permission(user.role, perm):
                    return f(*args, **kwargs)
            return jsonify({'error': '没有权限'}), 403
        return decorated_function
    return decorator
