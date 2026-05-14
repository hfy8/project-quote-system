from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.module import ModuleParticipant, Module
from app.models.user import User
from app.services.message_service import MessageService

module_participant_bp = Blueprint('module_participants', __name__, url_prefix='/api/modules')


@module_participant_bp.route('/<int:module_id>/participants', methods=['GET'])
@jwt_required()
def get_module_participants(module_id):
    """获取模块参与人员"""
    participants = ModuleParticipant.query.filter_by(module_id=module_id).all()
    return jsonify([p.to_dict() for p in participants])


@module_participant_bp.route('/<int:module_id>/participants', methods=['POST'])
@jwt_required()
def add_module_participants(module_id):
    """添加模块参与人员"""
    user_id = get_jwt_identity()
    data = request.get_json()
    user_ids = data.get('user_ids', [])

    if not user_ids:
        return jsonify({'error': '请选择人员'}), 400

    # 获取模块和报价单信息用于发消息
    module = Module.query.get(module_id)
    quotation = module.quotation if module else None

    added = []
    for uid in user_ids:
        # 检查是否已存在
        existing = ModuleParticipant.query.filter_by(module_id=module_id, user_id=uid).first()
        if existing:
            continue
        p = ModuleParticipant(module_id=module_id, user_id=uid)
        db.session.add(p)
        added.append(uid)
        
        # 发送消息通知被添加的成员
        if module and quotation:
            MessageService.notify_module_member_added(
                user_id=uid,
                quotation_name=quotation.name,
                module_name=module.name,
                quotation_id=quotation.id
            )

    db.session.commit()
    return jsonify({'message': f'已添加 {len(added)} 名人员', 'added': added})


@module_participant_bp.route('/<int:module_id>/participants/<int:participant_id>', methods=['DELETE'])
@jwt_required()
def remove_module_participant(module_id, participant_id):
    """移除模块参与人员"""
    p = ModuleParticipant.query.filter_by(id=participant_id, module_id=module_id).first()
    if not p:
        return jsonify({'error': '人员不存在'}), 404

    db.session.delete(p)
    db.session.commit()
    return jsonify({'message': '已移除'})
