from datetime import datetime
from app import db


class VersionSnapshot(db.Model):
    """版本快照模型"""
    __tablename__ = 'version_snapshots'

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey('quotations.id'), nullable=False)
    version_no = db.Column(db.Integer, nullable=False)
    snapshot_data = db.Column(db.Text, nullable=False)  # JSON字符串
    operation_type = db.Column(db.String(20), nullable=False)
    remark = db.Column(db.Text, nullable=True)
    operator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    word_file = db.Column(db.String(500), nullable=True, comment='Word文件路径')
    pdf_file = db.Column(db.String(500), nullable=True, comment='PDF文件路径')

    operator = db.relationship('User', backref='version_operations')

    def to_dict(self):
        return {
            'id': self.id,
            'quotation_id': self.quotation_id,
            'version_no': self.version_no,
            'snapshot_data': self.snapshot_data,
            'operation_type': self.operation_type,
            'remark': self.remark,
            'operator_id': self.operator_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'word_file': self.word_file,
            'pdf_file': self.pdf_file,
        }