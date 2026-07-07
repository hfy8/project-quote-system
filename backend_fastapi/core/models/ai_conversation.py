from datetime import datetime
from db import db


class AiConversation(db.Model):
    """AI 对话会话"""
    __tablename__ = 'ai_conversations'

    id = db.Column(db.String(36), primary_key=True)  # UUID string
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False, default='新对话')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)  # null initially, set on update

    # 关系
    messages = db.relationship(
        'AiMessage', backref='conversation', lazy='dynamic',
        cascade='all, delete-orphan',
        order_by='AiMessage.created_at',
    )
    user = db.relationship('User', foreign_keys=[user_id], backref='ai_conversations')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'message_count': self.messages.count() if hasattr(self, 'messages') else 0,
        }


class AiMessage(db.Model):
    """AI 对话消息"""
    __tablename__ = 'ai_messages'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(
        db.String(36), db.ForeignKey('ai_conversations.id'), nullable=False, index=True
    )
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    tool_calls = db.Column(db.Text, nullable=True)  # JSON string, nullable
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'role': self.role,
            'content': self.content,
            'tool_calls': self.tool_calls,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
