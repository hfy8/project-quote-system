from datetime import datetime
from db import db


class TravelCategory(db.Model):
    """差旅分类（系统配置）"""
    __tablename__ = 'travel_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)           # 国内出差/东南亚出差/欧洲出差/美国出差
    code = db.Column(db.String(20), unique=True, nullable=False)  # domestic/southeast_asia/europe/usa
    description = db.Column(db.String(200))
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'sort_order': self.sort_order or 0,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class TravelDayRate(db.Model):
    """差旅人天单价配置（系统配置）"""
    __tablename__ = 'travel_day_rates'

    id = db.Column(db.Integer, primary_key=True)
    travel_category_id = db.Column(db.Integer, db.ForeignKey('travel_categories.id'), nullable=False)
    unit_price = db.Column(db.Numeric(12, 2), default=0)      # 元/人天
    currency = db.Column(db.String(10), default='CNY')
    description = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    travel_category = db.relationship('TravelCategory', backref='day_rates')

    def to_dict(self):
        return {
            'id': self.id,
            'travel_category_id': self.travel_category_id,
            'travel_category_name': self.travel_category.name if self.travel_category else None,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'currency': self.currency or 'CNY',
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class TravelMode(db.Model):
    """出行方式（系统配置）"""
    __tablename__ = 'travel_modes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)           # 飞机/高铁/开车
    name_en = db.Column(db.String(100))
    code = db.Column(db.String(20), unique=True, nullable=False)  # plane/train/car
    description = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'name_en': self.name_en or self.name,
            'code': self.code,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class TravelPersonTripFee(db.Model):
    """差旅人次单价配置（系统配置）：每分类×每出行方式一个单价 + 签证费（非国内）"""
    __tablename__ = 'travel_person_trip_fees'

    id = db.Column(db.Integer, primary_key=True)
    travel_category_id = db.Column(db.Integer, db.ForeignKey('travel_categories.id'), nullable=False)
    travel_mode_id = db.Column(db.Integer, db.ForeignKey('travel_modes.id'), nullable=False)
    unit_price = db.Column(db.Numeric(12, 2), default=0)      # 交通单价（元/人次往返）
    visa_fee = db.Column(db.Numeric(12, 2), default=0)        # 签证费（元/人次，仅非国内）
    currency = db.Column(db.String(10), default='CNY')
    description = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    travel_category = db.relationship('TravelCategory', backref='person_trip_fees')
    travel_mode = db.relationship('TravelMode', backref='person_trip_fees')

    def to_dict(self):
        return {
            'id': self.id,
            'travel_category_id': self.travel_category_id,
            'travel_category_name': self.travel_category.name if self.travel_category else None,
            'travel_mode_id': self.travel_mode_id,
            'travel_mode_name': self.travel_mode.name if self.travel_mode else None,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'visa_fee': float(self.visa_fee) if self.visa_fee else 0,
            'currency': self.currency or 'CNY',
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
