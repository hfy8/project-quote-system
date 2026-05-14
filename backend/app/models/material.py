from datetime import datetime
from app import db


class Material(db.Model):
    """原材料模型"""
    __tablename__ = 'materials'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    spec = db.Column(db.String(100), nullable=True)
    brand = db.Column(db.String(50), nullable=True)
    unit = db.Column(db.String(20), nullable=True)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    category = db.Column(db.String(20), nullable=False, default='普通件')  # 大件/普通件/其他件
    status = db.Column(db.String(20), nullable=False, default='active')  # active/inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'spec': self.spec,
            'brand': self.brand,
            'unit': self.unit,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'category': self.category,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class ModuleMaterial(db.Model):
    """模块物料关联模型"""
    __tablename__ = 'module_materials'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('materials.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    selected_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    material = db.relationship('Material', backref='module_materials')
    selected_by = db.relationship('User', backref='selected_materials')

    def to_dict(self):
        m = self.material
        unit_price = float(m.unit_price) if m and m.unit_price else 0
        subtotal = self.quantity * unit_price
        return {
            'id': self.id,
            'module_id': self.module_id,
            'material_id': self.material_id,
            'quantity': self.quantity,
            'selected_by_id': self.selected_by_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            # 扁平化物料字段
            'material_name': m.name if m else None,
            'specification': m.spec if m else None,
            'brand': m.brand if m else None,
            'unit': m.unit if m else None,
            'unit_price': unit_price,
            'material_category': m.category if m else None,
            'material_status': m.status if m else None,
            # 小计
            'subtotal': subtotal,
        }