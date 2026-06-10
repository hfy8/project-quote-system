from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.labor_hour import LaborHour
from app.models.quotation import Quotation

labor_hours_bp = Blueprint('labor_hours', __name__, url_prefix='/api/quotations')

@labor_hours_bp.route('/<int:quotation_id>/labor-hours', methods=['GET'])
@jwt_required()
def get_labor_hours(quotation_id):
    quotation = Quotation.query.get(quotation_id)
    if not quotation:
        return jsonify({'error': 'Not found'}), 404

    # 线体报价单：聚合所有子报价单的人力项
    if quotation.type == 'line':
        child_ids = [c.id for c in quotation.children]
        all_ids = [quotation_id] + child_ids
        items = LaborHour.query.filter(LaborHour.quotation_id.in_(all_ids)).all()
        q_map = {q.id: q.name for q in Quotation.query.filter(Quotation.id.in_(all_ids)).all()}
        result = []
        for r in items:
            d = r.to_dict()
            d['quotation_name'] = q_map.get(r.quotation_id, '')
            result.append(d)
        return jsonify(result), 200

    # 普通报价单：只查自己的
    items = LaborHour.query.filter_by(quotation_id=quotation_id).all()
    return jsonify([r.to_dict() for r in items]), 200

@labor_hours_bp.route('/<int:quotation_id>/labor-hours', methods=['POST'])
@jwt_required()
def create_labor_hour(quotation_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    name = data.get('name', '')
    hours = float(data.get('hours', 0) or 0)
    unit_price = float(data.get('unit_price', 0) or 0)
    total = hours * unit_price

    item = LaborHour(
        quotation_id=quotation_id,
        name=name,
        hours=hours,
        unit_price=unit_price,
        total=total,
        created_by=user_id
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@labor_hours_bp.route('/<int:quotation_id>/labor-hours/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_labor_hour(quotation_id, item_id):
    data = request.get_json()
    # 支持线体报价单：line 类型时允许子报价单的人力工时
    quotation = Quotation.query.get(quotation_id)
    if quotation and quotation.type == 'line':
        child_ids = [c.id for c in quotation.children]
        all_ids = [quotation_id] + child_ids
        item = LaborHour.query.filter(LaborHour.id == item_id, LaborHour.quotation_id.in_(all_ids)).first()
    else:
        item = LaborHour.query.filter_by(id=item_id, quotation_id=quotation_id).first()
    if not item:
        return jsonify({'error': 'Not found'}), 404

    if 'name' in data:
        item.name = data['name']
    if 'hours' in data:
        item.hours = float(data['hours'] or 0)
    if 'unit_price' in data:
        item.unit_price = float(data['unit_price'] or 0)
    item.total = item.hours * item.unit_price

    db.session.commit()
    return jsonify(item.to_dict()), 200

@labor_hours_bp.route('/<int:quotation_id>/labor-hours/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_labor_hour(quotation_id, item_id):
    # 支持线体报价单：line 类型时允许子报价单的人力工时
    quotation = Quotation.query.get(quotation_id)
    if quotation and quotation.type == 'line':
        child_ids = [c.id for c in quotation.children]
        all_ids = [quotation_id] + child_ids
        item = LaborHour.query.filter(LaborHour.id == item_id, LaborHour.quotation_id.in_(all_ids)).first()
    else:
        item = LaborHour.query.filter_by(id=item_id, quotation_id=quotation_id).first()
    if not item:
        return jsonify({'error': 'Not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200
