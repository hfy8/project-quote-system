from datetime import datetime
from api_app.app import db


class PackingEntry(db.Model):
    """包装条目（项目层）"""
    __tablename__ = 'packing_entries'

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=False)
    packing_type_id = db.Column(db.Integer, db.ForeignKey('packing_types.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)               # 使用数量（单元）
    unit_price = db.Column(db.Numeric(10, 2), nullable=True)  # 项目层自定义单价，NULL则用系统配置
    remark = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    packing_type = db.relationship('PackingType', backref='entries')

    def to_dict(self):
        return {
            'id': self.id,
            'quotation_id': self.quotation_id,
            'packing_type_id': self.packing_type_id,
            'packing_type_name': self.packing_type.name if self.packing_type else None,
            'unit_price': float(self.unit_price) if self.unit_price else (float(self.packing_type.unit_price) if self.packing_type and self.packing_type.unit_price else 0),
            'quantity': self.quantity or 0,
            'subtotal': (float(self.unit_price) if self.unit_price else (float(self.packing_type.unit_price) if self.packing_type and self.packing_type.unit_price else 0)) * float(self.quantity or 0),
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class TravelPersonDays(db.Model):
    """差旅人天条目（项目层）"""
    __tablename__ = 'travel_person_days'

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=False)
    travel_category_id = db.Column(db.Integer, db.ForeignKey('travel_categories.id'), nullable=False)
    person_days = db.Column(db.Numeric(10, 2), default=0)    # 出星人天数
    unit_price = db.Column(db.Numeric(10, 2), nullable=True)  # 项目层自定义单价，NULL则用系统配置
    remark = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    travel_category = db.relationship('TravelCategory', backref='person_days_entries')

    def to_dict(self):
        return {
            'id': self.id,
            'quotation_id': self.quotation_id,
            'travel_category_id': self.travel_category_id,
            'travel_category_name': self.travel_category.name if self.travel_category else None,
            'unit_price': float(self.unit_price) if self.unit_price else (float(self.travel_category.day_rates[0].unit_price) if self.travel_category and self.travel_category.day_rates else 0),
            'person_days': float(self.person_days) if self.person_days else 0,
            'subtotal': (float(self.unit_price) if self.unit_price else (float(self.travel_category.day_rates[0].unit_price) if self.travel_category and self.travel_category.day_rates else 0)) * (float(self.person_days) if self.person_days else 0),
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class TravelPersonTrip(db.Model):
    """差旅人次条目（项目层）：每分类×每出行方式一个人次记录"""
    __tablename__ = 'travel_person_trips'

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=False)
    travel_category_id = db.Column(db.Integer, db.ForeignKey('travel_categories.id'), nullable=False)
    travel_mode_id = db.Column(db.Integer, db.ForeignKey('travel_modes.id'), nullable=False)
    person_count = db.Column(db.Integer, default=0)           # 人次
    unit_price = db.Column(db.Numeric(10, 2), nullable=True)  # 项目层自定义交通单价
    visa_fee = db.Column(db.Numeric(10, 2), nullable=True)    # 项目层自定义签证费
    remark = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    travel_category = db.relationship('TravelCategory', backref='person_trip_entries')
    travel_mode = db.relationship('TravelMode', backref='person_trip_entries')

    def to_dict(self):
        return {
            'id': self.id,
            'quotation_id': self.quotation_id,
            'travel_category_id': self.travel_category_id,
            'travel_category_name': self.travel_category.name if self.travel_category else None,
            'travel_mode_id': self.travel_mode_id,
            'travel_mode_name': self.travel_mode.name if self.travel_mode else None,
            'person_count': self.person_count or 0,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'visa_fee': float(self.visa_fee) if self.visa_fee else 0,
            'subtotal': ((float(self.unit_price) if self.unit_price else 0) + (float(self.visa_fee) if self.visa_fee else 0)) * (self.person_count or 0),
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
