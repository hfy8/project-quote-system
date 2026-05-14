from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.exchange_rate import ExchangeRate

exchange_rate_bp = Blueprint('exchange_rates', __name__, url_prefix='/api/exchange_rates')


@exchange_rate_bp.route('', methods=['GET'])
@jwt_required()
def get_exchange_rates():
    """获取所有汇率配置"""
    rates = ExchangeRate.query.all()
    return jsonify([r.to_dict() for r in rates]), 200


@exchange_rate_bp.route('/base', methods=['GET'])
@jwt_required()
def get_base_currency():
    """获取基准货币"""
    base = ExchangeRate.query.filter_by(is_base=True).first()
    if not base:
        return jsonify({'currency': 'CNY', 'rate': 1.0, 'is_base': True}), 200
    return jsonify(base.to_dict()), 200


@exchange_rate_bp.route('', methods=['POST'])
@jwt_required()
def create_exchange_rate():
    """创建汇率配置"""
    from app.utils.logger import log_operation
    
    data = request.get_json()
    user_id = get_jwt_identity()
    
    # 如果是基准货币，先取消其他基准并重新计算汇率
    if data.get('is_base'):
        # 重新计算所有汇率：以新基准货币的汇率为基准
        old_base = ExchangeRate.query.filter_by(is_base=True).first()
        new_base_currency = data.get('currency')
        new_base_rate = float(data.get('rate', 1.0))
        
        # 取消所有现有基准
        ExchangeRate.query.filter_by(is_base=True).update({'is_base': False})
        
        # 如果旧基准存在，计算比例并更新所有货币汇率
        if old_base and old_base.currency != new_base_currency:
            old_rate_value = old_base.rate  # 旧基准的汇率值（如 USD=7.2）
            new_rate_value = new_base_rate  # 新基准的汇率值（如 CNY=1）
            
            # 更新所有其他货币的汇率 = 原汇率 / 旧基准汇率 * 新基准汇率
            for rate in ExchangeRate.query.filter(ExchangeRate.currency != new_base_currency).all():
                rate.rate = round(rate.rate / old_rate_value * new_rate_value, 6)
        
        db.session.commit()
        
        rate = ExchangeRate(
            currency=new_base_currency,
            rate=1.0,  # 基准货币固定为1
            is_base=True,
            description=data.get('description')
        )
        db.session.add(rate)
        db.session.commit()
        
        log_operation(user_id, 'create', 'exchange_rate', f'设置基准货币 "{new_base_currency}"')
        return jsonify(rate.to_dict()), 201
    
    rate = ExchangeRate(
        currency=data.get('currency'),
        rate=data.get('rate', 1.0),
        is_base=False,
        description=data.get('description')
    )
    db.session.add(rate)
    db.session.commit()
    return jsonify(rate.to_dict()), 201


@exchange_rate_bp.route('/<int:rate_id>', methods=['PUT'])
@jwt_required()
def update_exchange_rate(rate_id):
    """更新汇率配置"""
    from app.utils.logger import log_operation
    
    rate = ExchangeRate.query.get(rate_id)
    if not rate:
        return jsonify({'error': '汇率不存在'}), 404
    
    data = request.get_json()
    user_id = get_jwt_identity()
    
    # 如果设置为基准货币
    if data.get('is_base') and not rate.is_base:
        # 重新计算所有汇率
        old_base = ExchangeRate.query.filter_by(is_base=True).first()
        new_base_currency = rate.currency
        new_base_rate = float(data.get('rate', 1.0))
        
        # 取消所有现有基准
        ExchangeRate.query.filter(ExchangeRate.id != rate_id).filter_by(is_base=True).update({'is_base': False})
        
        # 如果旧基准存在，计算比例并更新所有货币汇率
        if old_base and old_base.currency != new_base_currency:
            old_rate_value = old_base.rate
            new_rate_value = new_base_rate
            
            # 更新所有其他货币的汇率
            for r in ExchangeRate.query.filter(ExchangeRate.currency != new_base_currency).all():
                r.rate = round(r.rate / old_rate_value * new_rate_value, 6)
        
        rate.is_base = True
        rate.rate = 1.0  # 基准货币固定为1
        db.session.commit()
        
        log_operation(user_id, 'update', 'exchange_rate', f'设置基准货币为 "{new_base_currency}"')
        return jsonify(rate.to_dict()), 200
    
    # 普通更新
    if 'rate' in data:
        rate.rate = data.get('rate')
    if 'description' in data:
        rate.description = data.get('description')
    
    db.session.commit()
    return jsonify(rate.to_dict()), 200


@exchange_rate_bp.route('/<int:rate_id>/set-base', methods=['POST'])
@jwt_required()
def set_base_currency(rate_id):
    """设置基准货币（专用接口，需要管理员权限）"""
    from app.utils.logger import log_operation
    from app.utils.permissions import check_permission
    
    # 管理员权限检查
    try:
        check_permission('exchange_rate.*')
    except:
        return jsonify({'error': '需要管理员权限'}), 403
    
    rate = ExchangeRate.query.get(rate_id)
    if not rate:
        return jsonify({'error': '汇率不存在'}), 404
    
    user_id = get_jwt_identity()
    old_base = ExchangeRate.query.filter_by(is_base=True).first()
    new_base_currency = rate.currency
    
    # 获取新基准货币原来的汇率值（用于计算比例）
    # 注意：如果新基准之前就是基准，则它当前的 rate 就是 1.0
    new_base_old_rate = rate.rate
    
    # 取消所有现有基准，并计算比例
    ExchangeRate.query.filter_by(is_base=True).update({'is_base': False})
    
    # 计算比例并更新所有货币汇率
    # 公式：其他货币的新汇率 = 原汇率 / 新基准的原汇率
    # 例如：EUR=7.8, USD=7.1, CNY=1.0 (旧基准是CNY)
    # 设置USD为新基准：USD的旧汇率=7.1
    # EUR新汇率 = 7.8 / 7.1 = 1.0986
    # CNY新汇率 = 1.0 / 7.1 = 0.1408
    if old_base and old_base.currency != new_base_currency:
        for r in ExchangeRate.query.filter(ExchangeRate.currency != new_base_currency).all():
            r.rate = round(r.rate / new_base_old_rate, 6)
            db.session.add(r)
    
    rate.is_base = True
    rate.rate = 1.0  # 基准货币固定为1
    db.session.add(rate)
    db.session.commit()
    
    log_operation(user_id, 'update', 'exchange_rate', f'设置基准货币为 "{new_base_currency}"')
    return jsonify(rate.to_dict()), 200


@exchange_rate_bp.route('/<int:rate_id>', methods=['DELETE'])
@jwt_required()
def delete_exchange_rate(rate_id):
    """删除汇率配置"""
    rate = ExchangeRate.query.get(rate_id)
    if not rate:
        return jsonify({'error': '汇率不存在'}), 404
    
    db.session.delete(rate)
    db.session.commit()
    return jsonify({'message': '删除成功'}), 200


@exchange_rate_bp.route('/convert', methods=['GET'])
@jwt_required()
def convert_currency():
    """货币转换"""
    from_currency = request.args.get('from', 'CNY')
    to_currency = request.args.get('to', 'CNY')
    amount = float(request.args.get('amount', 0))
    
    from_rate = ExchangeRate.query.filter_by(currency=from_currency).first()
    to_rate = ExchangeRate.query.filter_by(currency=to_currency).first()
    
    if not from_rate or not to_rate:
        return jsonify({'error': '货币代码不存在'}), 400
    
    # 转换为基准货币，再转换为目标货币
    base_amount = amount / from_rate.rate
    result = base_amount * to_rate.rate
    
    return jsonify({
        'from': from_currency,
        'to': to_currency,
        'amount': amount,
        'result': round(result, 2),
        'rate': round(to_rate.rate / from_rate.rate, 4)
    }), 200
