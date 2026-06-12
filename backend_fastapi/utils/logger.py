"""操作日志记录器

v17: 不依赖 Flask - 使用 FastAPI Request context
通过 set_request_context(req) 在中间件中注入当前请求
"""
from functools import wraps
import threading
from db import db
from core.models.operation_log import OperationLog


# 线程本地 request 存储（中间件设置）
_local = threading.local()


def set_request_context(req):
    """FastAPI 中间件调用：注入当前请求"""
    _local.request = req


def _get_request():
    """获取当前请求（如有）"""
    return getattr(_local, "request", None)


def get_client_ip():
    """获取客户端IP"""
    req = _get_request()
    if not req:
        return '127.0.0.1'
    # FastAPI Request.headers + .client.host
    xff = req.headers.get('X-Forwarded-For')
    if xff:
        return xff.split(',')[0].strip()
    if req.client:
        return req.client.host
    return '127.0.0.1'


def log_operation(user_id, action, module, detail=None,
                  resource_type=None, resource_id=None):
    """
    记录操作日志

    Args:
        user_id: 用户ID
        action: 操作类型 (login/logout/create/update/delete/export/submit/approve/reject/view)
        module: 模块 (auth/quotation/material/fee/exchange_rate/user/role)
        detail: 详细描述
        resource_type: 资源类型（可选）
        resource_id: 资源ID（可选）
    """
    try:
        # 获取用户信息
        from core.models.user import User
        user = User.query.get(user_id)
        username = user.username if user else str(user_id)
    except Exception:
        username = str(user_id)

    req = _get_request()
    ip = get_client_ip() if req else '127.0.0.1'
    ua = req.headers.get('User-Agent', '')[:200] if req else 'system'

    log = OperationLog(
        user_id=user_id or 0,
        username=username,
        action=action,
        module=module,
        resource_type=resource_type,
        resource_id=resource_id,
        detail=detail,
        ip_address=ip,
        user_agent=ua
    )
    try:
        db.session.add(log)
        db.session.commit()
    except Exception:
        db.session.rollback()


def log_operation_manual(user_id, username, action, module,
                         resource_type=None, resource_id=None, detail=None):
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
    try:
        db.session.add(log)
        db.session.commit()
    except Exception:
        db.session.rollback()
