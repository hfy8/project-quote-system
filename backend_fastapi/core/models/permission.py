"""权限模型"""
from datetime import datetime
from db import db

# 角色-权限关联表
role_permissions = db.Table(
    'role_permissions',
    db.Column('role_id', db.BigInteger, db.ForeignKey('roles.id'), primary_key=True),
    db.Column('permission_id', db.BigInteger, db.ForeignKey('permissions.id'), primary_key=True)
)


class Role(db.Model):
    """角色模型"""
    __tablename__ = 'roles'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    permissions = db.relationship('Permission', secondary=role_permissions,
                                 backref=db.backref('roles', lazy='dynamic'), lazy='dynamic')

    def to_dict(self, include_permissions=True):
        from core.models import User
        result = {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'user_count': User.query.filter_by(role=self.code).count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
        if include_permissions:
            result['permissions'] = [p.code for p in self.permissions]
        return result


class Permission(db.Model):
    """权限模型"""
    __tablename__ = 'permissions'

    id = db.Column(db.BigInteger, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    group = db.Column(db.String(50))
    description = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'group': self.group,
            'description': self.description,
        }
