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
def create_module(quotation_id):
    """创建模块 - 需有权限或是报价单参与人"""
    from app.models import User, QuotationParticipant
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 401
    # 检查是否有 module.create 权限
    from app.utils.permissions import has_permission
    if not has_permission(user.role, 'module.create'):
        # 检查是否是报价单参与人
        participant = QuotationParticipant.query.filter_by(
            quotation_id=quotation_id, user_id=user_id
        ).first()
        if not participant:
            return jsonify({'error': '没有权限'}), 403

    data = request.get_json()
    module = Module(
        quotation_id=quotation_id,
        name=data.get('name'),
        name_en=data.get('name_en'),
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
    module.name_en = data.get('name_en', module.name_en)
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
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 200, type=int)
    query = ModuleMaterial.query.filter_by(module_id=module_id)
    total = query.count()
    materials = query.offset((page - 1) * page_size).limit(page_size).all()
    return jsonify({
        'items': [m.to_dict() for m in materials],
        'total': total,
        'page': page,
        'page_size': page_size
    }), 200


@module_bp.route('/modules/<int:module_id>/materials', methods=['POST'])
@jwt_required()
def add_material_to_module(module_id):
    """添加物料到模块"""
    data = request.get_json()
    user_id = get_jwt_identity()
    material_id = data.get('material_id')
    quantity = data.get('quantity', 1)

    # 检查该模块是否已添加过"其他"物料（按名称查，避免硬编码ID）
    other_material = db.session.execute(db.text(
        "SELECT id FROM materials WHERE name = '其他' LIMIT 1"
    )).fetchone()
    other_material_id = other_material[0] if other_material else None
    is_other = (other_material_id and material_id == other_material_id)
    if is_other:
        existing = db.session.execute(db.text('''
            SELECT id FROM module_materials
            WHERE module_id = :mid AND material_id = :mid2
            LIMIT 1
        '''), {'mid': module_id, 'mid2': other_material_id}).fetchone()
        if existing:
            return jsonify({'error': '该模块已添加"其他"物料，请直接修改其单价'}), 400

    module_material = ModuleMaterial(
        module_id=module_id,
        material_id=material_id,
        is_other=is_other,
        quantity=1 if is_other else quantity,
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
    if module_material.is_other and data.get('unit_price_override') is not None:
        module_material.unit_price_override = data.get('unit_price_override')
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
        'total_amount': sum(
            float(m.unit_price_override) if m.is_other and m.unit_price_override
            else m.quantity * float(m.material.unit_price) if m.material and m.material.unit_price
            else 0
            for m in materials
        ),
        'materials': [m.to_dict() for m in materials]
    }
    return jsonify(summary), 200


@module_bp.route('/quotations/<int:quotation_id>/all-modules', methods=['GET'])
@jwt_required()
def get_all_modules(quotation_id):
    """获取线体报价单的所有子报价单模块（聚合）"""
    from app.models import Quotation, Module
    # 检查报价单是否为线体
    quotation = Quotation.query.get(quotation_id)
    if not quotation:
        return jsonify({'error': '报价单不存在'}), 404

    # 获取所有子报价单的ID
    child_ids = [c.id for c in quotation.children.all()]

    # 获取线体自身的模块 + 所有子报价单的模块
    all_module_ids = [quotation_id] + child_ids
    modules = Module.query.filter(Module.quotation_id.in_(all_module_ids)).all()

    # 按子报价单分组，每个模块带上 quotation_id 和 quotation_name
    result = []
    for mod in modules:
        mod_dict = mod.to_dict()
        # 找到所属的子报价单信息
        if mod.quotation_id == quotation_id:
            mod_dict['quotation_name'] = quotation.name + '（线体）'
        else:
            child_q = Quotation.query.get(mod.quotation_id)
            mod_dict['quotation_name'] = child_q.name if child_q else f'子报价单{mod.quotation_id}'
        result.append(mod_dict)

    return jsonify(result), 200