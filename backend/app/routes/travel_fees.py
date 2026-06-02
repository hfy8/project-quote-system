from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.models import PackingType, TravelCategory, TravelDayRate, TravelMode, TravelPersonTripFee
from app.utils.permissions import check_permission

travel_fee_bp = Blueprint('travel_fees', __name__, url_prefix='/api')


# ===== 包装类型（系统配置）=====

@travel_fee_bp.route('/packing-types', methods=['GET'])
@jwt_required()
def get_packing_types():
    items = PackingType.query.filter_by(is_active=True).order_by(PackingType.id).all()
    return jsonify([t.to_dict() for t in items]), 200


@travel_fee_bp.route('/packing-types', methods=['POST'])
@jwt_required()
@check_permission('fee_type.create')
def create_packing_type():
    data = request.get_json()
    t = PackingType(
        name=data.get('name'),
        name_en=data.get('name_en'),
        unit_price=data.get('unit_price', 0),
        description=data.get('description'),
        is_active=data.get('is_active', True)
    )
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201


@travel_fee_bp.route('/packing-types/<int:tid>', methods=['PUT'])
@jwt_required()
@check_permission('fee_type.edit')
def update_packing_type(tid):
    t = PackingType.query.get(tid)
    if not t:
        return jsonify({'error': '包装类型不存在'}), 404
    data = request.get_json()
    t.name = data.get('name', t.name)
    t.name_en = data.get('name_en', t.name_en)
    t.unit_price = data.get('unit_price', t.unit_price)
    t.description = data.get('description', t.description)
    t.is_active = data.get('is_active', t.is_active)
    db.session.commit()
    return jsonify(t.to_dict()), 200


@travel_fee_bp.route('/packing-types/<int:tid>', methods=['DELETE'])
@jwt_required()
@check_permission('fee_type.delete')
def delete_packing_type(tid):
    t = PackingType.query.get(tid)
    if not t:
        return jsonify({'error': '包装类型不存在'}), 404
    t.is_active = False
    db.session.commit()
    return jsonify({'message': '已禁用'}), 200


# ===== 差旅分类（系统配置）=====

@travel_fee_bp.route('/travel-categories', methods=['GET'])
@jwt_required()
def get_travel_categories():
    items = TravelCategory.query.filter_by(is_active=True).order_by(TravelCategory.sort_order).all()
    return jsonify([t.to_dict() for t in items]), 200


@travel_fee_bp.route('/travel-categories', methods=['POST'])
@jwt_required()
@check_permission('fee_type.create')
def create_travel_category():
    data = request.get_json()
    t = TravelCategory(
        name=data.get('name'),
        code=data.get('code'),
        description=data.get('description'),
        sort_order=data.get('sort_order', 0),
        is_active=data.get('is_active', True)
    )
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201


@travel_fee_bp.route('/travel-categories/<int:tid>', methods=['PUT'])
@jwt_required()
@check_permission('fee_type.edit')
def update_travel_category(tid):
    t = TravelCategory.query.get(tid)
    if not t:
        return jsonify({'error': '差旅分类不存在'}), 404
    data = request.get_json()
    t.name = data.get('name', t.name)
    t.code = data.get('code', t.code)
    t.description = data.get('description', t.description)
    t.sort_order = data.get('sort_order', t.sort_order)
    t.is_active = data.get('is_active', t.is_active)
    db.session.commit()
    return jsonify(t.to_dict()), 200


@travel_fee_bp.route('/travel-categories/<int:tid>', methods=['DELETE'])
@jwt_required()
@check_permission('fee_type.delete')
def delete_travel_category(tid):
    t = TravelCategory.query.get(tid)
    if not t:
        return jsonify({'error': '差旅分类不存在'}), 404
    t.is_active = False
    db.session.commit()
    return jsonify({'message': '已禁用'}), 200


# ===== 差旅人天单价（系统配置）=====

@travel_fee_bp.route('/travel-day-rates', methods=['GET'])
@jwt_required()
def get_travel_day_rates():
    rates = TravelDayRate.query.filter_by(is_active=True).all()
    return jsonify([r.to_dict() for r in rates]), 200


@travel_fee_bp.route('/travel-day-rates', methods=['POST'])
@jwt_required()
@check_permission('fee_type.create')
def create_travel_day_rate():
    data = request.get_json()
    r = TravelDayRate(
        travel_category_id=data.get('travel_category_id'),
        unit_price=data.get('unit_price', 0),
        currency=data.get('currency', 'CNY'),
        description=data.get('description'),
        is_active=data.get('is_active', True)
    )
    db.session.add(r)
    db.session.commit()
    return jsonify(r.to_dict()), 201


@travel_fee_bp.route('/travel-day-rates/<int:rid>', methods=['PUT'])
@jwt_required()
@check_permission('fee_type.edit')
def update_travel_day_rate(rid):
    r = TravelDayRate.query.get(rid)
    if not r:
        return jsonify({'error': '差旅人天单价不存在'}), 404
    data = request.get_json()
    r.travel_category_id = data.get('travel_category_id', r.travel_category_id)
    r.unit_price = data.get('unit_price', r.unit_price)
    r.currency = data.get('currency', r.currency)
    r.description = data.get('description', r.description)
    r.is_active = data.get('is_active', r.is_active)
    db.session.commit()
    return jsonify(r.to_dict()), 200


@travel_fee_bp.route('/travel-day-rates/<int:rid>', methods=['DELETE'])
@jwt_required()
@check_permission('fee_type.delete')
def delete_travel_day_rate(rid):
    r = TravelDayRate.query.get(rid)
    if not r:
        return jsonify({'error': '差旅人天单价不存在'}), 404
    r.is_active = False
    db.session.commit()
    return jsonify({'message': '已禁用'}), 200


# ===== 出行方式（系统配置）=====

@travel_fee_bp.route('/travel-modes', methods=['GET'])
@jwt_required()
def get_travel_modes():
    items = TravelMode.query.filter_by(is_active=True).all()
    return jsonify([t.to_dict() for t in items]), 200


@travel_fee_bp.route('/travel-modes', methods=['POST'])
@jwt_required()
@check_permission('fee_type.create')
def create_travel_mode():
    data = request.get_json()
    t = TravelMode(
        name=data.get('name'),
        name_en=data.get('name_en'),
        code=data.get('code'),
        description=data.get('description'),
        is_active=data.get('is_active', True)
    )
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201


@travel_fee_bp.route('/travel-modes/<int:tid>', methods=['PUT'])
@jwt_required()
@check_permission('fee_type.edit')
def update_travel_mode(tid):
    t = TravelMode.query.get(tid)
    if not t:
        return jsonify({'error': '出行方式不存在'}), 404
    data = request.get_json()
    t.name = data.get('name', t.name)
    t.name_en = data.get('name_en', t.name_en)
    t.code = data.get('code', t.code)
    t.description = data.get('description', t.description)
    t.is_active = data.get('is_active', t.is_active)
    db.session.commit()
    return jsonify(t.to_dict()), 200


@travel_fee_bp.route('/travel-modes/<int:tid>', methods=['DELETE'])
@jwt_required()
@check_permission('fee_type.delete')
def delete_travel_mode(tid):
    t = TravelMode.query.get(tid)
    if not t:
        return jsonify({'error': '出行方式不存在'}), 404
    t.is_active = False
    db.session.commit()
    return jsonify({'message': '已禁用'}), 200


# ===== 差旅人次单价（系统配置）=====

@travel_fee_bp.route('/travel-person-trip-fees', methods=['GET'])
@jwt_required()
def get_travel_person_trip_fees():
    fees = TravelPersonTripFee.query.filter_by(is_active=True).all()
    return jsonify([f.to_dict() for f in fees]), 200


@travel_fee_bp.route('/travel-person-trip-fees', methods=['POST'])
@jwt_required()
@check_permission('fee_type.create')
def create_travel_person_trip_fee():
    data = request.get_json()
    f = TravelPersonTripFee(
        travel_category_id=data.get('travel_category_id'),
        travel_mode_id=data.get('travel_mode_id'),
        unit_price=data.get('unit_price', 0),
        visa_fee=data.get('visa_fee', 0),
        currency=data.get('currency', 'CNY'),
        description=data.get('description'),
        is_active=data.get('is_active', True)
    )
    db.session.add(f)
    db.session.commit()
    return jsonify(f.to_dict()), 201


@travel_fee_bp.route('/travel-person-trip-fees/<int:fid>', methods=['PUT'])
@jwt_required()
@check_permission('fee_type.edit')
def update_travel_person_trip_fee(fid):
    f = TravelPersonTripFee.query.get(fid)
    if not f:
        return jsonify({'error': '差旅人次单价不存在'}), 404
    data = request.get_json()
    f.travel_category_id = data.get('travel_category_id', f.travel_category_id)
    f.travel_mode_id = data.get('travel_mode_id', f.travel_mode_id)
    f.unit_price = data.get('unit_price', f.unit_price)
    f.visa_fee = data.get('visa_fee', f.visa_fee)
    f.currency = data.get('currency', f.currency)
    f.description = data.get('description', f.description)
    f.is_active = data.get('is_active', f.is_active)
    db.session.commit()
    return jsonify(f.to_dict()), 200


@travel_fee_bp.route('/travel-person-trip-fees/<int:fid>', methods=['DELETE'])
@jwt_required()
@check_permission('fee_type.delete')
def delete_travel_person_trip_fee(fid):
    f = TravelPersonTripFee.query.get(fid)
    if not f:
        return jsonify({'error': '差旅人次单价不存在'}), 404
    f.is_active = False
    db.session.commit()
    return jsonify({'message': '已禁用'}), 200
