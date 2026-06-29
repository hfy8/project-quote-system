from db import db
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


DEFAULT_TABS = [
    # project 类型（全部 Tab）
    {'participant_type': 'project', 'tab_name': 'modules', 'tab_label': '模块管理', 'type_name': '项目', 'description': '添加、编辑、删除模块', 'sort_order': 1},
    {'participant_type': 'project', 'tab_name': 'participants', 'tab_label': '参与人员', 'type_name': '项目', 'description': '管理报价单参与人员', 'sort_order': 2},
    {'participant_type': 'project', 'tab_name': 'coefficients', 'tab_label': '费用系数', 'type_name': '项目', 'description': '调整大件/核心部件/其他件系数', 'sort_order': 3},
    {'participant_type': 'project', 'tab_name': 'materials', 'tab_label': '物料清单', 'type_name': '项目', 'description': '物料选择与报价', 'sort_order': 4},
    {'participant_type': 'project', 'tab_name': 'fees', 'tab_label': '费用', 'type_name': '项目', 'description': '附加费用配置', 'sort_order': 5},
    {'participant_type': 'project', 'tab_name': 'labor', 'tab_label': '人力工时', 'type_name': '项目', 'description': '人力工时统计', 'sort_order': 6},
    {'participant_type': 'project', 'tab_name': 'summary', 'tab_label': '汇总', 'type_name': '项目', 'description': '查看费用汇总', 'sort_order': 7},
    {'participant_type': 'project', 'tab_name': 'export', 'tab_label': '导出', 'type_name': '项目', 'description': '导出 Excel/PDF', 'sort_order': 8},
    {'participant_type': 'project', 'tab_name': 'packing', 'tab_label': '运输包装', 'type_name': '项目', 'description': '运输包装配置', 'sort_order': 9},
    {'participant_type': 'project', 'tab_name': 'travel_person_days', 'tab_label': '差旅人天', 'type_name': '项目', 'description': '差旅人天统计', 'sort_order': 10},
    {'participant_type': 'project', 'tab_name': 'travel_person_trips', 'tab_label': '差旅人次', 'type_name': '项目', 'description': '差旅人次统计', 'sort_order': 11},
    # agency 类型
    {'participant_type': 'agency', 'tab_name': 'modules', 'tab_label': '模块管理', 'type_name': '机构', 'description': '查看模块', 'sort_order': 1},
    {'participant_type': 'agency', 'tab_name': 'materials', 'tab_label': '物料清单', 'type_name': '机构', 'description': '物料选择与报价', 'sort_order': 2},
    {'participant_type': 'agency', 'tab_name': 'fees', 'tab_label': '费用', 'type_name': '机构', 'description': '附加费用配置', 'sort_order': 3},
    {'participant_type': 'agency', 'tab_name': 'labor', 'tab_label': '人力工时', 'type_name': '机构', 'description': '人力工时统计', 'sort_order': 4},
    {'participant_type': 'agency', 'tab_name': 'summary', 'tab_label': '汇总', 'type_name': '机构', 'description': '查看费用汇总', 'sort_order': 5},
    {'participant_type': 'agency', 'tab_name': 'export', 'tab_label': '导出', 'type_name': '机构', 'description': '导出 Excel/PDF', 'sort_order': 6},
    {'participant_type': 'agency', 'tab_name': 'packing', 'tab_label': '运输包装', 'type_name': '机构', 'description': '运输包装配置', 'sort_order': 7},
    {'participant_type': 'agency', 'tab_name': 'travel_person_days', 'tab_label': '差旅人天', 'type_name': '机构', 'description': '差旅人天统计', 'sort_order': 8},
    {'participant_type': 'agency', 'tab_name': 'travel_person_trips', 'tab_label': '差旅人次', 'type_name': '机构', 'description': '差旅人次统计', 'sort_order': 9},
    # electrical 类型
    {'participant_type': 'electrical', 'tab_name': 'modules', 'tab_label': '模块管理', 'type_name': '电气', 'description': '查看模块', 'sort_order': 1},
    {'participant_type': 'electrical', 'tab_name': 'materials', 'tab_label': '物料清单', 'type_name': '电气', 'description': '物料选择与报价', 'sort_order': 2},
    {'participant_type': 'electrical', 'tab_name': 'fees', 'tab_label': '费用', 'type_name': '电气', 'description': '附加费用配置', 'sort_order': 3},
    {'participant_type': 'electrical', 'tab_name': 'labor', 'tab_label': '人力工时', 'type_name': '电气', 'description': '人力工时统计', 'sort_order': 4},
    {'participant_type': 'electrical', 'tab_name': 'summary', 'tab_label': '汇总', 'type_name': '电气', 'description': '查看费用汇总', 'sort_order': 5},
    {'participant_type': 'electrical', 'tab_name': 'export', 'tab_label': '导出', 'type_name': '电气', 'description': '导出 Excel/PDF', 'sort_order': 6},
    {'participant_type': 'electrical', 'tab_name': 'packing', 'tab_label': '运输包装', 'type_name': '电气', 'description': '运输包装配置', 'sort_order': 7},
    {'participant_type': 'electrical', 'tab_name': 'travel_person_days', 'tab_label': '差旅人天', 'type_name': '电气', 'description': '差旅人天统计', 'sort_order': 8},
    {'participant_type': 'electrical', 'tab_name': 'travel_person_trips', 'tab_label': '差旅人次', 'type_name': '电气', 'description': '差旅人次统计', 'sort_order': 9},
    # supplier 类型
    {'participant_type': 'supplier', 'tab_name': 'packing', 'tab_label': '运输包装', 'type_name': '供应商', 'description': '运输包装配置', 'sort_order': 1},
    {'participant_type': 'supplier', 'tab_name': 'travel_person_days', 'tab_label': '差旅人天', 'type_name': '供应商', 'description': '差旅人天统计', 'sort_order': 2},
    {'participant_type': 'supplier', 'tab_name': 'travel_person_trips', 'tab_label': '差旅人次', 'type_name': '供应商', 'description': '差旅人次统计', 'sort_order': 3},
]
