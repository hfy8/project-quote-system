"""操作日志管理路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import desc
from app import db
from app.models.operation_log import OperationLog
from app.utils.permissions import check_permission, has_permission


logs_bp = Blueprint('logs', __name__)

# 操作类型映射
ACTION_TEXT = {
    'login': '登录',
    'logout': '登出',
    'create': '创建',
    'update': '更新',
    'delete': '删除',
    'export': '导出',
    'import': '导入',
    'submit': '提交',
    'approve': '批准',
    'reject': '拒绝',
    'view': '查看',
    'reset_password': '重置密码'
}

# 模块映射
MODULE_TEXT = {
    'auth': '系统认证',
    'quotation': '报价单',
    'material': '原材料',
    'fee': '费用',
    'fee_type': '费用类型',
    'exchange_rate': '汇率',
    'user': '用户',
    'role': '角色',
    'system': '系统'
}


@logs_bp.route('', methods=['GET'])
@jwt_required()
def get_logs():
    """获取操作日志列表"""
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 20, type=int)
    module = request.args.get('module', '')
    action = request.args.get('action', '')
    keyword = request.args.get('keyword', '')
    user_id = request.args.get('user_id', '', type=int)

    # 构建查询
    query = OperationLog.query

    if module:
        query = query.filter(OperationLog.module == module)
    if action:
        query = query.filter(OperationLog.action == action)
    if keyword:
        query = query.filter(OperationLog.detail.ilike(f'%{keyword}%'))
    if user_id:
        query = query.filter(OperationLog.user_id == user_id)

    # 按时间倒序
    query = query.order_by(desc(OperationLog.created_at))

    # 分页
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return jsonify({
        'items': [log.to_dict() for log in items],
        'total': total,
        'page': page,
        'pageSize': page_size
    })


@logs_bp.route('/modules', methods=['GET'])
@jwt_required()
def get_log_modules():
    """获取日志模块列表"""
    modules = db.session.query(OperationLog.module).distinct().all()
    items = []
    for (m,) in modules:
        items.append({
            'value': m,
            'label': MODULE_TEXT.get(m, m)
        })
    return jsonify({'items': items})


@logs_bp.route('/actions', methods=['GET'])
@jwt_required()
def get_log_actions():
    """获取日志操作类型列表"""
    actions = db.session.query(OperationLog.action).distinct().all()
    items = []
    for (a,) in actions:
        items.append({
            'value': a,
            'label': ACTION_TEXT.get(a, a)
        })
    return jsonify({'items': items})
