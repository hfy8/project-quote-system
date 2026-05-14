"""角色管理路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

roles_bp = Blueprint('roles', __name__)

# 模拟角色数据
MOCK_ROLES = [
    {'id': 1, 'name': '管理员', 'code': 'admin', 'description': '系统管理员，拥有所有权限', 'permissions': ['*'], 'user_count': 1, 'created_at': '2025-01-01 00:00:00'},
    {'id': 2, 'name': '业务员', 'code': 'business', 'description': '业务员，可管理报价单、费用类型、汇率、系数设定等', 'permissions': ['quotation.*', 'fee.*', 'exchange_rate.*', 'fee_rate.*', 'module.*', 'version.*', 'material.view'], 'user_count': 0, 'created_at': '2025-01-15 00:00:00'},
    {'id': 3, 'name': '采购', 'code': 'purchaser', 'description': '采购人员，可管理原材料、费用类型', 'permissions': ['material.*', 'fee.*'], 'user_count': 0, 'created_at': '2025-02-01 00:00:00'},
    {'id': 4, 'name': '普通用户', 'code': 'viewer', 'description': '普通用户，仅可查看首页和我的分配', 'permissions': ['dashboard.view', 'module_assignment.view'], 'user_count': 0, 'created_at': '2025-02-15 00:00:00'},
]

# 可用的权限列表
AVAILABLE_PERMISSIONS = [
    # 报价单
    {'code': 'quotation.*', 'name': '报价单管理', 'group': '报价单'},
    {'code': 'quotation.create', 'name': '创建报价单', 'group': '报价单'},
    {'code': 'quotation.edit', 'name': '编辑报价单', 'group': '报价单'},
    {'code': 'quotation.delete', 'name': '删除报价单', 'group': '报价单'},
    {'code': 'quotation.export', 'name': '导出报价单', 'group': '报价单'},
    # 物料
    {'code': 'material.*', 'name': '物料管理', 'group': '物料'},
    {'code': 'material.view', 'name': '查看物料', 'group': '物料'},
    {'code': 'material.create', 'name': '创建物料', 'group': '物料'},
    {'code': 'material.edit', 'name': '编辑物料', 'group': '物料'},
    {'code': 'material.delete', 'name': '删除物料', 'group': '物料'},
    # 费用类型
    {'code': 'fee.*', 'name': '费用类型管理', 'group': '费用类型'},
    # 汇率
    {'code': 'exchange_rate.*', 'name': '汇率管理', 'group': '汇率'},
    # 系数设定
    {'code': 'fee_rate.*', 'name': '系数设定', 'group': '系数设定'},
    # 模块
    {'code': 'module.*', 'name': '模块管理', 'group': '模块'},
    # 版本
    {'code': 'version.*', 'name': '版本管理', 'group': '版本'},
    # 用户
    {'code': 'user.*', 'name': '用户管理', 'group': '用户'},
    # 角色
    {'code': 'role.*', 'name': '角色管理', 'group': '角色'},
    # 首页
    {'code': 'dashboard.view', 'name': '首页查看', 'group': '首页'},
    # 我的分配
    {'code': 'module_assignment.view', 'name': '我的分配查看', 'group': '我的分配'},
]

@roles_bp.route('', methods=['GET'])
@jwt_required()
def get_roles():
    """获取角色列表"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    keyword = request.args.get('keyword', '')
    
    filtered_roles = MOCK_ROLES
    if keyword:
        filtered_roles = [r for r in filtered_roles if keyword.lower() in r['name'].lower() or keyword.lower() in r['code'].lower()]
    
    total = len(filtered_roles)
    start = (page - 1) * page_size
    end = start + page_size
    items = filtered_roles[start:end]
    
    return jsonify({
        'items': items,
        'total': total,
        'page': page,
        'pageSize': page_size
    })

@roles_bp.route('/<int:role_id>', methods=['GET'])
@jwt_required()
def get_role(role_id):
    """获取单个角色详情"""
    role = next((r for r in MOCK_ROLES if r['id'] == role_id), None)
    if not role:
        return jsonify({'error': '角色不存在'}), 404
    return jsonify(role)

@roles_bp.route('', methods=['POST'])
@jwt_required()
def create_role():
    """创建新角色"""
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': '角色名称不能为空'}), 400
    
    new_id = max([r['id'] for r in MOCK_ROLES]) + 1
    new_role = {
        'id': new_id,
        'name': data['name'],
        'code': data.get('code', ''),
        'description': data.get('description', ''),
        'permissions': data.get('permissions', []),
        'user_count': 0,
        'created_at': '2026-05-09 00:00:00'
    }
    MOCK_ROLES.append(new_role)
    
    return jsonify(new_role), 201

@roles_bp.route('/<int:role_id>', methods=['PUT'])
@jwt_required()
def update_role(role_id):
    """更新角色"""
    role = next((r for r in MOCK_ROLES if r['id'] == role_id), None)
    if not role:
        return jsonify({'error': '角色不存在'}), 404
    
    data = request.get_json()
    role['name'] = data.get('name', role['name'])
    role['code'] = data.get('code', role['code'])
    role['description'] = data.get('description', role['description'])
    role['permissions'] = data.get('permissions', role['permissions'])
    
    return jsonify(role)

@roles_bp.route('/<int:role_id>', methods=['DELETE'])
@jwt_required()
def delete_role(role_id):
    """删除角色"""
    global MOCK_ROLES
    role = next((r for r in MOCK_ROLES if r['id'] == role_id), None)
    if not role:
        return jsonify({'error': '角色不存在'}), 404
    
    if role['user_count'] > 0:
        return jsonify({'error': '该角色下有用户，无法删除'}), 400
    
    MOCK_ROLES = [r for r in MOCK_ROLES if r['id'] != role_id]
    return jsonify({'message': '删除成功'})

@roles_bp.route('/permissions', methods=['GET'])
@jwt_required()
def get_permissions():
    """获取所有可用的权限列表"""
    return jsonify({'items': AVAILABLE_PERMISSIONS})
