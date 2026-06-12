from datetime import datetime
from db import db


class Position(db.Model):
    """职位模型"""
    __tablename__ = 'positions'

    id = db.Column(db.BigInteger, primary_key=True)  # 对应源系统 position_id
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(500))
    position_type = db.Column(db.String(20))  # 职位类型
    position_level = db.Column(db.SmallInteger)  # 职位级别
    is_active = db.Column(db.Boolean, default=True)
    sync_flag = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'position_type': self.position_type,
            'position_level': self.position_level,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
