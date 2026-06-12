from datetime import datetime
from api_app.app import db


class Organization(db.Model):
    """组织模型"""
    __tablename__ = 'organizations'

    id = db.Column(db.BigInteger, primary_key=True)  # 对应源系统 org_id
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True)
    org_type = db.Column(db.String(20))  # 组织类型
    description = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    sync_flag = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'org_type': self.org_type,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
