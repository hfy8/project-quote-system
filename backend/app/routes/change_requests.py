import json
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import ChangeRequest, Quotation, Module, ModuleMaterial, Material, User, VersionSnapshot, OtherFee
from app.utils.permissions import check_permission
from app.utils.logger import log_operation
from app.models.operation_log import Action, Module as LogModule
from app.services.message_service import MessageService

change_request_bp = Blueprint('change_requests', __name__)


def check_quotation_editable(quotation):
    """检查报价单是否可编辑（草稿状态可直接编辑）"""
    return quotation.status == 'draft'


def check_can_submit_change_request(quotation, user_id):
    """检查用户是否有权限提交变更申请"""
    # 报价单状态为 approved 时，需要提交变更申请
    if quotation.status != 'approved':
        return False, '报价单不是已归档状态，无需变更申请'
    
    # 允许所有用户提交变更申请（包括管理员），便于审核追溯
    
    # 检查用户是否是报价单的业务负责人
    if quotation.business_owner_id == user_id:
        return True, ''
    
    # 检查用户是否是模块参与人员
    # （简化处理：暂时允许所有非管理员用户提交变更申请）
    return True, ''


@change_request_bp.route('', methods=['GET'])
@jwt_required()
def get_change_requests():
    """获取变更申请列表"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    quotation_id = request.args.get('quotation_id', type=int)
    status = request.args.get('status')
    
    query = ChangeRequest.query
    
    if quotation_id:
        query = query.filter_by(quotation_id=quotation_id)
    if status:
        query = query.filter_by(status=status)
    
    pagination = query.order_by(ChangeRequest.requested_at.desc()).paginate(
        page=page, per_page=page_size, error_out=False
    )
    
    return jsonify({
        'items': [cr.to_dict() for cr in pagination.items],
        'total': pagination.total,
        'page': pagination.page,
        'page_size': pagination.per_page,
        'pages': pagination.pages
    }), 200


@change_request_bp.route('', methods=['POST'])
@jwt_required()
def create_change_request():
    """创建变更申请"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    quotation_id = data.get('quotation_id')
    module_id = data.get('module_id')
    change_type = data.get('change_type')
    proposed_data = data.get('proposed_data')
    original_data = data.get('original_data')
    
    quotation = Quotation.query.get(quotation_id)
    if not quotation:
        return jsonify({'error': '报价单不存在'}), 404
    
    can_submit, msg = check_can_submit_change_request(quotation, user_id)
    if not can_submit:
        return jsonify({'error': msg}), 400
    
    change_request = ChangeRequest(
        quotation_id=quotation_id,
        module_id=module_id,
        change_type=change_type,
        proposed_data=json.dumps(proposed_data, ensure_ascii=False),
        original_data=json.dumps(original_data, ensure_ascii=False) if original_data else None,
        requested_by=user_id
    )
    db.session.add(change_request)
    db.session.commit()
    
    log_operation(
        action=Action.CREATE,
        module=LogModule.QUOTATION,
        resource_type='change_request',
        resource_id=str(change_request.id),
        detail=f'提交变更申请: {change_type}'
    )
    
    # 发送消息通知业务员
    if quotation.business_owner_id:
        requester = User.query.get(user_id)
        module = Module.query.get(module_id) if module_id else None
        MessageService.notify_change_request_submitted(
            business_owner_id=quotation.business_owner_id,
            requester_name=requester.real_name if requester else '未知',
            quotation_name=quotation.name,
            module_name=module.name if module else '',
            change_type=change_type,
            change_request_id=change_request.id
        )
    
    return jsonify(change_request.to_dict()), 201


@change_request_bp.route('/<int:request_id>/approve', methods=['POST'])
@jwt_required()
@check_permission('quotation.edit')
def approve_change_request(request_id):
    """批准变更申请"""
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    remark = data.get('remark', '')
    
    change_request = ChangeRequest.query.get(request_id)
    if not change_request:
        return jsonify({'error': '变更申请不存在'}), 404
    
    if change_request.status != 'pending':
        return jsonify({'error': '该申请已被处理'}), 400
    
    quotation = change_request.quotation
    if not quotation:
        return jsonify({'error': '关联的报价单不存在'}), 404
    
    # 创建版本快照
    snapshot_data = {
        'name': quotation.name,
        'type': quotation.type,
        'scheme_no': quotation.scheme_no,
        'tax_rate': float(quotation.tax_rate) if quotation.tax_rate else 0,
        'business_owner_id': quotation.business_owner_id,
        'modules': [{
            'id': mod.id,
            'name': mod.name,
            'code': mod.code,
            'materials': [{
                'material_id': mm.material_id,
                'quantity': float(mm.quantity),
                'selected_by_id': mm.selected_by_id
            } for mm in ModuleMaterial.query.filter_by(module_id=mod.id).all()]
        } for mod in quotation.modules],
        'fees': [{
            'module_id': f.module_id,
            'fee_type': f.fee_type,
            'location': f.location,
            'amount': float(f.amount) if f.amount else 0,
            'description': f.description
        } for f in OtherFee.query.filter_by(quotation_id=quotation.id).all()]
    }
    
    # 获取真实的最大版本号（从数据库查询）
    max_version = db.session.query(db.func.max(VersionSnapshot.version_no)).filter_by(
        quotation_id=quotation.id
    ).scalar() or 0
    
    version_no = max_version + 1
    version = VersionSnapshot(
        quotation_id=quotation.id,
        version_no=version_no,
        operation_type='change_approve',
        remark=f'变更申请 #{change_request.id} 批准: {remark}',
        operator_id=user_id,
        snapshot_data=json.dumps(snapshot_data, ensure_ascii=False)
    )
    db.session.add(version)
    db.session.flush()
    
    # 生成版本文件
    from app.routes.exports import generate_version_files
    file_paths = generate_version_files(quotation.id, version_no, snapshot_data, snapshot_data)
    version.pdf_file = file_paths.get('pdf')
    version.word_file = file_paths.get('word')
    
    # 应用变更
    proposed = json.loads(change_request.proposed_data)
    original = json.loads(change_request.original_data) if change_request.original_data else {}
    
    if change_request.change_type == 'material_add':
        # 添加物料
        material = ModuleMaterial(
            module_id=change_request.module_id,
            material_id=proposed['material_id'],
            quantity=proposed['quantity']
        )
        db.session.add(material)
        
    elif change_request.change_type == 'material_update':
        # 更新物料
        module_material = ModuleMaterial.query.get(proposed['id'])
        if module_material:
            module_material.quantity = proposed['quantity']
            
    elif change_request.change_type == 'material_delete':
        # 删除物料
        module_material = ModuleMaterial.query.get(original['id'])
        if module_material:
            db.session.delete(module_material)
    
    # 更新报价单版本号
    quotation.current_version += 1
    
    # 更新变更申请状态
    change_request.status = 'approved'
    change_request.reviewed_by = user_id
    change_request.reviewed_at = datetime.utcnow()
    change_request.review_remark = remark
    
    db.session.commit()
    
    log_operation(
        action=Action.APPROVE,
        module=LogModule.QUOTATION,
        resource_type='change_request',
        resource_id=str(change_request.id),
        detail=f'批准变更申请 #{change_request.id}'
    )
    
    # 发送消息通知申请人
    if change_request.requested_by:
        module = Module.query.get(change_request.module_id) if change_request.module_id else None
        MessageService.notify_change_request_approved(
            requester_id=change_request.requested_by,
            quotation_name=quotation.name,
            module_name=module.name if module else '',
            change_type=change_request.change_type,
            change_request_id=change_request.id
        )
    
    # 发送消息通知业务负责人和成员（版本更新）
    user_ids = [quotation.business_owner_id] if quotation.business_owner_id else []
    for p in quotation.modules:
        for participant in p.participants:
            if participant.user_id not in user_ids:
                user_ids.append(participant.user_id)
    
    if user_ids:
        MessageService.notify_version_updated(
            user_ids=user_ids,
            quotation_name=quotation.name,
            version_no=quotation.current_version,
            quotation_id=quotation.id
        )
    
    return jsonify({
        'message': '变更申请已批准',
        'change_request': change_request.to_dict()
    }), 200


@change_request_bp.route('/<int:request_id>/reject', methods=['POST'])
@jwt_required()
@check_permission('quotation.edit')
def reject_change_request(request_id):
    """拒绝变更申请"""
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    remark = data.get('remark', '')
    
    change_request = ChangeRequest.query.get(request_id)
    if not change_request:
        return jsonify({'error': '变更申请不存在'}), 404
    
    if change_request.status != 'pending':
        return jsonify({'error': '该申请已被处理'}), 400
    
    change_request.status = 'rejected'
    change_request.reviewed_by = user_id
    change_request.reviewed_at = datetime.utcnow()
    change_request.review_remark = remark
    
    db.session.commit()
    
    log_operation(
        action=Action.REJECT,
        module=LogModule.QUOTATION,
        resource_type='change_request',
        resource_id=str(change_request.id),
        detail=f'拒绝变更申请 #{change_request.id}'
    )
    
    # 发送消息通知申请人
    if change_request.requested_by:
        module = Module.query.get(change_request.module_id) if change_request.module_id else None
        MessageService.notify_change_request_rejected(
            requester_id=change_request.requested_by,
            quotation_name=quotation.name,
            module_name=module.name if module else '',
            change_type=change_request.change_type,
            change_request_id=change_request.id,
            reason=remark
        )
    
    return jsonify({
        'message': '变更申请已拒绝',
        'change_request': change_request.to_dict()
    }), 200


@change_request_bp.route('/pending', methods=['GET'])
@jwt_required()
def get_pending_requests():
    """获取当前用户待审核的变更申请"""
    user_id = get_jwt_identity()
    
    # 获取当前用户作为业务负责人的报价单的变更申请
    pending = ChangeRequest.query.join(
        Quotation, ChangeRequest.quotation_id == Quotation.id
    ).filter(
        Quotation.business_owner_id == user_id,
        ChangeRequest.status == 'pending'
    ).order_by(ChangeRequest.requested_at.desc()).all()
    
    return jsonify([cr.to_dict() for cr in pending]), 200
