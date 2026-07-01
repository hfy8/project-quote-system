from db import db
from datetime import datetime

class LaborHour(db.Model):
    __tablename__ = 'labor_hours'

    # 3 个 labor_type (与前端 choices 一致)
    LABOR_TYPE_DESIGN = 'design'      # 设计
    LABOR_TYPE_DEBUG = 'debug'        # 调试
    LABOR_TYPE_ASSEMBLY = 'assembly'  # 装配
    LABOR_TYPE_CHOICES = ('design', 'debug', 'assembly')
    LABOR_TYPE_LABELS = {
        'design': '设计',
        'debug': '调试',
        'assembly': '装配',
    }

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False, comment='工时名称')
    labor_type = db.Column(db.String(20), default='design', comment='工时类型: design/debug/assembly')
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
            'labor_type': self.labor_type or 'design',
            'labor_type_label': self.LABOR_TYPE_LABELS.get(self.labor_type or 'design', '设计'),
            'hours': self.hours,
            'unit_price': self.unit_price,
            'total': self.total,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
