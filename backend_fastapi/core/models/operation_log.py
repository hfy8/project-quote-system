"""操作日志模型"""
from datetime import datetime, timezone, timedelta

from db import db

# 项目时区: 全部日志时间都按 +8 (Asia/Shanghai) 输出
PROJECT_TZ = timezone(timedelta(hours=8))
UTC_TZ = timezone.utc


def _format_local(dt):
    """把数据库返回的 naive 时间 (实际是 UTC) 转换为项目本地时区 ISO 8601 字符串

    返回格式: '2026-07-13T10:35:41+08:00' (带 T 分隔符 + +08:00 偏移)
    - 前端 split('T') 能正确拿到日期/时间两部分
    - 带 +08:00 偏移, 浏览器/JS 解析后永远是北京时间, 不受客户端时区影响
    """
    if not dt:
        return None
    # 数据库存的是 naive datetime 但语义是 UTC (created_at default=datetime.utcnow)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC_TZ)
    local = dt.astimezone(PROJECT_TZ)
    # strftime %z 输出 +0800, 改为 +08:00 符合 ISO 8601
    s = local.strftime('%Y-%m-%dT%H:%M:%S%z')
    return s[:-2] + ':' + s[-2:]


class OperationLog(db.Model):
    """操作日志模型"""
    __tablename__ = 'operation_logs'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, nullable=False, index=True)
    username = db.Column(db.String(50), nullable=False, index=True)
    employee_no = db.Column(db.String(50), index=True)  # 工号（写日志时快照）
    cn_name = db.Column(db.String(100))  # 中文姓名（写日志时快照）
    action = db.Column(db.String(20), nullable=False, index=True)  # login/logout/create/update/delete/export/submit/approve/reject
    module = db.Column(db.String(20), nullable=False, index=True)  # auth/quotation/material/fee/exchange_rate/user/role/system
    resource_type = db.Column(db.String(30))  # quotation/material/user/role等
    resource_id = db.Column(db.String(50))  # 资源ID或方案号
    detail = db.Column(db.String(500))  # 详细描述
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'employee_no': self.employee_no,
            'cn_name': self.cn_name,
            'action': self.action,
            'module': self.module,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'detail': self.detail,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'created_at': _format_local(self.created_at)
        }


# 操作类型常量
class Action:
    LOGIN = 'login'
    LOGOUT = 'logout'
    CREATE = 'create'
    UPDATE = 'update'
    EDIT = 'update'  # 别名: edit 等同 update (兼容旧调用)
    DELETE = 'delete'
    EXPORT = 'export'
    IMPORT = 'import'
    SUBMIT = 'submit'
    APPROVE = 'approve'
    REJECT = 'reject'
    CANCEL = 'cancel'
    VIEW = 'view'
    RESET_PASSWORD = 'reset_password'


# 模块常量
class Module:
    AUTH = 'auth'
    QUOTATION = 'quotation'
    MATERIAL = 'material'
    FEE = 'fee'
    FEE_TYPE = 'fee_type'
    EXCHANGE_RATE = 'exchange_rate'
    USER = 'user'
    ROLE = 'role'
    SYSTEM = 'system'
