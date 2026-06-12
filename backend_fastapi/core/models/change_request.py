from datetime import datetime
from db import db
from core.models.material import Material, ModuleMaterial


class ChangeRequest(db.Model):
    """变更申请模型 - 用于已归档报价单的物料/模块变更申请"""
    __tablename__ = 'change_requests'

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    
    # 变更类型: material_add(添加物料), material_update(更新物料), material_delete(删除物料)
    #           module_update(更新模块)
    change_type = db.Column(db.String(50), nullable=False)
    
    # 变更数据 (JSON): 包含 proposed_changes 和 original_data
    proposed_data = db.Column(db.Text, nullable=False)  # JSON string
    original_data = db.Column(db.Text, nullable=True)  # JSON string
    
    # 状态: pending(待审核), approved(已批准), rejected(已拒绝)
    status = db.Column(db.String(20), nullable=False, default='pending')
    
    # 申请信息
    requested_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 审核信息
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    review_remark = db.Column(db.Text, nullable=True)
    
    # 关系
    quotation = db.relationship('Quotation', backref='change_requests')
    module = db.relationship('Module', backref='change_requests')
    requester = db.relationship('User', foreign_keys=[requested_by], backref='change_requests_made')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by], backref='change_requests_reviewed')

    def to_dict(self):
        import json
        material_info = {}
        try:
            proposed = json.loads(self.proposed_data) if self.proposed_data else {}
            original = json.loads(self.original_data) if self.original_data else {}

            if self.change_type == 'material_add':
                # 新增物料：material_id 是 materials 表的ID
                material_id = proposed.get('material_id')
                if material_id:
                    mat = db.session.get(Material, material_id)
                    if mat:
                        material_info = {
                            'material_name': mat.name,
                            'brand': mat.brand,
                            'specification': mat.spec,
                            'quantity': proposed.get('quantity', 1)
                        }
            else:
                # 更新/删除物料：id 是 module_materials 表的主键
                module_material_id = original.get('id') or proposed.get('id')
                if module_material_id:
                    mm = db.session.get(ModuleMaterial, module_material_id)
                    if mm and mm.material:
                        material_info = {
                            'material_name': mm.material.name,
                            'brand': mm.material.brand,
                            'specification': mm.material.spec,
                            'quantity': original.get('quantity') or proposed.get('quantity', 1)
                        }
                    elif mm:
                        material_info = {
                            'material_name': f'物料ID:{module_material_id}',
                            'quantity': original.get('quantity') or proposed.get('quantity', 1)
                        }
        except Exception as e:
            print(f'Error getting material info: {e}')

        return {
            'id': self.id,
            'quotation_id': self.quotation_id,
            'quotation_name': self.quotation.name if self.quotation else None,
            'module_id': self.module_id,
            'module_name': self.module.name if self.module else None,
            'change_type': self.change_type,
            'proposed_data': json.loads(self.proposed_data) if self.proposed_data else {},
            'original_data': json.loads(self.original_data) if self.original_data else {},
            'status': self.status,
            'requested_by': self.requested_by,
            'requester_name': self.requester.real_name if self.requester else None,
            'requested_at': self.requested_at.isoformat() if self.requested_at else None,
            'reviewed_by': self.reviewed_by,
            'reviewer_name': self.reviewer.real_name if self.reviewer else None,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'review_remark': self.review_remark,
            **material_info
        }
