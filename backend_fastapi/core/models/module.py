from datetime import datetime
from db import db

# 模块类型枚举
MODULE_TYPE_MECHANICAL = 'mechanical'  # 机构
MODULE_TYPE_ELECTRICAL = 'electrical'  # 电气
MODULE_TYPE_OTHER = 'other'  # 其他
MODULE_TYPE_CHOICES = [MODULE_TYPE_MECHANICAL, MODULE_TYPE_ELECTRICAL, MODULE_TYPE_OTHER]

# 类型中文标签
MODULE_TYPE_LABELS = {
    MODULE_TYPE_MECHANICAL: '机构',
    MODULE_TYPE_ELECTRICAL: '电气',
    MODULE_TYPE_OTHER: '其他',
}

# 类型颜色 (前端用)
MODULE_TYPE_COLORS = {
    MODULE_TYPE_MECHANICAL: '#3b82f6',  # 蓝色
    MODULE_TYPE_ELECTRICAL: '#f59e0b',  # 橙色
    MODULE_TYPE_OTHER: '#94a3b8',  # 灰色
}

# 岗位关键词 → 模块类型映射 (从 position.name 判断)
MECHANICAL_KEYWORDS = [
    '机械', '装配', '机加', '钳工', '焊工', 'cnc', '磨床', '铣床', '车工',
    '刮研', '线切割', '激光下料', '抛光', '管道安装', '冷作', '机加工',
    '装配工', '组装', '工艺工程师', '机械工程师', '机械设计', '机械经理',
    '动力技术员', '调试', '技术员', '技师', '大组长', '代理大组长',
    '小组长', '组长', '机械组长', '装配工',
]
ELECTRICAL_KEYWORDS = [
    '电气', '电控', '电工', '电气工程师', '电气设计', '电气装配',
    '电气检验', '电力', 'plc', '自动化', '电气经理',
]


def infer_module_type_from_user(user) -> str:
    """
    根据用户岗位自动判断模块类型
    - 机构: 机械/装配/CNC/焊工 等
    - 电气: 电气/电控/电工 等
    - 其他: 高管/采购/行政 等无明确技术方向的岗位
    """
    if not user or not user.position_id:
        return MODULE_TYPE_OTHER
    # lazy load position
    position = user.position if hasattr(user, 'position') else None
    if not position or not position.name:
        return MODULE_TYPE_OTHER
    pname = position.name.lower()

    # 优先判断电气
    for kw in ELECTRICAL_KEYWORDS:
        if kw.lower() in pname:
            return MODULE_TYPE_ELECTRICAL
    # 再判断机构
    for kw in MECHANICAL_KEYWORDS:
        if kw.lower() in pname:
            return MODULE_TYPE_MECHANICAL
    # 兜底
    return MODULE_TYPE_OTHER


# 参与人类型 → 模块类型 (与前端一致, 单一来源)
# - agency → 机构
# - electrical → 电气
# - project / None / 混合 → 其他
def infer_module_type_from_participant_types(participant_types: list) -> str:
    """
    根据参与人员的 participant_type 列表推断模块类型
    - 全部 agency → mechanical (机构)
    - 全部 electrical → electrical (电气)
    - 混合 / project / 空 / None → other (其他)
    """
    types = set(t for t in participant_types if t)
    if not types:
        return MODULE_TYPE_OTHER
    if types == {'agency'}:
        return MODULE_TYPE_MECHANICAL
    if types == {'electrical'}:
        return MODULE_TYPE_ELECTRICAL
    # 混合 / 含 project / 其他类型 → 其他
    return MODULE_TYPE_OTHER


def infer_module_type_from_user_ids(db, user_ids: list) -> str:
    """
    兼容旧接口: 传入 user_id 列表
    实际从 quotation_participants 表查每个用户的参与类型 (取最新一条)
    """
    if not user_ids:
        return MODULE_TYPE_OTHER
    from core.models.user import User
    from core.models.quotation import QuotationParticipant
    rows = db.query(QuotationParticipant.user_id, QuotationParticipant.participant_type)\
        .filter(QuotationParticipant.user_id.in_(user_ids))\
        .all()
    return infer_module_type_from_participant_types([r[1] for r in rows])


class Module(db.Model):
    """模块模型"""
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(150), nullable=True, comment='英文名称')
    code = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    module_type = db.Column(db.String(20), nullable=False, default=MODULE_TYPE_OTHER, comment='模块类型: mechanical/electrical/other')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    participants = db.relationship('ModuleParticipant', backref='module', cascade='all, delete-orphan')
    materials = db.relationship('ModuleMaterial', backref='module', cascade='all, delete-orphan')

    def to_dict(self):
        total = sum(
            (float(m.unit_price_override) if m.is_other and m.unit_price_override else m.quantity * float(m.material.unit_price) if m.material and m.material.unit_price else 0)
            for m in self.materials
        )
        mt = self.module_type or MODULE_TYPE_OTHER
        return {
            'id': self.id,
            'quotation_id': self.quotation_id,
            'name': self.name,
            'name_en': self.name_en,
            'code': self.code,
            'description': self.description,
            'module_type': mt,
            'module_type_label': MODULE_TYPE_LABELS.get(mt, '其他'),
            'module_type_color': MODULE_TYPE_COLORS.get(mt, '#94a3b8'),
            'total': total,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'participants': [{'id': p.id, 'user_id': p.user_id} for p in self.participants],
            'materials': [m.to_dict() for m in self.materials]
        }


class ModuleParticipant(db.Model):
    """模块参与人员模型"""
    __tablename__ = 'module_participants'

    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
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