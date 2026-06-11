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
from app import db
from app.models import Role, Permission


ALL_PERMISSIONS = [
    # 首页
    {'code': 'dashboard.view', 'name': '查看首页', 'group': '首页'},
    # 报价单
    {'code': 'quotation.view', 'name': '查看报价单', 'group': '报价单'},
    {'code': 'quotation.create', 'name': '创建报价单', 'group': '报价单'},
    {'code': 'quotation.edit', 'name': '编辑报价单', 'group': '报价单'},
    {'code': 'quotation.delete', 'name': '删除报价单', 'group': '报价单'},
    {'code': 'quotation.export', 'name': '导出报价单', 'group': '报价单'},
    # 原材料
    {'code': 'material.view', 'name': '查看物料', 'group': '原材料'},
    {'code': 'material.create', 'name': '创建物料', 'group': '原材料'},
    {'code': 'material.edit', 'name': '编辑物料', 'group': '原材料'},
    {'code': 'material.delete', 'name': '删除物料', 'group': '原材料'},
    {'code': 'material.import', 'name': '导入物料', 'group': '原材料'},
    # 费用类型
    {'code': 'fee_type.view', 'name': '查看费用类型', 'group': '费用类型'},
    {'code': 'fee_type.create', 'name': '创建费用类型', 'group': '费用类型'},
    {'code': 'fee_type.edit', 'name': '编辑费用类型', 'group': '费用类型'},
    {'code': 'fee_type.delete', 'name': '删除费用类型', 'group': '费用类型'},
    # 费用系数
    {'code': 'fee_rate.view', 'name': '查看系数', 'group': '费用系数'},
    {'code': 'fee_rate.edit', 'name': '编辑系数', 'group': '费用系数'},
    # 汇率
    {'code': 'exchange_rate.view', 'name': '查看汇率', 'group': '汇率'},
    {'code': 'exchange_rate.edit', 'name': '编辑汇率', 'group': '汇率'},
    # 模块
    {'code': 'module.view', 'name': '查看模块', 'group': '模块'},
    {'code': 'module.create', 'name': '创建模块', 'group': '模块'},
    {'code': 'module.edit', 'name': '编辑模块', 'group': '模块'},
    {'code': 'module.delete', 'name': '删除模块', 'group': '模块'},
    # 版本
    {'code': 'version.view', 'name': '查看版本', 'group': '版本'},
    {'code': 'version.create', 'name': '创建版本', 'group': '版本'},
    {'code': 'version.edit', 'name': '编辑版本', 'group': '版本'},
    # 用户
    {'code': 'user.view', 'name': '查看用户', 'group': '用户'},
    {'code': 'user.create', 'name': '创建用户', 'group': '用户'},
    {'code': 'user.edit', 'name': '编辑用户', 'group': '用户'},
    {'code': 'user.delete', 'name': '删除用户', 'group': '用户'},
    {'code': 'user.reset_password', 'name': '重置密码', 'group': '用户'},
    # 角色
    {'code': 'role.view', 'name': '查看角色', 'group': '角色'},
    {'code': 'role.create', 'name': '创建角色', 'group': '角色'},
    {'code': 'role.edit', 'name': '编辑角色', 'group': '角色'},
    {'code': 'role.delete', 'name': '删除角色', 'group': '角色'},
    # 日志
    {'code': 'log.view', 'name': '查看日志', 'group': '日志'},
    # 系统
    {'code': 'system.view', 'name': '查看设置', 'group': '系统'},
    {'code': 'system.edit', 'name': '编辑设置', 'group': '系统'},
    # 我的分配
    {'code': 'module_assignment.view', 'name': '查看我的分配', 'group': '我的分配'},
    {'code': 'module_assignment.edit', 'name': '编辑我的分配', 'group': '我的分配'},
    # 参与人权限
    {'code': 'participant_type_permission.view', 'name': '查看参与人权限', 'group': '参与人权限'},
    {'code': 'participant_type_permission.edit', 'name': '编辑参与人权限', 'group': '参与人权限'},
    # 运输差旅配置
    {'code': 'travel_fee_config.view', 'name': '查看运输差旅配置', 'group': '运输差旅'},
    {'code': 'travel_fee_config.edit', 'name': '编辑运输差旅配置', 'group': '运输差旅'},
]

# 默认角色配置
DEFAULT_ROLES = [
    {
        'name': '管理员',
        'code': 'admin',
        'description': '系统管理员，拥有所有权限',
        'permissions': ['*']
    },
    {
        'name': '业务员',
        'code': 'business',
        'description': '业务员，可管理报价单、模块、版本等',
        'permissions': [
            'dashboard.view',
            'quotation.view', 'quotation.create', 'quotation.edit', 'quotation.delete', 'quotation.export',
            'material.view',
            'fee_type.view',
            'fee_rate.view',
            'exchange_rate.view',
            'module.view', 'module.create', 'module.edit', 'module.delete',
            'version.view', 'version.create', 'version.edit',
            'module_assignment.view', 'module_assignment.edit',
        ]
    },
    {
        'name': '采购',
        'code': 'purchaser',
        'description': '采购人员，可管理原材料、费用类型',
        'permissions': [
            'dashboard.view',
            'material.view', 'material.create', 'material.edit', 'material.delete', 'material.import',
            'fee_type.view',
            'module_assignment.view',
        ]
    },
    {
        'name': '普通用户',
        'code': 'viewer',
        'description': '普通用户，仅可查看首页和我的分配',
        'permissions': [
            'dashboard.view',
            'module_assignment.view',
        ]
    },
]


def seed_permissions_and_roles():
    """初始化权限和角色数据（幂等）"""
    # 插入权限
    for p in ALL_PERMISSIONS:
        if not Permission.query.filter_by(code=p['code']).first():
            db.session.add(Permission(**p))
    db.session.flush()

    # 插入/更新角色
    for r in DEFAULT_ROLES:
        role = Role.query.filter_by(code=r['code']).first()
        if not role:
            role = Role(name=r['name'], code=r['code'], description=r['description'])
            db.session.add(role)
            db.session.flush()

        # 直接重新赋值权限列表（替换而非clear）
        perm_objs = []
        for perm_code in r['permissions']:
            if perm_code == '*':
                continue  # admin 特殊处理
            perm = Permission.query.filter_by(code=perm_code).first()
            if perm:
                perm_objs.append(perm)
        role.permissions = perm_objs

    db.session.commit()


