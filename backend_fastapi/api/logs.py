"""FastAPI 路由 - 操作日志 (迁移版)"""

from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import desc
from core.models.operation_log import OperationLog
from main import get_db, get_current_user_id

router = APIRouter(prefix="/api/logs")

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


@router.get("")
def get_logs(
    page: int = 1,
    pageSize: int = 20,
    module: Optional[str] = "",
    action: Optional[str] = "",
    keyword: Optional[str] = "",
    user_id: Optional[int] = None,
    db=Depends(get_db),
    current_user=Depends(get_current_user_id),
):
    """获取操作日志列表"""
    query = db.query(OperationLog)

    if module:
        query = query.filter(OperationLog.module == module)
    if action:
        query = query.filter(OperationLog.action == action)
    if keyword:
        query = query.filter(OperationLog.detail.ilike(f'%{keyword}%'))
    if user_id:
        query = query.filter(OperationLog.user_id == user_id)

    query = query.order_by(desc(OperationLog.created_at))

    total = query.count()
    items = query.offset((page - 1) * pageSize).limit(pageSize).all()

    return JSONResponse(content={
        'items': [log.to_dict() for log in items],
        'total': total,
        'page': page,
        'pageSize': pageSize,
    })


@router.get("/modules")
def get_log_modules(db=Depends(get_db), current_user=Depends(get_current_user_id)):
    """获取日志模块列表"""
    modules = db.query(OperationLog.module).distinct().all()
    items = []
    for (m,) in modules:
        items.append({
            'value': m,
            'label': MODULE_TEXT.get(m, m)
        })
    return JSONResponse(content={'items': items})


@router.get("/actions")
def get_log_actions(db=Depends(get_db), current_user=Depends(get_current_user_id)):
    """获取日志操作类型列表"""
    actions = db.query(OperationLog.action).distinct().all()
    items = []
    for (a,) in actions:
        items.append({
            'value': a,
            'label': ACTION_TEXT.get(a, a)
        })
    return JSONResponse(content={'items': items})
