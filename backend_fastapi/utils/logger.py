"""操作日志记录器

v17: 不依赖 Flask - 使用 FastAPI Request context
通过 set_request_context(req) 在中间件中注入当前请求

v1.4.57: 改用 contextvars 替代 threading.local
  - threading.local 在 FastAPI sync endpoint + anyio threadpool 模式下失效
    (middleware async 注入 + endpoint sync 读 不在同一 thread → 读到空 → fallback '127.0.0.1')
  - contextvars 由 asyncio task 继承，跨 sync/async 边界稳定保留
"""
from contextvars import ContextVar
from db import db
from core.models.operation_log import OperationLog


# contextvars 替代 threading.local：FastAPI 中间件 async 注入，sync endpoint 也能读到
_request_ctx: ContextVar = ContextVar('request_context', default=None)


def set_request_context(req):
    """FastAPI 中间件调用：注入当前请求"""
    _request_ctx.set(req)


def _get_request():
    """获取当前请求（如有）"""
    return _request_ctx.get()


def get_client_ip():
    """获取客户端IP

    优先级:
      1. X-Forwarded-For 第一个 (最原始客户端 IP)
      2. X-Real-IP
      3. req.client.host (uvicorn --proxy-headers 模式下 = X-Forwarded-For 的最后值)
      4. fallback '127.0.0.1'
    """
    req = _get_request()
    if not req:
        return '127.0.0.1'
    # FastAPI Request.headers + .client.host
    xff = req.headers.get('X-Forwarded-For')
    if xff:
        # X-Forwarded-For 可能包含多个 IP (客户端, proxy1, proxy2...)
        # 第一个是最原始的客户端
        return xff.split(',')[0].strip()
    x_real_ip = req.headers.get('X-Real-IP')
    if x_real_ip:
        return x_real_ip.strip()
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
        # 获取用户信息（含工号和中文姓名，快照到日志里）
        from core.models.user import User
        user = User.query.get(user_id)
        username = user.username if user else str(user_id)
        employee_no = user.employee.employee_no if (user and user.employee) else None
        cn_name = user.employee.cn_name if (user and user.employee) else None
    except Exception:
        username = str(user_id)
        employee_no = None
        cn_name = None

    req = _get_request()
    ip = get_client_ip() if req else '127.0.0.1'
    ua = req.headers.get('User-Agent', '')[:200] if req else 'system'

    log = OperationLog(
        user_id=user_id or 0,
        username=username,
        employee_no=employee_no,
        cn_name=cn_name,
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
    # 尝试从 user 拿工号/姓名快照（可选，user_id 无效时允许为空）
    employee_no = None
    cn_name = None
    if user_id:
        try:
            from core.models.user import User
            user = User.query.get(user_id)
            if user and user.employee:
                employee_no = user.employee.employee_no
                cn_name = user.employee.cn_name
        except Exception:
            pass

    log = OperationLog(
        user_id=user_id or 0,
        username=username,
        employee_no=employee_no,
        cn_name=cn_name,
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
