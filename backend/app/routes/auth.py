from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User
from app.utils.logger import log_operation_manual
from app.models.operation_log import Action, Module
from app.utils.permissions import get_user_permissions

auth_bp = Blueprint('auth', __name__)


def get_client_ip():
    """获取客户端IP"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr or '127.0.0.1'


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': '请提供用户名和密码'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': '用户名或密码错误'}), 401

    access_token = create_access_token(identity=user.id)

    # 记录登录日志
    log_operation_manual(
        user_id=user.id,
        username=user.username,
        action=Action.LOGIN,
        module=Module.AUTH,
        resource_type='user',
        resource_id=str(user.id),
        detail=f'用户 "{user.username}" 登录成功'
    )

    # 返回用户信息，使用角色对应的标准权限
    user_data = user.to_dict()
    user_data['permissions'] = get_user_permissions(user.role)

    return jsonify({
        'access_token': access_token,
        'user': user_data
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """用户登出"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user:
        log_operation_manual(
            user_id=user.id,
            username=user.username,
            action=Action.LOGOUT,
            module=Module.AUTH,
            resource_type='user',
            resource_id=str(user.id),
            detail=f'用户 "{user.username}" 登出'
        )
    return jsonify({'message': '登出成功'}), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """获取当前用户信息"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    return jsonify(user.to_dict()), 200


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """修改密码"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if not old_password or not new_password:
        return jsonify({'error': '请提供旧密码和新密码'}), 400
    
    if not user.check_password(old_password):
        return jsonify({'error': '旧密码错误'}), 401
    
    user.set_password(new_password)
    db.session.commit()
    return jsonify({'message': '密码修改成功'}), 200