"""纯 SQLAlchemy 启动模块 - 替代 Flask-SQLAlchemy

不依赖 Flask、也不依赖 core 包。

设计目标：
- 让 `from db import db` 可用
- 让 `from core.models import X` 也可用（向后兼容 shim）
- `db.Model` / `db.Column` / `db.relationship` / `db.BigInteger` 等代理到纯 SQLAlchemy 类
- `db.query` / `db.add` / `db.commit` / `db.delete` / `db.flush` / `db.session` / `db.rollback` 全部工作
- 所有 SQLAlchemy models（继承 `db.Model`）自动注册到 `db.Model.metadata`
"""
import os
from sqlalchemy import (
    create_engine, BigInteger, Boolean, Column, Date, DateTime, Float, JSON,
    ForeignKey, Integer, Numeric, SmallInteger, String, Table as _make_table, Text, Time,
    or_, and_, not_, func,
    UniqueConstraint, CheckConstraint, Index,
)
from sqlalchemy.orm import declarative_base, relationship, backref, sessionmaker, scoped_session, \
    joinedload, selectinload, contains_eager
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept


# 显式延迟加载 Config（避免 import 时的循环依赖）
def _get_config():
    """延迟导入 Config - 必须在 main.py 先 import core.config"""
    from core.config import Config
    return Config


# ============== 引擎 + Session 工厂 ==============
def _make_engine():
    """根据 Config 构造引擎（延迟初始化）"""
    Config = _get_config()
    return create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)


def _make_session_factory():
    Config = _get_config()
    return sessionmaker(bind=_make_engine(), expire_on_commit=False)


# 第一次访问时再创建（避免 import 时就建立连接）
_engine = None
_SessionFactory = None
_ScopedSession = None


def engine():
    """懒加载 engine"""
    global _engine
    if _engine is None:
        _engine = _make_engine()
    return _engine


def db_session_factory():
    """返回一个新的 Session"""
    global _SessionFactory, _ScopedSession
    if _SessionFactory is None:
        _SessionFactory = _make_session_factory()
        _ScopedSession = scoped_session(_SessionFactory)
    return _ScopedSession()


# ============== Model Base（declarative_base） ==============
# 自定义 metaclass 注入 Flask-SQL-Alchemy 风格的 Model.query 类属性
# 必须继承 DeclarativeAttributeIntercept 才能与 DeclarativeBase 一起用


class _ModelQueryMeta(DeclarativeAttributeIntercept):
    """让 Model.query 等价于 db.session.query(Model)（类级别）"""
    def __getattr__(cls, name):
        if name == 'query':
            return db.query(cls)
        raise AttributeError(f"type object '{cls.__name__}' has no attribute '{name}'")


class ModuleBase(DeclarativeBase, metaclass=_ModelQueryMeta):
    """纯 SQLAlchemy 2.x Base + Flask-SQL-Alchemy 风格的 .query 类属性"""
    pass


# ============== db 代理类 ==============
class _DBProxy:
    """让 db.query() / db.add() / db.commit() 等 Flask-SQL-Alchemy 风格 API 继续可用

    实际代理到：
    - class 属性 (db.Model, db.Column, ...) → 纯 SQLAlchemy 类
    - session 方法 (db.query, db.add, ...) → 当前的 scoped_session
    """

    # === class 属性代理（让 db.Model = ModuleBase, db.Column = Column, ...）===
    # 注意：所有 SQLAlchemy 类（Column, relationship, backref, association_proxy）
    # 都要包成 staticmethod，否则在 db.XXX 访问时 Python 会把它当 unbound method，
    # 第一个 positional 参数会被解释为 self
    Model = ModuleBase
    Column = staticmethod(Column)
    relationship = staticmethod(relationship)
    backref = staticmethod(backref)
    # db.Table 是 Flask-SQL-Alchemy 风格的关联表，隐式绑定到 db.Model.metadata
    # 签名: Table(name, *columns, **kwargs) - 自动在 args 前面注入 metadata
    @staticmethod
    def Table(name, *args, **kwargs):
        if 'metadata' in kwargs:
            # 显式给了 metadata 就用显式的
            return _make_table(name, *args, **kwargs)
        # 把 metadata 注入到第二个位置（SQLAlchemy 规范）
        return _make_table(name, ModuleBase.metadata, *args, **kwargs)

    BigInteger = staticmethod(BigInteger)
    Boolean = staticmethod(Boolean)
    Date = staticmethod(Date)
    DateTime = staticmethod(DateTime)
    Float = staticmethod(Float)
    ForeignKey = staticmethod(ForeignKey)
    Integer = staticmethod(Integer)
    JSON = staticmethod(JSON)
    Numeric = staticmethod(Numeric)
    SmallInteger = staticmethod(SmallInteger)
    String = staticmethod(String)
    # Table 用 @staticmethod 包装（自动注入 metadata）
    Text = staticmethod(Text)
    Time = staticmethod(Time)
    UniqueConstraint = staticmethod(UniqueConstraint)
    CheckConstraint = staticmethod(CheckConstraint)
    Index = staticmethod(Index)
    association_proxy = staticmethod(association_proxy)

    # === session 方法代理 ===
    @property
    def session(self):
        """返回当前线程的 session"""
        return db_session_factory()

    def query(self, *args, **kwargs):
        return self.session.query(*args, **kwargs)

    def add(self, obj):
        self.session.add(obj)

    def add_all(self, objs):
        self.session.add_all(objs)

    def delete(self, obj):
        self.session.delete(obj)

    def flush(self):
        self.session.flush()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def execute(self, *args, **kwargs):
        return self.session.execute(*args, **kwargs)

    def merge(self, obj):
        return self.session.merge(obj)

    def refresh(self, obj):
        self.session.refresh(obj)

    def expunge(self, obj):
        self.session.expunge(obj)

    def expunge_all(self):
        self.session.expunge_all()

    def begin(self):
        return self.session.begin()

    def begin_nested(self):
        return self.session.begin_nested()

    def close(self):
        self.session.close()

    @property
    def or_(self):
        return or_

    @property
    def and_(self):
        return and_

    @property
    def not_(self):
        return not_

    @property
    def func(self):
        return func

    def contains_eager(self, *args, **kwargs):
        return contains_eager(*args, **kwargs)

    def joinedload(self, *args, **kwargs):
        return joinedload(*args, **kwargs)

    def selectinload(self, *args, **kwargs):
        return selectinload(*args, **kwargs)


# 全局单例
db = _DBProxy()


# ============== 便捷函数 ==============
def get_db_session():
    """FastAPI 依赖函数（兼容旧 import 路径）"""
    session = db_session_factory()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
