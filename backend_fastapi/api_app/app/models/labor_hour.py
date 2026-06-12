from api_app.app import db
from datetime import datetime

class LaborHour(db.Model):
    __tablename__ = 'labor_hours'

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False, comment='工时名称')
    hours = db.Column(db.Float, default=0, comment='工时数')
    unit_price = db.Column(db.Float, default=0, comment='单价')
    total = db.Column(db.Float, default=0, comment='合计 = 工时 * 单价')
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'quotation_id': self.quotation_id,
            'name': self.name,
            'hours': self.hours,
            'unit_price': self.unit_price,
            'total': self.total,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
