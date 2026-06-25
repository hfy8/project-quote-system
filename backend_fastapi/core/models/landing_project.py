"""已落地项目表

数据来源: 外部项目管理系统 http://222.92.47.101/prod-api/project/list
用途: 报价单列表显示项目落地状态, 落地项目禁止撤销归档

特点:
- scheme_no 是核心关联字段 (与报价单 scheme_no 对应)
- 存外部完整数据 (full_data JSONB), 后续字段扩展无需改表
- 30 分钟全量 UPSERT 同步
"""
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from db import db


class LandingProject(db.Model):
    """已落地项目记录"""
    __tablename__ = 'landing_projects'

    scheme_no = db.Column(db.String(50), primary_key=True, comment='项目编号, 关联报价单 scheme_no')
    external_project_id = db.Column(db.String(50), index=True, comment='外部系统 project_id')
    scheme_name = db.Column(db.String(200), comment='项目名称')
    customer_name = db.Column(db.String(200), comment='客户名称')
    project_manager_name = db.Column(db.String(100), comment='项目经理姓名')
    project_status = db.Column(db.String(50), index=True, comment='项目状态 (IN_PROGRESS/COMPLETED/...)')
    archive_status = db.Column(db.Boolean, default=False, comment='是否归档')

    # 外部完整数据, 用于后续字段扩展 (如 contact_phone, contract_code 等)
    full_data = db.Column(JSON, comment='外部接口完整响应 JSON')

    # 同步元信息
    first_synced_at = db.Column(db.DateTime, default=datetime.utcnow, comment='首次同步时间')
    last_synced_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='最近同步时间')

    def to_dict(self):
        return {
            'scheme_no': self.scheme_no,
            'external_project_id': self.external_project_id,
            'scheme_name': self.scheme_name,
            'customer_name': self.customer_name,
            'project_manager_name': self.project_manager_name,
            'project_status': self.project_status,
            'archive_status': self.archive_status,
            'first_synced_at': self.first_synced_at.isoformat() if self.first_synced_at else None,
            'last_synced_at': self.last_synced_at.isoformat() if self.last_synced_at else None,
        }
