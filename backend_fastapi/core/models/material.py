from datetime import datetime
from db import db


class Material(db.Model):
    """原材料模型"""
    __tablename__ = 'materials'

    id = db.Column(db.Integer, primary_key=True)
    item_no = db.Column(db.String(50), nullable=True, index=True)  # 品号 (跨系统同步用, 允许为空)
    name = db.Column(db.String(100), nullable=False, index=True)
    # 产品名称 (产品线/分类) — migration 018
    # 与 name (品名/具体型号) 是两个独立维度:
    #   - product_name: 跨多个具体物料的产品线名 (如"四轴机械手"、"点激光检测")
    #   - name: 单个物料的具体型号名
    product_name = db.Column(db.String(100), nullable=True, index=True)
    spec = db.Column(db.String(100), nullable=True, index=True)
    brand = db.Column(db.String(50), nullable=True, index=True)
    unit = db.Column(db.String(20), nullable=True)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    category = db.Column(db.String(20), nullable=False, default='核心部件', index=True)  # 大件/核心部件/其他件
    # 物料类型 (机械类/非机械类) — 与 category 是两个独立维度
    # 取值: 'mechanical' (机械类), 'electrical' (非机械类-电控), 'other' (其他)
    # migration 016
    material_type = db.Column(db.String(20), nullable=False, default='other', index=True)
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
            'product_name': self.product_name,  # 产品名称 (产品线) — migration 018
            'spec': self.spec,
            'brand': self.brand,
            'unit': self.unit,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'category': self.category,
            'material_type': self.material_type,  # 机械类/非机械类 — migration 016
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
    # 快照物料类型 (机械类/非机械类) — migration 017
    # 添加物料时从 materials.material_type 读一次写入, 后续物料 type 改了也不影响历史报价单
    # 跟 operation_log 的 employee_no + cn_name 快照思路一致
    material_type = db.Column(db.String(20), nullable=False, default='other', index=True)
    # 快照产品名称 (产品线) — migration 019
    # 跟 material_type 一致, 防止物料表 product_name 修改影响历史报价单
    product_name = db.Column(db.String(100), nullable=True, index=True)
    # 快照部件分类 — migration 019
    category = db.Column(db.String(20), nullable=True, index=True)
    # 自制件标记 — migration 020
    # true 表示这个物料在原材料库没有, 是用户手动填写的 (品名/规格/单位/品牌/关键参数 全部用 custom_data JSONB 存)
    # 自制件不进物料库, 不进"导出无品号物料"列表
    is_custom = db.Column(db.Boolean, nullable=False, default=False, index=True)
    # 自制件字段 JSONB — migration 020
    # 存: {name, spec, unit, brand, unit_price, param1, param2, param3}
    # unit_price 也存 unit_price_override (传统字段), 这里存 JSONB 是便于整体序列化
    custom_data = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    material = db.relationship('Material', backref='module_materials')
    selected_by = db.relationship('User', backref='selected_materials')

    def to_dict(self):
        # 自制件分支 (migration 020) - 物料字段全从 custom_data JSONB 扁平化
        if self.is_custom:
            cd = self.custom_data or {}
            unit_price = float(cd.get('unit_price', 0) or 0)
            qty = self.quantity if self.quantity else 1
            return {
                'id': self.id,
                'module_id': self.module_id,
                'material_id': None,
                'is_custom': True,
                'quantity': qty,
                'selected_by_id': self.selected_by_id,
                'selected_by_name': self.selected_by.real_name if self.selected_by else None,
                'created_at': self.created_at.isoformat() if self.created_at else None,
                # 从 JSONB 扁平化字段 (前端 el-table 不需要加新列)
                'material_name': cd.get('name'),
                'item_no': None,  # 自制件无品号 → 前端会跳过"导出无品号物料"
                'specification': cd.get('spec'),
                'brand': cd.get('brand'),
                'unit': cd.get('unit'),
                'unit_price': unit_price,
                'unit_price_override': unit_price,
                'is_other': False,
                # 复用现有快照字段 (mm 自身存的, 不依赖 Material)
                'material_category': self.category,
                'category': self.category,
                'material_status': None,
                'material_type': self.material_type,
                'product_name': self.product_name,
                'param1': cd.get('param1'),
                'param2': cd.get('param2'),
                'param3': cd.get('param3'),
                'subtotal': qty * unit_price,  # 自制件支持数量
            }
        # 正常物料分支
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
            # 部件分类快照 (migration 019) - 优先用 self.category, 老数据无快照时回退到 m.category
            'material_category': self.category or (m.category if m else None),
            'category': self.category or (m.category if m else None),  # 导出 Excel 用
            'material_status': m.status if m else None,
            # 物料类型快照 (机械类/非机械类) — migration 017
            # mm 自身存的 type, 跟 m.material_type 可能不同 (历史快照)
            'material_type': self.material_type,
            # 产品名称快照 (migration 019) - 优先用 self.product_name, 老数据无快照时回退到 m.product_name
            'product_name': self.product_name or (m.product_name if m else None),
            # 关键参数
            'param1': m.param1 if m else None,
            'param2': m.param2 if m else None,
            'param3': m.param3 if m else None,
            # 小计
            'subtotal': subtotal,
        }