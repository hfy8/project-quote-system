from datetime import datetime
from db import db


class Department(db.Model):
    """部门模型"""
    __tablename__ = 'departments'

    id = db.Column(db.BigInteger, primary_key=True)  # 对应源系统 dept_id
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(500))
    level = db.Column(db.SmallInteger)  # 部门层级
    header_id = db.Column(db.BigInteger)  # 部门负责人ID
    parent_id = db.Column(db.BigInteger, db.ForeignKey('departments.id'))  # 上级部门ID
    parent_path = db.Column(db.String(500))  # 父路径
    org_id = db.Column(db.BigInteger)  # 组织ID
    dept_type = db.Column(db.String(20))  # 部门类型
    is_active = db.Column(db.Boolean, default=True)
    sync_flag = db.Column(db.Boolean, default=True)  # 同步标记
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系 - employees 关系在 Employee 模型中定义
    parent = db.relationship('Department', remote_side=[id], backref='children')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'level': self.level,
            'header_id': self.header_id,
            'parent_id': self.parent_id,
            'parent_path': self.parent_path,
            'org_id': self.org_id,
            'dept_type': self.dept_type,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
