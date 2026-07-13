"""操作日志助手函数 - 简化 endpoint 中的 log_operation 调用

用法:
    from utils.log_helpers import record_crud, record_archive_op, record_diff_update
    record_crud(user_id, 'quotation', 'create', f'创建报价单 {scheme_no}', resource_id=str(q.id))
"""
from typing import Any, Iterable, Optional, Sequence

from utils.logger import log_operation


# ============== 基础 CRUD 封装 ==============

def record_crud(
    user_id: Any,
    module: str,
    action: str,  # 'create' / 'update' / 'delete' / 'import'
    detail: str,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
):
    """记录 CRUD 操作 (create/update/delete/import).

    Args:
        user_id: 当前用户 ID (从 Depends(get_current_user_id))
        module: 模块名 (quotation/material/fee/user/role/module 等)
        action: 动作 (create/update/delete/import)
        detail: 描述, 如 "创建报价单 C2568"
        resource_type: 资源类型, 如 quotation/user/role
        resource_id: 资源 ID 或编号
    """
    log_operation(
        user_id=user_id,
        action=action,
        module=module,
        detail=detail,
        resource_type=resource_type,
        resource_id=resource_id,
    )


def record_status_change(
    user_id: Any,
    module: str,
    resource_label: str,
    old_status: Any,
    new_status: Any,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
):
    """记录状态变更, 格式 "{resource_label} 状态 {old}→{new}".

    Args:
        resource_label: 资源名 (如 报价单 C2568)
        old_status: 原状态
        new_status: 新状态
    """
    log_operation(
        user_id=user_id,
        action='update',
        module=module,
        detail=f'{resource_label} 状态 {old_status}→{new_status}',
        resource_type=resource_type,
        resource_id=resource_id,
    )


def record_diff_update(
    user_id: Any,
    module: str,
    resource_label: str,
    changed_fields: Sequence[str],
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    detail_suffix: str = '',
):
    """记录字段变更 (PATCH/PUT), 格式 "更新 {label} (字段: {f1, f2}){suffix}".

    Args:
        resource_label: 资源名
        changed_fields: 发生变化的字段名列表, 空列表表示仅记录"更新"
        detail_suffix: 附加描述, 如 ": {reason}"
    """
    if changed_fields:
        fields_text = ', '.join(changed_fields)
        detail = f'更新 {resource_label} (字段: {fields_text}){detail_suffix}'
    else:
        detail = f'更新 {resource_label}{detail_suffix}'
    log_operation(
        user_id=user_id,
        action='update',
        module=module,
        detail=detail,
        resource_type=resource_type,
        resource_id=resource_id,
    )


def record_archive_op(
    user_id: Any,
    action: str,  # 'submit' / 'approve' / 'reject' / 'cancel'
    scheme_no: str,
    approver_or_user: Optional[str] = None,
    reason: Optional[str] = None,
    resource_id: Optional[str] = None,
):
    """记录归档/审批相关操作.

    Args:
        action: submit/approve/reject/cancel
        scheme_no: 报价单方案号
        approver_or_user: 审批人/操作人 (reject 时必填, 其他可选)
        reason: 驳回原因 (仅 reject)
        resource_id: 报价单 ID
    """
    templates = {
        'submit': lambda: f'提交归档 {scheme_no}',
        'approve': lambda: f'{approver_or_user or "审批人"} 审批通过 {scheme_no}',
        'reject': lambda: f'{approver_or_user or "审批人"} 驳回 {scheme_no}: 原因={reason or "(无)"}',
        'cancel': lambda: f'{approver_or_user or approver_or_user or "用户"} 取消 {scheme_no} 审批申请',
    }
    detail = templates.get(action, lambda: f'{action} {scheme_no}')()
    log_operation(
        user_id=user_id,
        action=action,
        module='quotation',
        detail=detail,
        resource_type='quotation',
        resource_id=str(resource_id) if resource_id else None,
    )


def record_export(
    user_id: Any,
    fmt: str,  # 'Word' / 'Excel' / 'PDF'
    scheme_no: str,
    version_no: Optional[int] = None,
    resource_id: Optional[str] = None,
):
    """记录导出操作.

    Args:
        fmt: 导出格式
        scheme_no: 报价单方案号
        version_no: 版本号 (可选)
    """
    if version_no is not None:
        detail = f'导出 {fmt} ({scheme_no} v{version_no})'
    else:
        detail = f'导出 {fmt} ({scheme_no})'
    log_operation(
        user_id=user_id,
        action='export',
        module='quotation',
        detail=detail,
        resource_type='quotation',
        resource_id=str(resource_id) if resource_id else None,
    )


def record_approval(user_id: Any, action: str, detail: str, resource_type: Optional[str] = None, resource_id: Optional[str] = None):
    """通用审批/驳回 (非报价单场景).

    Args:
        action: 'approve' / 'reject' / 'submit'
    """
    log_operation(
        user_id=user_id,
        action=action,
        module='system',
        detail=detail,
        resource_type=resource_type,
        resource_id=str(resource_id) if resource_id else None,
    )


def record_login(user_id: int, username: str, success: bool = True, ip: Optional[str] = None):
    """登录日志 (手动模式, 因为 login 时不一定有 user_id).

    Args:
        username: 用户名
        success: 是否成功
    """
    from utils.logger import log_operation_manual
    log_operation_manual(
        user_id=user_id or 0,
        username=username,
        action='login',
        module='auth',
        detail=f'用户 "{username}" {"登录成功" if success else "登录失败"}',
        resource_type='user',
        resource_id=str(user_id) if user_id else None,
    )


def record_logout(user_id: Any, username: str):
    """登出日志 (手动模式)."""
    from utils.logger import log_operation_manual
    log_operation_manual(
        user_id=user_id or 0,
        username=username,
        action='logout',
        module='auth',
        detail=f'用户 "{username}" 登出',
        resource_type='user',
        resource_id=str(user_id) if user_id else None,
    )


def record_password_change(user_id: Any, username: str, is_self: bool = True, target_username: Optional[str] = None):
    """密码修改日志.

    Args:
        is_self: True=自己改, False=管理员改他人
        target_username: 被重置的用户名 (is_self=False 时使用)
    """
    if is_self:
        detail = f'用户 "{username}" 修改了自己的密码'
    else:
        detail = f'管理员 "{username}" 重置了用户 "{target_username}" 的密码'
    log_operation(
        user_id=user_id,
        action='reset_password',
        module='auth',
        detail=detail,
        resource_type='user',
        resource_id=str(user_id),
    )


def record_ai_ask(user_id: Any, question_len: int, conversation_id: Optional[int] = None):
    """AI 提问日志."""
    log_operation(
        user_id=user_id,
        action='view',
        module='ai',
        detail=f'AI 提问 ({question_len}字符)',
        resource_type='ai_conversation',
        resource_id=str(conversation_id) if conversation_id else None,
    )


def record_sync(user_id: Any, sync_type: str, target: Optional[str] = None):
    """同步触发日志.

    Args:
        sync_type: '汇率' / '物料价格' / '数据'
        target: 同步对象描述
    """
    detail = f'触发{sync_type}同步'
    if target:
        detail += f' ({target})'
    log_operation(
        user_id=user_id,
        action='update',
        module='system',
        detail=detail,
        resource_type='sync',
    )