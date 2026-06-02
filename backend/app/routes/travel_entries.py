from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.models import PackingEntry, TravelPersonDays, TravelPersonTrip, TravelPersonTripFee, TravelCategory
from app.utils.permissions import check_permission

travel_entry_bp = Blueprint('travel_entries', __name__, url_prefix='/api')


# ===== 包装条目（项目层）=====

@travel_entry_bp.route('/packing-entries', methods=['GET'])
@jwt_required()
def get_packing_entries():
    """获取某报价单的包装条目"""
    quotation_id = request.args.get('quotation_id')
    if not quotation_id:
        return jsonify({'error': 'quotation_id is required'}), 400
    items = PackingEntry.query.filter_by(quotation_id=int(quotation_id)).all()
    return jsonify([e.to_dict() for e in items]), 200


@travel_entry_bp.route('/packing-entries', methods=['POST'])
@jwt_required()
@check_permission('quotation.edit')
def upsert_packing_entry():
    """创建或更新包装条目（按 quotation_id + packing_type_id 唯一）"""
    data = request.get_json()
    quotation_id = data.get('quotation_id')
    packing_type_id = data.get('packing_type_id')
    if not quotation_id or not packing_type_id:
        return jsonify({'error': 'quotation_id and packing_type_id are required'}), 400

    entry = PackingEntry.query.filter_by(
        quotation_id=int(quotation_id),
        packing_type_id=int(packing_type_id)
    ).first()

    if entry:
        entry.quantity = data.get('quantity', entry.quantity)
        entry.remark = data.get('remark', entry.remark)
    else:
        entry = PackingEntry(
            quotation_id=int(quotation_id),
            packing_type_id=int(packing_type_id),
            quantity=data.get('quantity', 0),
            remark=data.get('remark')
        )
        db.session.add(entry)

    db.session.commit()
    return jsonify(entry.to_dict()), 200


@travel_entry_bp.route('/packing-entries/<int:eid>', methods=['DELETE'])
@jwt_required()
@check_permission('quotation.edit')
def delete_packing_entry(eid):
    entry = PackingEntry.query.get(eid)
    if not entry:
        return jsonify({'error': '包装条目不存在'}), 404
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'message': '删除成功'}), 200


# ===== 差旅人天条目（项目层）=====

@travel_entry_bp.route('/travel-person-days', methods=['GET'])
@jwt_required()
def get_travel_person_days():
    quotation_id = request.args.get('quotation_id')
    if not quotation_id:
        return jsonify({'error': 'quotation_id is required'}), 400
    items = TravelPersonDays.query.filter_by(quotation_id=int(quotation_id)).all()
    return jsonify([e.to_dict() for e in items]), 200


@travel_entry_bp.route('/travel-person-days', methods=['POST'])
@jwt_required()
@check_permission('quotation.edit')
def upsert_travel_person_days():
    """创建或更新差旅人天条目（按 quotation_id + travel_category_id 唯一）"""
    data = request.get_json()
    quotation_id = data.get('quotation_id')
    travel_category_id = data.get('travel_category_id')
    if not quotation_id or not travel_category_id:
        return jsonify({'error': 'quotation_id and travel_category_id are required'}), 400

    entry = TravelPersonDays.query.filter_by(
        quotation_id=int(quotation_id),
        travel_category_id=int(travel_category_id)
    ).first()

    if entry:
        entry.person_days = data.get('person_days', entry.person_days)
        entry.remark = data.get('remark', entry.remark)
    else:
        entry = TravelPersonDays(
            quotation_id=int(quotation_id),
            travel_category_id=int(travel_category_id),
            person_days=data.get('person_days', 0),
            remark=data.get('remark')
        )
        db.session.add(entry)

    db.session.commit()
    return jsonify(entry.to_dict()), 200


@travel_entry_bp.route('/travel-person-days/<int:eid>', methods=['DELETE'])
@jwt_required()
@check_permission('quotation.edit')
def delete_travel_person_days(eid):
    entry = TravelPersonDays.query.get(eid)
    if not entry:
        return jsonify({'error': '差旅人天条目不存在'}), 404
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'message': '删除成功'}), 200


# ===== 差旅人次条目（项目层）=====

@travel_entry_bp.route('/travel-person-trips', methods=['GET'])
@jwt_required()
def get_travel_person_trips():
    quotation_id = request.args.get('quotation_id')
    if not quotation_id:
        return jsonify({'error': 'quotation_id is required'}), 400

    trips = TravelPersonTrip.query.filter_by(quotation_id=int(quotation_id)).all()
    result = []
    for trip in trips:
        d = trip.to_dict()
        # 附加单价信息（从系统配置表查）
        fee = TravelPersonTripFee.query.filter_by(
            travel_category_id=trip.travel_category_id,
            travel_mode_id=trip.travel_mode_id,
            is_active=True
        ).first()
        if fee:
            d['unit_price'] = float(fee.unit_price) if fee.unit_price else 0
            d['visa_fee'] = float(fee.visa_fee) if fee.visa_fee else 0
            d['subtotal'] = d['person_count'] * d['unit_price']
            # 非国内分类（code != 'domestic'）才加签证费
            cat = TravelCategory.query.get(trip.travel_category_id)
            if cat and cat.code != 'domestic':
                d['subtotal'] += d['person_count'] * d['visa_fee']
        result.append(d)
    return jsonify(result), 200


@travel_entry_bp.route('/travel-person-trips', methods=['POST'])
@jwt_required()
@check_permission('quotation.edit')
def upsert_travel_person_trip():
    """创建或更新差旅人次条目（按 quotation_id + travel_category_id + travel_mode_id 唯一）"""
    data = request.get_json()
    quotation_id = data.get('quotation_id')
    travel_category_id = data.get('travel_category_id')
    travel_mode_id = data.get('travel_mode_id')
    if not all([quotation_id, travel_category_id, travel_mode_id]):
        return jsonify({'error': 'quotation_id, travel_category_id, travel_mode_id are required'}), 400

    trip = TravelPersonTrip.query.filter_by(
        quotation_id=int(quotation_id),
        travel_category_id=int(travel_category_id),
        travel_mode_id=int(travel_mode_id)
    ).first()

    if trip:
        trip.person_count = data.get('person_count', trip.person_count)
        trip.remark = data.get('remark', trip.remark)
    else:
        trip = TravelPersonTrip(
            quotation_id=int(quotation_id),
            travel_category_id=int(travel_category_id),
            travel_mode_id=int(travel_mode_id),
            person_count=data.get('person_count', 0),
            remark=data.get('remark')
        )
        db.session.add(trip)

    db.session.commit()
    return jsonify(trip.to_dict()), 200


@travel_entry_bp.route('/travel-person-trips/<int:tid>', methods=['DELETE'])
@jwt_required()
@check_permission('quotation.edit')
def delete_travel_person_trip(tid):
    trip = TravelPersonTrip.query.get(tid)
    if not trip:
        return jsonify({'error': '差旅人次条目不存在'}), 404
    db.session.delete(trip)
    db.session.commit()
    return jsonify({'message': '删除成功'}), 200
