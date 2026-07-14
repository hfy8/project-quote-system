from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from core.models.permission import Role  # D3: 用于查 DB role_permissions


# 角色权限映射 - 与 roles.py 保持一致
ROLE_PERMISSIONS = {
    'admin': ['*'],
    'business': ['quotation.*', 'fee.*', 'exchange_rate.*', 'fee_rate.*', 'module.*', 'version.*', 'material.view', 'dashboard.view', 'module_assignment.view'],
    'purchaser': ['material.*', 'fee.*', 'dashboard.view', 'module_assignment.view'],
    'viewer': ['dashboard.view', 'module_assignment.view']
}


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'

    id = db.Column(db.BigInteger, primary_key=True)  # 对应源系统 user_id
    username = db.Column(db.String(50), unique=True, nullable=False)  # 登录账号
    password_hash = db.Column(db.String(255), nullable=False)
    real_name = db.Column(db.String(50), nullable=False)  # 真实姓名
    role = db.Column(db.String(20), nullable=False, default='business')  # admin/business/purchaser/viewer
    employee_id = db.Column(db.BigInteger, db.ForeignKey('employees.id'))  # 关联员工ID
    dept_id = db.Column(db.BigInteger, db.ForeignKey('departments.id'))  # 部门ID
    position_id = db.Column(db.BigInteger, db.ForeignKey('positions.id'))  # 职位ID
    is_active = db.Column(db.Boolean, default=True)
    sync_flag = db.Column(db.Boolean, default=True)  # 同步标记
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    employee = db.relationship('Employee', foreign_keys=[employee_id], backref='user')
    department = db.relationship('Department', backref='users')
    position = db.relationship('Position', backref='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_permissions(self):
        """获取用户权限 (D3: 统一从 DB role_permissions 读, 不再走硬编码 ROLE_PERMISSIONS)"""
        if self.role == 'admin':
            return ['*']
        # D3: 优先查 DB (User.role string → Role.code → Role.permissions)
        role = db.session.query(Role).filter_by(code=self.role).first()
        if role and role.permissions is not None:
            return [p.code for p in role.permissions]
        # 兜底: ROLE_PERMISSIONS (向后兼容, 比如新 role 还没 seed)
        return ROLE_PERMISSIONS.get(self.role, ['dashboard.view', 'module_assignment.view'])

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'real_name': self.real_name,
            'role': self.role,
            'permissions': self.get_permissions(),
            'employee_id': self.employee_id,
            'employee_no': self.employee.employee_no if self.employee else None,
            'cn_name': self.employee.cn_name if self.employee else None,
            'dept_id': self.dept_id,
            'dept_name': self.department.name if self.department else None,
            'position_id': self.position_id,
            'position_name': self.position.name if self.position else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
