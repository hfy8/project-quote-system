from flask import Blueprint, jsonify, request
from app.utils.permissions import check_permission, has_permission
from flask_jwt_extended import jwt_required
from app import db
from app.models import ParticipantTypePermission

ptp_bp = Blueprint('participant_type_permissions', __name__)

# 默认 Tab 配置
DEFAULT_TABS = [
    # project 类型（全部 Tab）
    {'participant_type': 'project', 'tab_name': 'modules', 'tab_label': '模块管理', 'type_name': '项目', 'description': '添加、编辑、删除模块', 'sort_order': 1},
    {'participant_type': 'project', 'tab_name': 'participants', 'tab_label': '参与人员', 'type_name': '项目', 'description': '管理报价单参与人员', 'sort_order': 2},
    {'participant_type': 'project', 'tab_name': 'coefficients', 'tab_label': '费用系数', 'type_name': '项目', 'description': '调整大件/普通件/其他件系数', 'sort_order': 3},
    {'participant_type': 'project', 'tab_name': 'materials', 'tab_label': '物料清单', 'type_name': '项目', 'description': '物料选择与报价', 'sort_order': 4},
    {'participant_type': 'project', 'tab_name': 'fees', 'tab_label': '费用', 'type_name': '项目', 'description': '附加费用配置', 'sort_order': 5},
    {'participant_type': 'project', 'tab_name': 'labor', 'tab_label': '人力工时', 'type_name': '项目', 'description': '人力工时统计', 'sort_order': 6},
    {'participant_type': 'project', 'tab_name': 'summary', 'tab_label': '汇总', 'type_name': '项目', 'description': '查看费用汇总', 'sort_order': 7},
    {'participant_type': 'project', 'tab_name': 'export', 'tab_label': '导出', 'type_name': '项目', 'description': '导出 Excel/PDF', 'sort_order': 8},
    # agency 类型
    {'participant_type': 'agency', 'tab_name': 'materials', 'tab_label': '物料清单', 'type_name': '机构', 'description': '物料选择与报价', 'sort_order': 1},
    {'participant_type': 'agency', 'tab_name': 'fees', 'tab_label': '费用', 'type_name': '机构', 'description': '附加费用配置', 'sort_order': 2},
    {'participant_type': 'agency', 'tab_name': 'labor', 'tab_label': '人力工时', 'type_name': '机构', 'description': '人力工时统计', 'sort_order': 3},
    {'participant_type': 'agency', 'tab_name': 'summary', 'tab_label': '汇总', 'type_name': '机构', 'description': '查看费用汇总', 'sort_order': 4},
    {'participant_type': 'agency', 'tab_name': 'export', 'tab_label': '导出', 'type_name': '机构', 'description': '导出 Excel/PDF', 'sort_order': 5},
    # electrical 类型
    {'participant_type': 'electrical', 'tab_name': 'materials', 'tab_label': '物料清单', 'type_name': '电气', 'description': '物料选择与报价', 'sort_order': 1},
    {'participant_type': 'electrical', 'tab_name': 'fees', 'tab_label': '费用', 'type_name': '电气', 'description': '附加费用配置', 'sort_order': 2},
    {'participant_type': 'electrical', 'tab_name': 'labor', 'tab_label': '人力工时', 'type_name': '电气', 'description': '人力工时统计', 'sort_order': 3},
    {'participant_type': 'electrical', 'tab_name': 'summary', 'tab_label': '汇总', 'type_name': '电气', 'description': '查看费用汇总', 'sort_order': 4},
    {'participant_type': 'electrical', 'tab_name': 'export', 'tab_label': '导出', 'type_name': '电气', 'description': '导出 Excel/PDF', 'sort_order': 5},
]


@ptp_bp.route('', methods=['POST'])
@jwt_required()
@check_permission('participant_type_permission.edit')
def create():
    """添加一条 Tab 权限记录"""
    data = request.get_json()
    ptype = data.get('participant_type')
    tab_name = data.get('tab_name')
    if not ptype or not tab_name:
        return jsonify({'error': 'participant_type 和 tab_name 不能为空'}), 400
    p = ParticipantTypePermission(
        participant_type=ptype,
        tab_name=tab_name,
        tab_label=data.get('tab_label', tab_name),
        description=data.get('description', ''),
        sort_order=data.get('sort_order', 0),
        is_disabled=data.get('is_disabled', False)
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201


@ptp_bp.route('', methods=['GET'])
@jwt_required()
def get_all():
    """获取所有类型权限配置"""
    permissions = ParticipantTypePermission.query.order_by(
        ParticipantTypePermission.participant_type,
        ParticipantTypePermission.sort_order
    ).all()
    return jsonify([p.to_dict() for p in permissions])


@ptp_bp.route('/by-type/<ptype>', methods=['GET'])
@jwt_required()
def get_by_type(ptype):
    """按类型获取权限（含禁用的，供管理页面使用）"""
    permissions = ParticipantTypePermission.query.filter_by(
        participant_type=ptype
    ).order_by(ParticipantTypePermission.sort_order).all()
    return jsonify([p.to_dict() for p in permissions])


@ptp_bp.route('/tabs/<ptype>', methods=['GET'])
@jwt_required()
def get_tabs_by_type(ptype):
    """获取某类型可用的 tab 列表（仅未禁用的）"""
    permissions = ParticipantTypePermission.query.filter_by(
        participant_type=ptype,
        is_disabled=False
    ).order_by(ParticipantTypePermission.sort_order).all()
    return jsonify([p.tab_name for p in permissions])


@ptp_bp.route('/initialize', methods=['POST'])
@jwt_required()
def initialize():
    """初始化默认权限配置（幂等）"""
    created = 0
    for tab in DEFAULT_TABS:
        existing = ParticipantTypePermission.query.filter_by(
            participant_type=tab['participant_type'],
            tab_name=tab['tab_name']
        ).first()
        if not existing:
            p = ParticipantTypePermission(**tab)
            db.session.add(p)
            created += 1
    db.session.commit()
    return jsonify({'created': created, 'message': f'初始化完成，新增 {created} 条'})


@ptp_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    """更新权限配置"""
    p = ParticipantTypePermission.query.get(id)
    if not p:
        return jsonify({'error': '记录不存在'}), 404
    data = request.get_json()
    if 'description' in data:
        p.description = data['description']
    if 'sort_order' in data:
        p.sort_order = data['sort_order']
    if 'is_disabled' in data:
        p.is_disabled = data['is_disabled']
    if 'tab_label' in data:
        p.tab_label = data['tab_label']
    if 'type_name' in data:
        p.type_name = data['type_name']
    db.session.commit()
    return jsonify(p.to_dict())


@ptp_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    """删除单条权限配置"""
    p = ParticipantTypePermission.query.get(id)
    if not p:
        return jsonify({'error': '记录不存在'}), 404
    db.session.delete(p)
    db.session.commit()
    return jsonify({'message': '删除成功'})


@ptp_bp.route('/types/<ptype>', methods=['DELETE'])
@jwt_required()
@check_permission('participant_type_permission.edit')
def delete_type(ptype):
    """删除某类型的所有权限配置"""
    ParticipantTypePermission.query.filter_by(participant_type=ptype).delete()
    db.session.commit()
    return jsonify({'message': '删除成功'})


@ptp_bp.route('/types', methods=['POST'])
@jwt_required()
@check_permission('participant_type_permission.edit')
def create_type():
    """创建新参与类型"""
    data = request.get_json()
    ptype = data.get('participant_type')
    name = data.get('type_name', '')  # 前端传入 type_name
    if not ptype:
        return jsonify({'error': 'participant_type 不能为空'}), 400
    # 检查是否已存在该类型的记录
    existing = ParticipantTypePermission.query.filter_by(participant_type=ptype).first()
    if existing:
        return jsonify({'error': '该类型已存在'}), 400
    # 创建占位记录（type_name=分类中文名，tab_name='' 表示这是类型标记，非真实 Tab）
    p = ParticipantTypePermission(
        participant_type=ptype,
        tab_name='__type__',
        tab_label=name or ptype,
        type_name=name or ptype,
        description='类型标记',
        sort_order=0,
        is_disabled=False
    )
    db.session.add(p)
    db.session.commit()
    return jsonify({'message': '创建成功', 'participant_type': ptype})


@ptp_bp.route('/batch', methods=['PUT'])
@jwt_required()
def batch_update():
    """批量更新某类型的权限配置"""
    data = request.get_json()
    ptype = data.get('participant_type')
    tabs = data.get('tabs', [])  # [{tab_name, description, sort_order}, ...]

    for tab in tabs:
        p = ParticipantTypePermission.query.filter_by(
            participant_type=ptype,
            tab_name=tab['tab_name']
        ).first()
        if p:
            p.description = tab.get('description', p.description)
            p.sort_order = tab.get('sort_order', p.sort_order)
    db.session.commit()
    return jsonify({'message': '更新成功'})
