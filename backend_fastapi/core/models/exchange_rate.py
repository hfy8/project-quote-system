from datetime import datetime
from db import db


class ExchangeRate(db.Model):
    """汇率配置"""
    __tablename__ = 'exchange_rates'

    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(20), nullable=False, comment='货币代码：CNY/USD/EUR等')
    rate = db.Column(db.Float, nullable=False, default=1.0, comment='汇率（相对于基准货币）')
    is_base = db.Column(db.Boolean, default=False, comment='是否为基准货币')
    description = db.Column(db.String(200), comment='描述')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'currency': self.currency,
            'rate': self.rate,
            'is_base': self.is_base,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
