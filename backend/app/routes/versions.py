from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import VersionSnapshot, Quotation
import json

version_bp = Blueprint('versions', __name__)


@version_bp.route('/quotations/<int:quotation_id>/versions', methods=['GET'])
@jwt_required()
def get_versions(quotation_id):
    """获取版本列表"""
    versions = VersionSnapshot.query.filter_by(quotation_id=quotation_id).order_by(VersionSnapshot.version_no.desc()).all()
    return jsonify([v.to_dict() for v in versions]), 200


@version_bp.route('/quotations/<int:quotation_id>/versions', methods=['POST'])
@jwt_required()
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
        'quotation': quotation.to_dict(),
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

    result = version.to_dict()
    result['snapshot_data'] = json.loads(version.snapshot_data)
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

    return jsonify({
        'version1': json.loads(version1.snapshot_data),
        'version2': json.loads(version2.snapshot_data),
    }), 200