from datetime import datetime
from db import db


class Material(db.Model):
    """原材料模型"""
    __tablename__ = 'materials'

    id = db.Column(db.Integer, primary_key=True)
    item_no = db.Column(db.String(50), nullable=True, index=True)  # 品号 (跨系统同步用, 允许为空)
    name = db.Column(db.String(100), nullable=False, index=True)
    spec = db.Column(db.String(100), nullable=True, index=True)
    brand = db.Column(db.String(50), nullable=True, index=True)
    unit = db.Column(db.String(20), nullable=True)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    category = db.Column(db.String(20), nullable=False, default='核心部件', index=True)  # 大件/核心部件/其他件
    # 三项关键参数（灵活字段，机构/电控选料参考）
    param1 = db.Column(db.String(100), nullable=True)   # 关键参数01
    param2 = db.Column(db.String(100), nullable=True)  # 关键参数02
    param3 = db.Column(db.String(100), nullable=True)   # 关键参数03
    status = db.Column(db.String(20), nullable=False, default='active', index=True)  # active/inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 价格同步跟踪字段 (migration 012)
    last_price_synced_at = db.Column(db.DateTime, nullable=True)
    last_price_sync_status = db.Column(db.String(20), nullable=True)  # success/failed/skipped/pending
    last_price_sync_error = db.Column(db.Text, nullable=True)
    last_price_sync_source = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'item_no': self.item_no,
            'name': self.name,
            'spec': self.spec,
            'brand': self.brand,
            'unit': self.unit,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'category': self.category,
            'param1': self.param1,
            'param2': self.param2,
            'param3': self.param3,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            # 价格同步状态
            'last_price_synced_at': self.last_price_synced_at.isoformat() if self.last_price_synced_at else None,
            'last_price_sync_status': self.last_price_sync_status,
            'last_price_sync_error': self.last_price_sync_error,
            'last_price_sync_source': self.last_price_sync_source,
        }


class ModuleMaterial(db.Model):
    """模块物料关联模型"""
    __tablename__ = 'module_materials'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False, index=True)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False, index=True)
    is_other = db.Column(db.Boolean, default=False)  # true 表示其他类物料
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price_override = db.Column(db.Numeric(10, 2), nullable=True)  # 仅material_id=24时使用
    selected_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    material = db.relationship('Material', backref='module_materials')
    selected_by = db.relationship('User', backref='selected_materials')

    def to_dict(self):
        m = self.material
        if self.is_other and self.unit_price_override is not None:
            unit_price = float(self.unit_price_override)
            subtotal = unit_price  # 数量固定1
        else:
            unit_price = float(m.unit_price) if m and m.unit_price else 0
            subtotal = self.quantity * unit_price
        return {
            'id': self.id,
            'module_id': self.module_id,
            'material_id': self.material_id,
            'quantity': self.quantity,
            'selected_by_id': self.selected_by_id,
            'selected_by_name': self.selected_by.real_name if self.selected_by else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            # 扁平化物料字段
            'material_name': m.name if m else None,
            'item_no': m.item_no if m else None,  # 品号 (跨系统同步用)
            'specification': m.spec if m else None,
            'brand': m.brand if m else None,
            'unit': m.unit if m else None,
            'unit_price': unit_price,
            'unit_price_override': float(self.unit_price_override) if self.unit_price_override else None,
            'is_other': self.is_other,
            'material_category': m.category if m else None,
            'material_status': m.status if m else None,
            # 关键参数
            'param1': m.param1 if m else None,
            'param2': m.param2 if m else None,
            'param3': m.param3 if m else None,
            # 小计
            'subtotal': subtotal,
        }