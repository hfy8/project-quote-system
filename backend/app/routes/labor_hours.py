from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.labor_hour import LaborHour

labor_hours_bp = Blueprint('labor_hours', __name__, url_prefix='/api/quotations')

@labor_hours_bp.route('/<int:quotation_id>/labor-hours', methods=['GET'])
@jwt_required()
def get_labor_hours(quotation_id):
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
    item = LaborHour.query.filter_by(id=item_id, quotation_id=quotation_id).first()
    if not item:
        return jsonify({'error': 'Not found'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Deleted'}), 200
