"""数据库初始化脚本 (Docker 部署用)

功能:
1. CREATE EXTENSION IF NOT EXISTS vector (pgvector)
2. db.create_all() 建所有表
3. 创建默认 admin 用户
4. 初始化基础数据 (角色/权限/物料分类/差旅配置)
"""
import sys
import os

# 把 /app 加到 sys.path (而不是 scripts 目录), 这样才能 import db.py (单文件模块)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import _make_engine, db_session_factory, ModuleBase
from core.config import Config
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker


def init_extensions(engine):
    """建 pgvector 扩展"""
    print("🔌 启用 pgvector 扩展...")
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
        conn.execute(text('CREATE EXTENSION IF NOT EXISTS "pgcrypto"'))
        conn.execute(text('CREATE EXTENSION IF NOT EXISTS "pg_trgm"'))
        conn.commit()
    print("   ✅ 扩展已启用")


def init_tables(engine):
    """建所有表"""
    print("📋 建表 (db.create_all)...")
    # 导入所有 model 让 metadata 注册
    from core.models import (
        user, role, permission, role_permission, user_role,
        quotation, module, material, module_participant, quotation_participant,
        labor_hour, travel, travel_entry, packing, fee, fee_rate, exchange_rate,
        version, message, knowledge, change_request, participant_type_permission,
    )
    ModuleBase.metadata.create_all(engine)
    print("   ✅ 表已建")


def init_admin(session):
    """建默认 admin 用户"""
    from core.models.user import User
    admin = session.query(User).filter_by(username='admin').first()
    if admin:
        print(f"   admin 已存在: id={admin.id}")
        return

    admin = User(
        username='admin',
        real_name='系统管理员',
        role='admin',  # 用 role 字段标识
        is_active=True,
    )
    admin.set_password('admin123')
    session.add(admin)
    session.commit()
    print(f"   ✅ admin 已建: id={admin.id}, 默认密码 admin123")


def init_data(session):
    """基础数据: 角色/差旅配置/物料分类/汇率"""
    from core.models.permission import Role
    from core.models.exchange_rate import ExchangeRate
    from core.models.travel import TravelCategory, TravelMode, TravelDayRate, TravelPersonTripFee
    from core.models.packing import PackingType

    # 角色（code 必填，name 描述）
    for code, name, desc in [
        ('admin', '系统管理员', '拥有所有权限'),
        ('manager', '经理', '业务管理'),
        ('business', '业务员', '报价单业务'),
        ('purchaser', '采购员', '物料管理'),
        ('viewer', '查看者', '只读'),
    ]:
        if not session.query(Role).filter_by(code=code).first():
            session.add(Role(code=code, name=name, description=desc))
    session.commit()

    # 汇率
    default_rates = [
        ('CNY', 1.0), ('USD', 7.25), ('EUR', 7.85), ('GBP', 9.15),
        ('JPY', 0.048), ('HKD', 0.93),
    ]
    for cur, rate in default_rates:
        if not session.query(ExchangeRate).filter_by(currency=cur).first():
            session.add(ExchangeRate(currency=cur, rate=rate))
    session.commit()

    # 差旅分类
    cats = [
        ('国内', 'domestic'), ('亚洲', 'asia'), ('欧洲', 'europe'),
        ('美洲', 'americas'), ('非洲', 'africa'), ('大洋洲', 'oceania'), ('中东', 'middle_east'),
    ]
    for name, code in cats:
        if not session.query(TravelCategory).filter_by(code=code).first():
            session.add(TravelCategory(name=name, code=code))
    session.commit()

    # 出行方式
    modes = [('飞机', 'flight'), ('高铁', 'train'), ('汽车', 'car'), ('轮船', 'ship'), ('其他', 'other')]
    for name, code in modes:
        if not session.query(TravelMode).filter_by(code=code).first():
            session.add(TravelMode(name=name, code=code))
    session.commit()

    # 包装类型
    pkgs = [('纸箱', 50), ('木箱', 200), ('托盘', 500), ('缠绕膜', 30), ('其他', 0)]
    for name, price in pkgs:
        if not session.query(PackingType).filter_by(name=name).first():
            session.add(PackingType(name=name, unit_price=price, is_active=True))
    session.commit()

    # 费用分类费率
    from core.models.fee_rate import FeeRate
    for cat, rate in [('大件', 1.2), ('核心部件', 1.0), ('其他件', 1.1)]:
        if not session.query(FeeRate).filter_by(category=cat).first():
            session.add(FeeRate(category=cat, rate=rate))
    session.commit()

    print("   ✅ 基础数据已初始化")


def main():
    print("=" * 50)
    print("  Project Quote System - DB Init (v17)")
    print("=" * 50)

    engine = _make_engine()

    # 测试连接
    try:
        with engine.connect() as conn:
            ver = conn.execute(text("SELECT version()")).scalar()
            print(f"📡 已连接: {ver[:50]}")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        sys.exit(1)

    init_extensions(engine)
    init_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        init_admin(session)
        init_data(session)
    finally:
        session.close()

    print("=" * 50)
    print("✅ 数据库初始化完成！")
    print("   admin / admin123")


if __name__ == '__main__':
    main()
