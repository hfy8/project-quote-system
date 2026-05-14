from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User
from app.utils.permissions import check_permission, check_any_permission
from app.utils.logger import log_operation
from app.models.operation_log import Action, Module

user_bp = Blueprint('users', __name__)


@user_bp.route('/roles', methods=['GET'])
@jwt_required()
def get_roles():
    """获取角色列表（动态从用户表）"""
    roles = db.session.query(User.role).distinct().all()
    return jsonify([r[0] for r in roles if r[0]]), 200


@user_bp.route('', methods=['GET'])
@jwt_required()
@check_any_permission('user.*', 'user.view')
def get_users():
    """获取用户列表（分页、过滤）"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    role = request.args.get('role')
    keyword = request.args.get('keyword')
    
    query = User.query
    
    # 按角色筛选
    if role:
        query = query.filter_by(role=role)
    
    # 关键字过滤（姓名或工号）
    if keyword:
        query = query.filter(
            db.or_(
                User.real_name.ilike(f'%{keyword}%'),
                User.username.ilike(f'%{keyword}%')
            )
        )
    
    # 只显示活跃用户
    query = query.filter_by(is_active=True)
    
    # 分页
    pagination = query.order_by(User.id).paginate(
        page=page, per_page=page_size, error_out=False
    )
    
    return jsonify({
        'items': [u.to_dict() for u in pagination.items],
        'total': pagination.total,
        'page': pagination.page,
        'page_size': pagination.per_page,
        'pages': pagination.pages
    }), 200


@user_bp.route('', methods=['POST'])
@jwt_required()
@check_permission('user.*')
def create_user():
    """创建用户"""
    data = request.get_json()
    user = User(
        username=data.get('username'),
        real_name=data.get('real_name'),
        role=data.get('role', 'business')
    )
    user.set_password(data.get('password', '123456'))
    db.session.add(user)
    db.session.commit()

    # 记录日志
    log_operation(
        action=Action.CREATE,
        module=Module.USER,
        resource_type='user',
        resource_id=str(user.id),
        detail=f'创建用户 "{user.username}"'
    )
    return jsonify(user.to_dict()), 201


@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@check_permission('user.*')
def update_user(user_id):
    """更新用户"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404

    data = request.get_json()
    old_info = f'{user.username}({user.role})'
    user.real_name = data.get('real_name', user.real_name)
    user.role = data.get('role', user.role)
    if data.get('password'):
        user.set_password(data['password'])

    db.session.commit()

    # 记录日志
    log_operation(
        action=Action.UPDATE,
        module=Module.USER,
        resource_type='user',
        resource_id=str(user.id),
        detail=f'更新用户 "{user.username}" 信息'
    )
    return jsonify(user.to_dict()), 200


@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@check_permission('user.*')
def delete_user(user_id):
    """删除用户"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404

    username = user.username
    db.session.delete(user)
    db.session.commit()

    # 记录日志
    log_operation(
        action=Action.DELETE,
        module=Module.USER,
        resource_type='user',
        resource_id=str(user_id),
        detail=f'删除用户 "{username}"'
    )
    return jsonify({'message': '删除成功'}), 200


@user_bp.route('/<int:user_id>/reset-password', methods=['POST'])
@jwt_required()
@check_permission('user.*')
def reset_password(user_id):
    """重置用户密码为默认密码123456"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404

    user.set_password('123456')
    db.session.commit()

    # 记录日志
    log_operation(
        action=Action.RESET_PASSWORD,
        module=Module.USER,
        resource_type='user',
        resource_id=str(user_id),
        detail=f'重置用户 "{user.username}" 的密码'
    )
    return jsonify({'message': '密码已重置为123456'}), 200