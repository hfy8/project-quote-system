"""权限检查工具"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.user import User

# 角色权限映射 - 与前端路由权限保持一致
ROLE_PERMISSIONS = {
    'admin': ['*'],  # 管理员拥有所有权限

    'manager': [
        # 报价单管理
        'quotation.view', 'quotation.create', 'quotation.edit', 'quotation.delete', 'quotation.export',
        # 原材料管理
        'material.view', 'material.create', 'material.edit', 'material.delete', 'material.import',
        # 费用管理
        'fee.view', 'fee.create', 'fee.edit', 'fee.delete',
        # 费用类型
        'fee_type.view', 'fee_type.create', 'fee_type.edit', 'fee_type.delete',
        # 费用系数
        'fee_rate.view', 'fee_rate.create', 'fee_rate.edit', 'fee_rate.delete',
        # 汇率配置
        'exchange_rate.view', 'exchange_rate.create', 'exchange_rate.edit', 'exchange_rate.delete', 'exchange_rate.set_base',
        # 用户管理
        'user.view', 'user.create', 'user.edit', 'user.delete', 'user.reset_password',
        # 角色管理
        'role.view', 'role.create', 'role.edit', 'role.delete',
        # 系统设置
        'system.view', 'system.edit',
        # 日志查看
        'log.view',
        # 模块分配
        'module_assignment.view', 'module_assignment.edit',
        # 首页
        'dashboard.view',
    ],

    'business': [
        # 报价单管理
        'quotation.view', 'quotation.create', 'quotation.edit', 'quotation.delete', 'quotation.export',
        # 原材料查看
        'material.view',
        # 费用类型查看
        'fee_type.view',
        # 费用系数查看
        'fee_rate.view',
        # 汇率配置查看
        'exchange_rate.view',
        # 模块管理
        'module.view', 'module.create', 'module.edit', 'module.delete', 'module.assign',
        # 版本管理
        'version.view', 'version.create', 'version.edit', 'version.delete',
        # 模块分配
        'module_assignment.view', 'module_assignment.edit',
        # 首页
        'dashboard.view',
    ],

    'purchaser': [
        # 原材料管理
        'material.view', 'material.create', 'material.edit', 'material.delete', 'material.import',
        # 费用类型查看
        'fee_type.view',
        # 模块查看
        'module.view',
        # 模块分配
        'module_assignment.view',
        # 首页
        'dashboard.view',
    ],

    'viewer': [
        # 报价单查看和导出
        'quotation.view', 'quotation.export',
        # 原材料查看
        'material.view',
        # 费用类型查看
        'fee_type.view',
        # 模块查看
        'module.view',
        # 模块分配查看
        'module_assignment.view',
        # 首页
        'dashboard.view',
    ],
}


def get_user_permissions(user_role):
    """获取用户角色的权限列表"""
    return ROLE_PERMISSIONS.get(user_role, [])


def has_permission(user_role, permission):
    """检查用户是否有指定权限"""
    permissions = get_user_permissions(user_role)

    # * 表示所有权限
    if '*' in permissions:
        return True

    # 精确匹配
    if permission in permissions:
        return True

    # 通配符匹配 (如 'quotation.*' 匹配 'quotation.create')
    parts = permission.split('.')
    for perm in permissions:
        if perm.endswith('.*'):
            prefix = perm[:-2]
            if parts[0] == prefix:
                return True

    return False


def match_permission(permissions, required_permission):
    """前端用的权限匹配函数 - 检查权限列表是否包含所需权限"""
    # * 表示所有权限
    if '*' in permissions:
        return True

    # 精确匹配
    if required_permission in permissions:
        return True

    # 通配符匹配
    parts = required_permission.split('.')
    for perm in permissions:
        if perm.endswith('.*'):
            prefix = perm[:-2]
            if parts[0] == prefix:
                return True

    return False


def check_permission(required_permission):
    """装饰器：检查用户是否有权限"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            if not user:
                return jsonify({'error': '用户不存在'}), 401

            if not has_permission(user.role, required_permission):
                return jsonify({'error': '没有权限执行此操作'}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def check_any_permission(*required_permissions):
    """装饰器：检查用户是否有任意一个权限"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            if not user:
                return jsonify({'error': '用户不存在'}), 401

            for perm in required_permissions:
                if has_permission(user.role, perm):
                    return f(*args, **kwargs)

            return jsonify({'error': '没有权限执行此操作'}), 403
        return decorated_function
    return decorator
