"""核心业务包 - 配置、模型、服务、任务

设计：
- 启动时由 main.py 导入此包（`import core`）
- 导入 core.models 触发所有 SQLAlchemy models 注册到 ModuleBase.metadata
- 不需要 Flask app context
"""
# 触发所有 models 注册到 SQLAlchemy metadata
from core.models import (  # noqa: F401
    user, quotation, material, module, fee, fee_rate,
    labor_hour, travel, travel_entry, packing, version,
    message, change_request, operation_log, exchange_rate,
    permission, organization, department, position, employee,
    participant_type_permission, knowledge, ai_conversation,
)
