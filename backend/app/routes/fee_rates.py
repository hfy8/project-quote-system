from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.fee_rate import FeeRate
from app.utils.permissions import check_permission


fee_rate_bp = Blueprint('fee_rates', __name__, url_prefix='/api/fee_rates')


@fee_rate_bp.route('', methods=['GET'])
@jwt_required()
def get_fee_rates():
    """获取所有费用系数配置"""
    rates = FeeRate.query.all()
    return jsonify([r.to_dict() for r in rates]), 200


@fee_rate_bp.route('', methods=['POST'])
@jwt_required()
def create_fee_rate():
    """创建费用系数配置"""
    data = request.get_json()
    rate = FeeRate(
        category=data.get('category'),
        rate=data.get('rate', 1.0),
        description=data.get('description')
    )
    db.session.add(rate)
    db.session.commit()
    return jsonify(rate.to_dict()), 201


@fee_rate_bp.route('/<int:rate_id>', methods=['PUT'])
@jwt_required()
@check_permission('fee_rate.edit')
def update_fee_rate(rate_id):
    """更新费用系数配置"""
    rate = FeeRate.query.get(rate_id)
    if not rate:
        return jsonify({'error': '费用系数不存在'}), 404
    
    data = request.get_json()
    rate.category = data.get('category', rate.category)
    rate.rate = data.get('rate', rate.rate)
    rate.description = data.get('description', rate.description)
    
    db.session.commit()
    return jsonify(rate.to_dict()), 200


@fee_rate_bp.route('/<int:rate_id>', methods=['DELETE'])
@jwt_required()
def delete_fee_rate(rate_id):
    """删除费用系数配置"""
    rate = FeeRate.query.get(rate_id)
    if not rate:
        return jsonify({'error': '费用系数不存在'}), 404
    
    db.session.delete(rate)
    db.session.commit()
    return jsonify({'message': '删除成功'}), 200


@fee_rate_bp.route('/category/<string:category>', methods=['GET'])
@jwt_required()
def get_fee_rate_by_category(category):
    """根据分类获取费用系数"""
    rate = FeeRate.query.filter_by(category=category).first()
    if not rate:
        return jsonify({'error': '未找到该分类的费用系数', 'rate': 1.0}), 200
    return jsonify(rate.to_dict()), 200
