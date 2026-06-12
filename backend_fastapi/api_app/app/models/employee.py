from datetime import datetime
from api_app.app import db


class Employee(db.Model):
    """员工模型 - 存储从HR系统同步的详细员工信息"""
    __tablename__ = 'employees'

    id = db.Column(db.BigInteger, primary_key=True)  # 对应源系统 employee_id
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))  # 关联本地用户表
    employee_no = db.Column(db.String(50), unique=True)  # 员工工号
    cn_name = db.Column(db.String(100), nullable=False)  # 中文姓名
    en_name = db.Column(db.String(100))  # 英文姓名
    nick_name = db.Column(db.String(100))  # 昵称
    gender = db.Column(db.SmallInteger)  # 性别: 0-女, 1-男
    email = db.Column(db.String(100))  # 邮箱
    mobile = db.Column(db.String(20))  # 手机号
    avatar = db.Column(db.String(500))  # 头像URL
    dept_id = db.Column(db.BigInteger, db.ForeignKey('departments.id'))  # 部门ID
    org_id = db.Column(db.BigInteger, db.ForeignKey('organizations.id'))  # 组织ID
    position_id = db.Column(db.BigInteger, db.ForeignKey('positions.id'))  # 职位ID
    is_active = db.Column(db.Boolean, default=True)
    sync_flag = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    department = db.relationship('Department', foreign_keys=[dept_id])
    organization = db.relationship('Organization', foreign_keys=[org_id])
    position = db.relationship('Position', foreign_keys=[position_id])

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'employee_no': self.employee_no,
            'cn_name': self.cn_name,
            'en_name': self.en_name,
            'nick_name': self.nick_name,
            'gender': self.gender,
            'email': self.email,
            'mobile': self.mobile,
            'avatar': self.avatar,
            'dept_id': self.dept_id,
            'org_id': self.org_id,
            'position_id': self.position_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
