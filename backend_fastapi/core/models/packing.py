from datetime import datetime
from db import db


class PackingType(db.Model):
    """包装类型（系统配置）"""
    __tablename__ = 'packing_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)           # 纸箱/木箱/托盘
    name_en = db.Column(db.String(100))
    unit_price = db.Column(db.Numeric(12, 2), default=0)      # 单价（元/个）
    description = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'name_en': self.name_en or self.name,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
