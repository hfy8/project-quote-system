"""操作日志模型"""
from datetime import datetime
from db import db


class OperationLog(db.Model):
    """操作日志模型"""
    __tablename__ = 'operation_logs'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    user_id = db.Column(db.BigInteger, nullable=False, index=True)
    username = db.Column(db.String(50), nullable=False, index=True)
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
            'action': self.action,
            'module': self.module,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'detail': self.detail,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }


# 操作类型常量
class Action:
    LOGIN = 'login'
    LOGOUT = 'logout'
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
    EXPORT = 'export'
    IMPORT = 'import'
    SUBMIT = 'submit'
    APPROVE = 'approve'
    REJECT = 'reject'
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
