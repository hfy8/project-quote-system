from app import db
from datetime import datetime


class ParticipantTypePermission(db.Model):
    """参与人员类型权限配置"""
    __tablename__ = 'participant_type_permissions'

    id = db.Column(db.Integer, primary_key=True)
    participant_type = db.Column(db.String(50), nullable=False)  # project / agency / electrical
    tab_name = db.Column(db.String(50), nullable=False)          # modules / participants / coefficients / materials / fees / summary / versions / export
    tab_label = db.Column(db.String(100), nullable=False)       # 中文标签：模块管理 / 参与人员 / 费用系数 / 物料 / 费用 / 汇总 / 版本 / 导出
    description = db.Column(db.String(500), nullable=True)     # 说明
    type_name = db.Column(db.String(100), nullable=True)           # 分类中文名，如"项目"、"机构"、"电气"
    sort_order = db.Column(db.Integer, default=0)               # 排序
    is_disabled = db.Column(db.Boolean, default=False)         # 是否禁用
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('participant_type', 'tab_name', name='uq_participant_type_tab'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'participant_type': self.participant_type,
            'tab_name': self.tab_name,
            'tab_label': self.tab_label,
            'description': self.description,
            'type_name': self.type_name,
            'sort_order': self.sort_order,
            'is_disabled': self.is_disabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
