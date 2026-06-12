from datetime import datetime
from db import db


class Message(db.Model):
    """消息模型"""
    __tablename__ = 'messages'

    id = db.Column(db.BigInteger, primary_key=True)
    sender_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=True)  # 系统消息sender为NULL
    recipient_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # module_member_added/change_request_submitted/change_request_approved/change_request_rejected/version_updated
    related_id = db.Column(db.BigInteger, nullable=True)  # 关联的报价单/变更申请ID
    related_type = db.Column(db.String(50), nullable=True)  # quotation/change_request
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')

    def to_dict(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'sender_name': self.sender.real_name if self.sender else '系统',
            'recipient_id': self.recipient_id,
            'recipient_name': self.recipient.real_name if self.recipient else None,
            'title': self.title,
            'content': self.content,
            'type': self.type,
            'related_id': self.related_id,
            'related_type': self.related_type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }