from datetime import datetime
from db import db


class FeeRate(db.Model):
    """费用系数配置"""
    __tablename__ = 'fee_rates'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False, comment='物料分类：大件/普通件/其他件')
    rate = db.Column(db.Float, nullable=False, default=1.0, comment='费用系数')
    description = db.Column(db.String(200), comment='描述')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'rate': self.rate,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
