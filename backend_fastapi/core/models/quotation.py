from datetime import datetime
from db import db


class Quotation(db.Model):
    """报价单模型"""
    __tablename__ = 'quotations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    type = db.Column(db.String(20), nullable=False, index=True)  # single/line
    scheme_no = db.Column(db.String(50), nullable=True, index=True)
    status = db.Column(db.String(20), nullable=False, default='draft', index=True)  # draft/approved
    business_owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    tax_rate = db.Column(db.Float, default=0.13, comment='税率')  # 默认13%增值税
    profit_rate = db.Column(db.Float, default=0.0, comment='对外利润率，如 0.15 表示 15%')  # 对外利润率
    currency = db.Column(db.String(10), default='CNY', comment='币种')  # CNY/USD/EUR
    current_version = db.Column(db.Integer, default=1, comment='当前版本号')
    parent_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=True, index=True, comment='父报价单ID（子报价单引用线体）')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    children = db.relationship('Quotation', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    business_owner = db.relationship('User', foreign_keys=[business_owner_id], backref='owned_quotations')
    creator = db.relationship('User', foreign_keys=[creator_id], backref='created_quotations')
    participants = db.relationship('QuotationParticipant', backref='quotation', cascade='all, delete-orphan')
    modules = db.relationship('Module', backref='quotation', cascade='all, delete-orphan')
    fees = db.relationship('OtherFee', backref='quotation', cascade='all, delete-orphan')
    versions = db.relationship('VersionSnapshot', backref='quotation', cascade='all, delete-orphan')
    coefficients = db.Column(db.JSON, default=dict, comment='费用系数配置：{large, standard, other}')

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
            'profit_rate': self.profit_rate if self.profit_rate is not None else 0.0,
            'currency': self.currency,
            'current_version': self.current_version,
            'parent_id': self.parent_id,
            'child_count': self.children.count() if self.children else 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'coefficients': self.coefficients or {'large': 1.0, 'standard': 1.0, 'other': 1.0},
        }


class QuotationParticipant(db.Model):
    """报价单参与人员模型"""
    __tablename__ = 'quotation_participants'

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    participant_type = db.Column(db.String(20), nullable=False, default='project', comment='参与类型: project/agency/electrical 项目/机构/电气')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='quotation_participations')

    def to_dict(self):
        return {
            'id': self.id,
            'quotation_id': self.quotation_id,
            'user_id': self.user_id,
            'participant_type': self.participant_type,
            'user': self.user.to_dict() if self.user else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }