from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import VersionSnapshot, Quotation
import json
from app.utils.permissions import check_permission


version_bp = Blueprint('versions', __name__)


@version_bp.route('/quotations/<int:quotation_id>/versions', methods=['GET'])
@jwt_required()
def get_versions(quotation_id):
    """获取版本列表"""
    versions = VersionSnapshot.query.filter_by(quotation_id=quotation_id).order_by(VersionSnapshot.version_no.desc()).all()
    return jsonify([v.to_dict() for v in versions]), 200


@version_bp.route('/quotations/<int:quotation_id>/versions', methods=['POST'])
@jwt_required()
@check_permission('version.create')
def create_version(quotation_id):
    """创建版本快照"""
    user_id = get_jwt_identity()
    data = request.get_json()

    # 获取下一个版本号
    last_version = VersionSnapshot.query.filter_by(quotation_id=quotation_id).order_by(VersionSnapshot.version_no.desc()).first()
    next_version = (last_version.version_no + 1) if last_version else 1

    # 构建快照数据
    quotation = Quotation.query.get(quotation_id)
    snapshot_data = {
        'quotation': {
            'name': quotation.name,
            'type': quotation.type,
            'scheme_no': quotation.scheme_no,
            'tax_rate': quotation.tax_rate,
            'currency': quotation.currency,
            'business_owner_id': quotation.business_owner_id,
            'business_owner_name': quotation.business_owner.real_name if quotation.business_owner else None,
            'creator_id': quotation.creator_id,
            'creator_name': quotation.creator.real_name if quotation.creator else None,
        },
        'modules': [m.to_dict() for m in quotation.modules],
        'fees': [f.to_dict() for f in quotation.fees],
    }

    version = VersionSnapshot(
        quotation_id=quotation_id,
        version_no=next_version,
        snapshot_data=json.dumps(snapshot_data),
        operation_type=data.get('operation_type', 'manual'),
        remark=data.get('remark'),
        operator_id=user_id
    )
    db.session.add(version)
    db.session.commit()
    return jsonify(version.to_dict()), 201


@version_bp.route('/versions/<int:version_id>', methods=['GET'])
@jwt_required()
def get_version(version_id):
    """获取版本详情"""
    version = VersionSnapshot.query.get(version_id)
    if not version:
        return jsonify({'error': '版本不存在'}), 404

    snapshot = json.loads(version.snapshot_data)
    result = version.to_dict()
    # 确保快照数据包含 quotation, modules, fees 顶层结构
    # 旧格式: {name, type, modules, fees} - 需要包装
    # 新格式: {quotation, modules, fees} - 直接使用
    if 'quotation' not in snapshot:
        if 'modules' in snapshot or 'fees' in snapshot:
            # 旧格式：modules和fees在顶层，需要包装到quotation下
            snapshot = {
                'quotation': snapshot,
                'modules': snapshot.get('modules', []),
                'fees': snapshot.get('fees', [])
            }
        else:
            # 无法识别的格式
            snapshot = {'quotation': snapshot, 'modules': [], 'fees': []}
    result['snapshot_data'] = snapshot
    return jsonify(result), 200


@version_bp.route('/versions/<int:version_id>/rollback', methods=['POST'])
@jwt_required()
def rollback_version(version_id):
    """回退到指定版本"""
    version = VersionSnapshot.query.get(version_id)
    if not version:
        return jsonify({'error': '版本不存在'}), 404

    # 创建新版本记录回退操作
    user_id = get_jwt_identity()
    last_version = VersionSnapshot.query.filter_by(quotation_id=version.quotation_id).order_by(VersionSnapshot.version_no.desc()).first()
    next_version = (last_version.version_no + 1) if last_version else 1

    rollback_version = VersionSnapshot(
        quotation_id=version.quotation_id,
        version_no=next_version,
        snapshot_data=version.snapshot_data,
        operation_type='rollback',
        remark=f'回退到版本 {version.version_no}',
        operator_id=user_id
    )
    db.session.add(rollback_version)
    db.session.commit()
    return jsonify(rollback_version.to_dict()), 201


@version_bp.route('/versions/<int:version_id>/compare/<int:other_id>', methods=['GET'])
@jwt_required()
def compare_versions(version_id, other_id):
    """对比两个版本"""
    version1 = VersionSnapshot.query.get(version_id)
    version2 = VersionSnapshot.query.get(other_id)

    if not version1 or not version2:
        return jsonify({'error': '版本不存在'}), 404

    def normalize(snapshot):
        """统一快照数据格式：确保 {quotation, modules, fees} 顶层结构"""
        if 'quotation' in snapshot:
            return snapshot
        if 'modules' in snapshot or 'fees' in snapshot:
            coeff = snapshot.get('coefficients')
            return {
                'quotation': snapshot,
                'modules': snapshot.get('modules', []),
                'fees': snapshot.get('fees', []),
                'labor_hours': snapshot.get('labor_hours', []),
                'coefficients': coeff
            }
        coeff = snapshot.get('coefficients')
        return {'quotation': snapshot, 'modules': [], 'fees': [], 'labor_hours': snapshot.get('labor_hours', []), 'coefficients': coeff}

    v1_data = normalize(json.loads(version1.snapshot_data))
    v2_data = normalize(json.loads(version2.snapshot_data))
    
    # 补充物料详情（旧快照可能只有 material_id）
    from app.models import Material
    material_cache = {}
    
    def enrich_material(mat_data):
        """为物料补充 name/spec/brand/unit_price"""
        if not mat_data:
            return mat_data
        mat_id = mat_data.get('material_id')
        if not mat_id:
            return mat_data
        if mat_id not in material_cache:
            mat = Material.query.get(mat_id)
            if mat:
                material_cache[mat_id] = {
                    'material_name': mat.name,
                    'spec': mat.spec,
                    'brand': mat.brand,
                    'unit_price': float(mat.unit_price) if mat.unit_price else 0,
                    'unit': mat.unit,
                }
            else:
                material_cache[mat_id] = {'material_name': f'物料{mat_id}', 'spec': '-', 'brand': '-', 'unit_price': 0, 'unit': ''}
        return {**mat_data, **material_cache[mat_id]}
    
    def enrich_module(mod):
        if 'materials' in mod:
            mod['materials'] = [enrich_material(m) for m in mod['materials']]
        return mod
    
    v1_data['modules'] = [enrich_module(m) for m in v1_data.get('modules', [])]
    v2_data['modules'] = [enrich_module(m) for m in v2_data.get('modules', [])]

    # 计算汇总（使用报价单系数，与PDF一致）
    from app.routes.exports import calculate_version_totals
    v1_totals = calculate_version_totals(v1_data)
    v2_totals = calculate_version_totals(v2_data)

    return jsonify({
        'version1': v1_data,
        'version2': v2_data,
        'totals1': v1_totals,
        'totals2': v2_totals
    }), 200