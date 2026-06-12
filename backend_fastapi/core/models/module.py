from datetime import datetime
from db import db


class Module(db.Model):
    """模块模型"""
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(150), nullable=True, comment='英文名称')
    code = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    participants = db.relationship('ModuleParticipant', backref='module', cascade='all, delete-orphan')
    materials = db.relationship('ModuleMaterial', backref='module', cascade='all, delete-orphan')

    def to_dict(self):
        total = sum(
            (float(m.unit_price_override) if m.is_other and m.unit_price_override else m.quantity * float(m.material.unit_price) if m.material and m.material.unit_price else 0)
            for m in self.materials
        )
        return {
            'id': self.id,
            'quotation_id': self.quotation_id,
            'name': self.name,
            'name_en': self.name_en,
            'code': self.code,
            'description': self.description,
            'total': total,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'participants': [{'id': p.id, 'user_id': p.user_id} for p in self.participants],
            'materials': [m.to_dict() for m in self.materials]
        }


class ModuleParticipant(db.Model):
    """模块参与人员模型"""
    __tablename__ = 'module_participants'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='module_participations')

    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'user_id': self.user_id,
            'user_name': self.user.real_name if self.user else None,
            'username': self.user.username if self.user else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }