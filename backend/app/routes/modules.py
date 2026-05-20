from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Module, ModuleParticipant, Material, ModuleMaterial
from app.utils.permissions import check_permission


module_bp = Blueprint('modules', __name__)


@module_bp.route('/quotations/<int:quotation_id>/modules', methods=['GET'])
@jwt_required()
def get_modules(quotation_id):
    """获取模块列表"""
    modules = Module.query.filter_by(quotation_id=quotation_id).all()
    return jsonify([m.to_dict() for m in modules]), 200


@module_bp.route('/quotations/<int:quotation_id>/modules', methods=['POST'])
@jwt_required()
@check_permission('module.create')
def create_module(quotation_id):
    """创建模块"""
    data = request.get_json()
    module = Module(
        quotation_id=quotation_id,
        name=data.get('name'),
        code=data.get('code'),
        description=data.get('description')
    )
    db.session.add(module)
    db.session.commit()
    return jsonify(module.to_dict()), 201


@module_bp.route('/modules/<int:module_id>', methods=['GET'])
@jwt_required()
def get_module(module_id):
    """获取模块详情"""
    module = Module.query.get(module_id)
    if not module:
        return jsonify({'error': '模块不存在'}), 404
    return jsonify(module.to_dict()), 200


@module_bp.route('/modules/<int:module_id>', methods=['PUT'])
@jwt_required()
@check_permission('module.edit')
def update_module(module_id):
    """更新模块"""
    module = Module.query.get(module_id)
    if not module:
        return jsonify({'error': '模块不存在'}), 404

    data = request.get_json()
    module.name = data.get('name', module.name)
    module.code = data.get('code', module.code)
    module.description = data.get('description', module.description)
    db.session.commit()
    return jsonify(module.to_dict()), 200


@module_bp.route('/modules/<int:module_id>', methods=['DELETE'])
@jwt_required()
@check_permission('module.delete')
def delete_module(module_id):
    """删除模块"""
    module = Module.query.get(module_id)
    if not module:
        return jsonify({'error': '模块不存在'}), 404

    db.session.delete(module)
    db.session.commit()
    return jsonify({'message': '删除成功'}), 200


@module_bp.route('/modules/<int:module_id>/materials', methods=['GET'])
@jwt_required()
def get_module_materials(module_id):
    """获取模块物料列表"""
    materials = ModuleMaterial.query.filter_by(module_id=module_id).all()
    return jsonify([m.to_dict() for m in materials]), 200


@module_bp.route('/modules/<int:module_id>/materials', methods=['POST'])
@jwt_required()
def add_material_to_module(module_id):
    """添加物料到模块"""
    data = request.get_json()
    user_id = get_jwt_identity()

    module_material = ModuleMaterial(
        module_id=module_id,
        material_id=data.get('material_id'),
        quantity=data.get('quantity', 1),
        selected_by_id=user_id
    )
    db.session.add(module_material)
    db.session.commit()
    return jsonify(module_material.to_dict()), 201


@module_bp.route('/module_materials/<int:id>', methods=['PUT'])
@jwt_required()
def update_module_material(id):
    """更新模块物料"""
    module_material = ModuleMaterial.query.get(id)
    if not module_material:
        return jsonify({'error': '模块物料不存在'}), 404

    data = request.get_json()
    module_material.quantity = data.get('quantity', module_material.quantity)
    db.session.commit()
    return jsonify(module_material.to_dict()), 200


@module_bp.route('/module_materials/<int:id>', methods=['DELETE'])
@jwt_required()
def remove_module_material(id):
    """从模块移除物料"""
    module_material = ModuleMaterial.query.get(id)
    if not module_material:
        return jsonify({'error': '模块物料不存在'}), 404

    db.session.delete(module_material)
    db.session.commit()
    return jsonify({'message': '移除成功'}), 200


@module_bp.route('/modules/<int:module_id>/summary', methods=['GET'])
@jwt_required()
def get_module_summary(module_id):
    """获取模块物料汇总"""
    materials = ModuleMaterial.query.filter_by(module_id=module_id).all()
    summary = {
        'total_quantity': sum(m.quantity for m in materials),
        'total_amount': sum(m.quantity * float(m.material.unit_price) for m in materials if m.material),
        'materials': [m.to_dict() for m in materials]
    }
    return jsonify(summary), 200