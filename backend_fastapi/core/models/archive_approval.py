"""报价单归档审批记录"""
from datetime import datetime
from db import db


class ArchiveApproval(db.Model):
    __tablename__ = "archive_approvals"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey("quotations.id", ondelete="CASCADE"), nullable=False, index=True)
    requested_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    requested_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    approver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="pending")  # pending/approved/rejected/cancelled
    reject_reason = db.Column(db.Text, nullable=True)
    via = db.Column(db.String(20), nullable=False, default="approval")  # approval/admin
    remark = db.Column(db.Text, nullable=True)
    extra_metadata = db.Column("metadata", db.JSON, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "quotation_id": self.quotation_id,
            "requested_by": self.requested_by,
            "requested_at": self.requested_at.isoformat() if self.requested_at else None,
            "approver_id": self.approver_id,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "status": self.status,
            "reject_reason": self.reject_reason,
            "via": self.via,
            "remark": self.remark,
            "metadata": self.extra_metadata,
        }