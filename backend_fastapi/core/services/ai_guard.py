"""AI 工具权限校验 + 操作日志

阶段 6：所有写操作的 AI 工具必须经过此模块的权限校验和日志记录。
"""
from typing import Dict, Optional, Tuple

# ============== 工具 → 权限码映射 ==============
# 写操作工具必须在这里登记，没有登记的工具默认只读（无需校验）。
# 复用了现有权限码（ai.* 暂不引入，避免引入新 seed 工作）。
TOOL_PERMISSIONS: Dict[str, str] = {
    "update_quotation_status": "quotation.edit",
    "delete_knowledge": "system.edit",          # 知识库管理 = 系统设置
    "add_knowledge": "system.edit",              # 知识库管理 = 系统设置
    "upsert_knowledge_embedding": "system.edit", # 知识库管理 = 系统设置
    "create_quotation": "quotation.create",
    # 系统日志读取：仅 admin/manager（看 system.edit 权限码）
    "tail_app_logs": "system.edit",
    "grep_app_logs": "system.edit",
    "get_recent_errors": "system.edit",
    "get_slow_queries": "system.edit",
    "get_slow_query_stats": "system.edit",
}

# 工具 → 操作日志 action 映射
TOOL_LOG_ACTIONS: Dict[str, Tuple[str, str]] = {
    # tool_name: (action, module)
    "update_quotation_status": ("update", "quotation"),
    "delete_knowledge": ("delete", "knowledge"),
    "add_knowledge": ("create", "knowledge"),
    "upsert_knowledge_embedding": ("update", "knowledge"),
    "create_quotation": ("create", "quotation"),
}


def get_required_permission(tool_name: str) -> Optional[str]:
    """获取工具需要的权限码。无则返回 None（只读工具）"""
    return TOOL_PERMISSIONS.get(tool_name)


def check_tool_permission(user_id: int, tool_name: str) -> Tuple[bool, str]:
    """
    检查用户是否有权调用指定 AI 工具

    Args:
        user_id: 用户 ID
        tool_name: 工具名

    Returns:
        (allowed, message)
        allowed=True 表示通过
        allowed=False 表示拒绝（message 是拒绝原因）
    """
    perm_code = get_required_permission(tool_name)
    # 只读工具无需校验
    if not perm_code:
        return True, "只读工具，无需权限校验"

    if not user_id:
        return False, "未登录用户不能执行写操作"

    try:
        from core.models.user import User
        from core.models.permission import Role
        from db import db_session_factory

        session = db_session_factory()
        try:
            user = session.query(User).get(int(user_id))
            if not user:
                return False, f"用户 #{user_id} 不存在"

            # 管理员放行
            if user.role == "admin":
                return True, f"管理员放行（tool={tool_name}）"

            # 查找角色权限
            role = session.query(Role).filter(Role.code == user.role).first()
            if not role:
                return False, f"用户角色 '{user.role}' 不存在"

            perm_codes = {p.code for p in role.permissions}
            if perm_code in perm_codes or "*" in perm_codes:
                return True, f"权限 {perm_code} 通过"

            return False, f"缺少权限 {perm_code}"
        finally:
            session.close()
    except Exception as e:
        return False, f"权限校验异常: {str(e)}"


def log_tool_action(user_id: int, tool_name: str, arguments: dict,
                    success: bool, result_preview: str = "") -> bool:
    """
    记录 AI 工具调用日志

    Args:
        user_id: 用户 ID
        tool_name: 工具名
        arguments: 工具参数
        success: 是否成功
        result_preview: 结果预览（前 200 字）

    Returns:
        是否成功记录
    """
    try:
        from utils.logger import log_operation

        action_module = TOOL_LOG_ACTIONS.get(tool_name, ("ai_tool", "ai"))
        action, module = action_module

        # 构造 detail：tool + 参数 + 结果
        args_str = str(arguments)[:200] if arguments else ""
        detail = f"[AI:{tool_name}] args={args_str} success={success}"
        if not success and result_preview:
            detail += f" error={result_preview[:200]}"

        # 资源 ID 提取（从常见参数）
        resource_id = None
        resource_type = None
        if "quotation_id" in arguments:
            resource_type = "quotation"
            resource_id = str(arguments.get("quotation_id"))
        elif "doc_id" in arguments:
            resource_type = "knowledge_doc"
            resource_id = str(arguments.get("doc_id"))

        log_operation(
            user_id=user_id,
            action=action,
            module=module,
            detail=detail,
            resource_type=resource_type,
            resource_id=resource_id,
        )
        return True
    except Exception as e:
        # 日志失败不能阻断业务
        import logging
        logging.getLogger(__name__).warning(f"log_tool_action failed: {e}")
        return False