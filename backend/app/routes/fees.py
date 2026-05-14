from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.models import OtherFee, FeeType

fee_bp = Blueprint('fees', __name__)


@fee_bp.route('/quotations/<int:quotation_id>/fees', methods=['GET'])
@jwt_required()
def get_fees(quotation_id):
    """获取费用列表"""
    fees = OtherFee.query.filter_by(quotation_id=quotation_id).all()
    return jsonify([f.to_dict() for f in fees]), 200


@fee_bp.route('/quotations/<int:quotation_id>/fees', methods=['POST'])
@jwt_required()
def create_fee(quotation_id):
    """添加费用"""
    data = request.get_json()
    fee = OtherFee(
        quotation_id=quotation_id,
        module_id=data.get('module_id'),
        fee_type=data.get('fee_type'),
        location=data.get('location'),
        amount=data.get('amount', 0),
        description=data.get('description')
    )
    db.session.add(fee)
    db.session.commit()
    return jsonify(fee.to_dict()), 201


@fee_bp.route('/fees/<int:fee_id>', methods=['PUT'])
@jwt_required()
def update_fee(fee_id):
    """更新费用"""
    fee = OtherFee.query.get(fee_id)
    if not fee:
        return jsonify({'error': '费用不存在'}), 404

    data = request.get_json()
    fee.module_id = data.get('module_id', fee.module_id)
    fee.fee_type = data.get('fee_type', fee.fee_type)
    fee.location = data.get('location', fee.location)
    fee.amount = data.get('amount', fee.amount)
    fee.description = data.get('description', fee.description)

    db.session.commit()
    return jsonify(fee.to_dict()), 200


@fee_bp.route('/fees/<int:fee_id>', methods=['DELETE'])
@jwt_required()
def delete_fee(fee_id):
    """删除费用"""
    fee = OtherFee.query.get(fee_id)
    if not fee:
        return jsonify({'error': '费用不存在'}), 404

    db.session.delete(fee)
    db.session.commit()
    return jsonify({'message': '删除成功'}), 200


@fee_bp.route('/fee-types', methods=['GET'])
@jwt_required()
def get_fee_types():
    """获取费用类型配置"""
    fee_types = FeeType.query.all()
    return jsonify([f.to_dict() for f in fee_types]), 200


@fee_bp.route('/fee-types', methods=['POST'])
@jwt_required()
def create_fee_type():
    """创建费用类型"""
    data = request.get_json()
    fee_type = FeeType(
        name=data.get('name'),
        location=data.get('location'),
        is_active=True
    )
    db.session.add(fee_type)
    db.session.commit()
    return jsonify(fee_type.to_dict()), 201


@fee_bp.route('/fee-types/<int:fee_type_id>', methods=['PUT'])
@jwt_required()
def update_fee_type(fee_type_id):
    """更新费用类型"""
    fee_type = FeeType.query.get(fee_type_id)
    if not fee_type:
        return jsonify({'error': '费用类型不存在'}), 404

    data = request.get_json()
    fee_type.name = data.get('name', fee_type.name)
    fee_type.location = data.get('location', fee_type.location)
    fee_type.is_active = data.get('is_active', fee_type.is_active)

    db.session.commit()
    return jsonify(fee_type.to_dict()), 200


@fee_bp.route('/fee-types/<int:fee_type_id>', methods=['DELETE'])
@jwt_required()
def delete_fee_type(fee_type_id):
    """删除费用类型"""
    fee_type = FeeType.query.get(fee_type_id)
    if not fee_type:
        return jsonify({'error': '费用类型不存在'}), 404

    db.session.delete(fee_type)
    db.session.commit()
    return jsonify({'message': '删除成功'}), 200