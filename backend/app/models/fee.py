from datetime import datetime
from app import db


class OtherFee(db.Model):
    """其他费用模型"""
    __tablename__ = 'other_fees'

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=True)  # 可空
    fee_type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(20), nullable=False)  # 厂内/厂外
    amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    module = db.relationship('Module', backref='fees')

    def to_dict(self):
        return {
            'id': self.id,
            'quotation_id': self.quotation_id,
            'module_id': self.module_id,
            'fee_type': self.fee_type,
            'location': self.location,
            'amount': float(self.amount) if self.amount else 0,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class FeeType(db.Model):
    """费用类型配置模型"""
    __tablename__ = 'fee_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    name_en = db.Column(db.String(100), nullable=True, comment='英文名称')
    location = db.Column(db.String(20), nullable=False)  # 厂内/厂外
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'name_en': self.name_en,
            'location': self.location,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }