from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.models import Material, ModuleMaterial
from app.utils.permissions import check_permission, check_any_permission

material_bp = Blueprint('materials', __name__)


@material_bp.route('', methods=['GET'])
@jwt_required()
def get_materials():
    """获取物料列表"""
    keyword = request.args.get('keyword', '')
    category = request.args.get('category')
    status = request.args.get('status')

    query = Material.query
    if keyword:
        keyword_filter = f'%{keyword}%'
        query = query.filter(
            db.or_(
                Material.name.ilike(keyword_filter),
                Material.spec.ilike(keyword_filter),
                Material.brand.ilike(keyword_filter)
            )
        )
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)

    materials = query.all()
    return jsonify([m.to_dict() for m in materials]), 200


@material_bp.route('', methods=['POST'])
@jwt_required()
@check_permission('material.*')
def create_material():
    """创建物料"""
    data = request.get_json()
    material = Material(
        name=data.get('name'),
        spec=data.get('spec'),
        brand=data.get('brand'),
        unit=data.get('unit'),
        unit_price=data.get('unit_price', 0),
        category=data.get('category', 'standard'),
        status='active'
    )
    db.session.add(material)
    db.session.commit()
    return jsonify(material.to_dict()), 201


@material_bp.route('/<int:material_id>', methods=['PUT'])
@jwt_required()
@check_permission('material.*')
def update_material(material_id):
    """更新物料"""
    material = Material.query.get(material_id)
    if not material:
        return jsonify({'error': '物料不存在'}), 404

    data = request.get_json()
    material.name = data.get('name', material.name)
    material.spec = data.get('spec', material.spec)
    material.brand = data.get('brand', material.brand)
    material.unit = data.get('unit', material.unit)
    material.unit_price = data.get('unit_price', material.unit_price)
    material.category = data.get('category', material.category)

    db.session.commit()
    return jsonify(material.to_dict()), 200


@material_bp.route('/<int:material_id>', methods=['DELETE'])
@jwt_required()
@check_permission('material.*')
def delete_material(material_id):
    """删除物料"""
    material = Material.query.get(material_id)
    if not material:
        return jsonify({'error': '物料不存在'}), 404
    
    # 先删除关联的 module_materials 记录
    ModuleMaterial.query.filter_by(material_id=material_id).delete()
    
    db.session.delete(material)
    db.session.commit()
    return jsonify({'message': '删除成功'}), 200


@material_bp.route('/<int:material_id>/toggle', methods=['PUT'])
@jwt_required()
@check_permission('material.*')
def toggle_material(material_id):
    """启用/禁用物料"""
    material = Material.query.get(material_id)
    if not material:
        return jsonify({'error': '物料不存在'}), 404

    material.status = 'inactive' if material.status == 'active' else 'active'
    db.session.commit()
    return jsonify(material.to_dict()), 200


@material_bp.route('/import', methods=['POST'])
@jwt_required()
@check_permission('material.*')
def import_materials():
    """批量导入物料"""
    data = request.get_json()
    materials_data = data.get('materials', [])

    created = []
    for m_data in materials_data:
        material = Material(
            name=m_data.get('name'),
            spec=m_data.get('spec'),
            brand=m_data.get('brand'),
            unit=m_data.get('unit'),
            unit_price=m_data.get('unit_price', 0),
            category=m_data.get('category', 'standard'),
            status='active'
        )
        db.session.add(material)
        created.append(material)

    db.session.commit()
    return jsonify({'created': len(created), 'materials': [m.to_dict() for m in created]}), 201