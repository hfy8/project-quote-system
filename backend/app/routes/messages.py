from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Message, User
from datetime import datetime, timedelta

messages_bp = Blueprint('messages', __name__)


@messages_bp.route('', methods=['GET'])
@jwt_required()
def get_messages():
    """获取当前用户的消息列表"""
    user_id = get_jwt_identity()
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    is_read = request.args.get('is_read')  # 可选：筛选已读/未读
    
    query = Message.query.filter_by(recipient_id=user_id).order_by(Message.created_at.desc())
    
    if is_read is not None:
        query = query.filter_by(is_read=is_read.lower() == 'true')
    
    pagination = query.paginate(page=page, per_page=page_size, error_out=False)
    
    return jsonify({
        'items': [m.to_dict() for m in pagination.items],
        'total': pagination.total,
        'page': page,
        'page_size': page_size,
        'pages': pagination.pages
    })


@messages_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    """获取未读消息数量"""
    user_id = get_jwt_identity()
    count = Message.query.filter_by(recipient_id=user_id, is_read=False).count()
    return jsonify({'unread_count': count})


@messages_bp.route('/<int:message_id>/read', methods=['PUT'])
@jwt_required()
def mark_as_read(message_id):
    """标记单条消息为已读"""
    user_id = get_jwt_identity()
    message = Message.query.filter_by(id=message_id, recipient_id=user_id).first()
    
    if not message:
        return jsonify({'error': '消息不存在'}), 404
    
    message.is_read = True
    message.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'success': True})


@messages_bp.route('/read-all', methods=['PUT'])
@jwt_required()
def mark_all_as_read():
    """标记所有消息为已读"""
    user_id = get_jwt_identity()
    Message.query.filter_by(recipient_id=user_id, is_read=False).update({'is_read': True, 'updated_at': datetime.utcnow()})
    db.session.commit()
    return jsonify({'success': True})


@messages_bp.route('/cleanup', methods=['POST'])
@jwt_required()
def cleanup_old_messages():
    """清理过期消息（需要管理员权限）"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return jsonify({'error': '需要管理员权限'}), 403
    
    # 已读消息超过30天删除，未读消息超过60天删除
    read_cutoff = datetime.utcnow() - timedelta(days=30)
    unread_cutoff = datetime.utcnow() - timedelta(days=60)
    
    # 删除已读过期消息
    deleted_read = Message.query.filter(
        Message.is_read == True,
        Message.created_at < read_cutoff
    ).delete(synchronize_session=False)
    
    # 删除未读过期消息
    deleted_unread = Message.query.filter(
        Message.is_read == False,
        Message.created_at < unread_cutoff
    ).delete(synchronize_session=False)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'deleted_read': deleted_read,
        'deleted_unread': deleted_unread,
        'total_deleted': deleted_read + deleted_unread
    })