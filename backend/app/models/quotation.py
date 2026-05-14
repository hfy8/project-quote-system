from datetime import datetime
from app import db


class Quotation(db.Model):
    """报价单模型"""
    __tablename__ = 'quotations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # single/line
    scheme_no = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='draft')  # draft/approved
    business_owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tax_rate = db.Column(db.Float, default=0.13, comment='税率')  # 默认13%增值税
    currency = db.Column(db.String(10), default='CNY', comment='币种')  # CNY/USD/EUR
    current_version = db.Column(db.Integer, default=1, comment='当前版本号')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    business_owner = db.relationship('User', foreign_keys=[business_owner_id], backref='owned_quotations')
    creator = db.relationship('User', foreign_keys=[creator_id], backref='created_quotations')
    participants = db.relationship('QuotationParticipant', backref='quotation', cascade='all, delete-orphan')
    modules = db.relationship('Module', backref='quotation', cascade='all, delete-orphan')
    fees = db.relationship('OtherFee', backref='quotation', cascade='all, delete-orphan')
    versions = db.relationship('VersionSnapshot', backref='quotation', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'scheme_no': self.scheme_no,
            'status': self.status,
            'business_owner_id': self.business_owner_id,
            'business_owner_name': self.business_owner.real_name if self.business_owner else None,
            'creator_id': self.creator_id,
            'creator_name': self.creator.real_name if self.creator else None,
            'tax_rate': self.tax_rate,
            'currency': self.currency,
            'current_version': self.current_version,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class QuotationParticipant(db.Model):
    """报价单参与人员模型"""
    __tablename__ = 'quotation_participants'

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='quotation_participations')

    def to_dict(self):
        return {
            'id': self.id,
            'quotation_id': self.quotation_id,
            'user_id': self.user_id,
            'user': self.user.to_dict() if self.user else None,
        }