"""AI 知识库模型 - 业务规范 / FAQ / 历史经验
"""
from datetime import datetime
from db import db
from pgvector.sqlalchemy import Vector


class KnowledgeDoc(db.Model):
    """AI 知识库文档
    用于 RAG 检索，存储业务规范、FAQ、历史经验等文本
    """
    __tablename__ = 'ai_knowledge_base'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    doc_type = db.Column(db.String(30), nullable=False, index=True)  # spec/faq/experience/rule
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.String(500))  # 逗号分隔的检索关键词
    source = db.Column(db.String(100))  # 来源（admin/auto/system）
    created_by = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # RAG v2: embedding 相关字段（pgvector）
    embedding = db.Column(Vector(1024))  # pgvector 原生向量类型
    embedding_model = db.Column(db.String(50))  # 'mini/m3e' / 'mock'
    embedding_updated_at = db.Column(db.DateTime)  # 最近一次 embedding 计算时间

    def to_dict(self):
        return {
            'id': self.id,
            'doc_type': self.doc_type,
            'title': self.title,
            'content': self.content,
            'keywords': self.keywords.split(',') if self.keywords else [],
            'source': self.source,
            'created_by': self.created_by,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'has_embedding': bool(self.embedding is not None),
            'embedding_model': self.embedding_model,
        }
