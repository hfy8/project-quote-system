"""操作日志记录器"""
from flask import request
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from api_app.app import db
from api_app.app.models.operation_log import OperationLog


def get_client_ip():
    """获取客户端IP"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr or '127.0.0.1'


def log_operation(action, module, resource_type=None, resource_id=None, detail=None):
    """
    记录操作日志

    Args:
        action: 操作类型 (login/logout/create/update/delete/export/submit/approve/reject/view)
        module: 模块 (auth/quotation/material/fee/exchange_rate/user/role)
        resource_type: 资源类型
        resource_id: 资源ID
        detail: 详细描述
    """
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        if not user_id:
            return
    except Exception:
        return

    try:
        # 获取用户信息
        from api_app.app.models.user import User
        user = User.query.get(user_id)
        username = user.username if user else str(user_id)
    except Exception:
        username = str(user_id)

    log = OperationLog(
        user_id=user_id or 0,
        username=username,
        action=action,
        module=module,
        resource_type=resource_type,
        resource_id=resource_id,
        detail=detail,
        ip_address=get_client_ip(),
        user_agent=request.headers.get('User-Agent', '')[:200]
    )
    db.session.add(log)
    db.session.commit()


def log_operation_manual(user_id, username, action, module, resource_type=None, resource_id=None, detail=None):
    """手动记录操作日志（不依赖当前请求上下文）"""
    log = OperationLog(
        user_id=user_id or 0,
        username=username,
        action=action,
        module=module,
        resource_type=resource_type,
        resource_id=resource_id,
        detail=detail,
        ip_address='127.0.0.1',
        user_agent='system'
    )
    db.session.add(log)
    db.session.commit()
