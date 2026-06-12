"""操作日志工具（FastAPI 版）- 兼容 Flask 的 log_operation 接口

直接从 backend/app/utils/logger.py 简化，去掉 Flask-JWT 依赖，
改用传入的 db session 和 user_id。
"""

from api_app.app.models.operation_log import OperationLog, Action, Module
from datetime import datetime


def log_operation(
    action,
    module,
    resource_type=None,
    resource_id=None,
    detail=None,
    db=None,
    user_id=None,
    username=None,
):
    """记录操作日志

    兼容版：接受可选的 db session（FastAPI 的 get_db()）替代 Flask-SQLAlchemy session。
    如果 db 或 user_id 为 None，则不记录（静默跳过）。
    """
    if not db or not user_id:
        return

    log = OperationLog(
        user_id=int(user_id),
        username=username or str(user_id),
        action=action.value if hasattr(action, 'value') else action,
        module=module.value if hasattr(module, 'value') else module,
        resource_type=resource_type,
        resource_id=resource_id,
        detail=detail,
        created_at=datetime.utcnow(),
    )
    db.add(log)
    db.flush()


def log_operation_manual(
    user_id, username, action, module,
    resource_type=None, resource_id=None, detail=None,
    db=None,
):
    """手动记录操作日志（不依赖请求上下文）"""
    if not db:
        return

    log = OperationLog(
        user_id=int(user_id),
        username=username or str(user_id),
        action=action.value if hasattr(action, 'value') else action,
        module=module.value if hasattr(module, 'value') else module,
        resource_type=resource_type,
        resource_id=resource_id,
        detail=detail,
        created_at=datetime.utcnow(),
    )
    db.add(log)
    db.flush()
