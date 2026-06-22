"""Seed 脚本：清空所有报价单依赖 + 重建 25 个草稿状态报价单

用 DELETE 不用 TRUNCATE（避免阻塞），逐表删除带 CASCADE 防止外键失败
"""
import sys
import time
import random
from datetime import datetime, timedelta

sys.path.insert(0, '/home/rs8568/project-quote-system/backend_fastapi')
from db import _make_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from core.models.quotation import Quotation, QuotationParticipant
from core.models.module import Module, ModuleParticipant
from core.models.material import Material, ModuleMaterial
from core.models.labor_hour import LaborHour
from core.models.travel_entry import TravelPersonDays, TravelPersonTrip, PackingEntry
from core.models.packing import PackingType
from core.models.user import User

random.seed(42)

engine = _make_engine()
Session = sessionmaker(bind=engine)
session = Session()

# ============== 1. 清空所有依赖表 ==============
print('🗑️  清空现有数据...', flush=True)
# 按依赖顺序删除：先子表后主表
delete_order = [
    'operation_logs', 'version_snapshots',
    'packing_entries', 'travel_person_trips', 'travel_person_days',
    'labor_hours', 'module_materials', 'module_participants',
    'quotation_participants', 'modules', 'other_fees',
    'quotations',
]
for table in delete_order:
    t0 = time.time()
    res = session.execute(text(f'DELETE FROM {table}'))
    session.commit()
    print(f'   {table}: {res.rowcount} 行 ({time.time()-t0:.1f}s)', flush=True)
print('✅ 清空完成')

# ============== 2. 基础数据 ==============
print('\n📦 加载基础数据...', flush=True)
admin = session.query(User).filter_by(username='admin').first()
users = session.query(User).filter(User.id != admin.id).limit(5).all()
print(f'   admin: id={admin.id}')
print(f'   其他用户数: {len(users)}')

materials = session.query(Material).filter_by(status='active').limit(50).all()
print(f'   可用物料: {len(materials)}')

travel_cats_count = session.execute(text('SELECT count(*) FROM travel_categories')).scalar()
travel_modes_count = session.execute(text('SELECT count(*) FROM travel_modes')).scalar()
travel_day_rates_count = session.execute(text('SELECT count(*) FROM travel_day_rates')).scalar()
travel_person_fees = session.query(text('SELECT * FROM travel_person_trip_fees LIMIT 10')).all() if False else None
# 直接查
from core.models.travel import TravelPersonTripFee
travel_person_fees = session.query(TravelPersonTripFee).all()
travel_day_rates = session.execute(text('SELECT * FROM travel_day_rates')).all()
# 转成字典
day_rate_list = [dict(row._mapping) for row in travel_day_rates]
print(f'   差旅分类: {travel_cats_count}, 出行方式: {travel_modes_count}')
print(f'   人天单价: {len(day_rate_list)}, 人次单价: {len(travel_person_fees)}')

packing_types = session.query(PackingType).filter_by(is_active=True).all()
print(f'   包装类型: {len(packing_types)}')

if not materials or len(travel_person_fees) < 1:
    print('❌ 缺少基础数据')
    sys.exit(1)

# ============== 3. 模拟数据池 ==============
customers = ['宁德时代', '比亚迪', '华为', '富士康', '特斯拉', '蔚来', '理想', '小米', 'OPPO', 'vivo',
             '海尔', '美的', '格力', '三一重工', '徐工', '中联重科', '宝钢', '中国石化', '国家电网', '中航工业']
projects_single = ['老化测试台', '单机检测设备', '性能测试机', '振动测试台', '环境试验箱', '包装设备',
                   '贴片机', '焊接机器人', 'AGV小车', '智能仓储', '分拣系统', '输送线', '升降平台',
                   '数控机床', '激光切割机', '3D打印机', '注塑机', '冲压机', '喷涂机器人', '装配线']
projects_line = ['动力电池模组装配线', '电芯自动化产线', 'PACK总成生产线', '电机智能装配线', '电控测试产线']
modules_pool = ['上料模块', '定位模块', '检测模块', '焊接模块', '装配模块', '下料模块', '搬运模块', '测试模块']
labor_names = ['机械设计', '电气设计', '软件调试', '装配', '调试', '现场安装', '编程', '测试验证']

# ============== 4. 创建 20 个单机 ==============
print('\n📝 创建 20 个单机报价单...', flush=True)
created_singles = []
for i in range(20):
    customer = random.choice(customers)
    project = random.choice(projects_single)
    q = Quotation(
        name=f'{customer}{project}202606-{i+1:02d}',
        type='single',
        scheme_no=f'DJ{202606}{i+1:03d}',
        status='draft',
        business_owner_id=random.choice(users).id if users else admin.id,
        creator_id=admin.id,
        tax_rate=0.13,
        profit_rate=round(random.uniform(0.10, 0.20), 4),
        currency='CNY',
        current_version=1,
        parent_id=None,
        coefficients={'large': 1.0, 'standard': 1.0, 'other': 1.0},
        created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
    )
    session.add(q)
    session.flush()
    created_singles.append(q)
print(f'   ✅ 单机: {len(created_singles)} 个')

# ============== 5. 创建 5 个线体 + 子报价单 ==============
print('\n📝 创建 5 个线体报价单 + 子报价单...', flush=True)
line_quotations = []
created_children = []
for i in range(5):
    customer = random.choice(customers)
    project = random.choice(projects_line)
    parent = Quotation(
        name=f'{customer}{project}202606-L{i+1:02d}',
        type='line',
        scheme_no=f'XT{202606}{i+1:03d}',
        status='draft',
        business_owner_id=random.choice(users).id if users else admin.id,
        creator_id=admin.id,
        tax_rate=0.13,
        profit_rate=round(random.uniform(0.12, 0.22), 4),
        currency='CNY',
        current_version=1,
        parent_id=None,
        coefficients={'large': 1.0, 'standard': 1.0, 'other': 1.0},
        created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
    )
    session.add(parent)
    session.flush()
    line_quotations.append(parent)

    n_children = random.randint(1, 4)
    for j in range(n_children):
        child = Quotation(
            name=f'{parent.name}-子项{j+1:02d}',
            type='single',
            scheme_no=f'{parent.scheme_no}-C{j+1:02d}',
            status='draft',
            business_owner_id=parent.business_owner_id,
            creator_id=admin.id,
            tax_rate=parent.tax_rate,
            profit_rate=parent.profit_rate,
            currency='CNY',
            current_version=1,
            parent_id=parent.id,
            coefficients=parent.coefficients,
            created_at=parent.created_at + timedelta(days=j+1),
        )
        session.add(child)
        session.flush()
        created_children.append(child)
    print(f'   线体 {i+1}: {parent.name} → {n_children} 子报价单')

print(f'   ✅ 线体: {len(line_quotations)} + 子报价单: {len(created_children)}')

# ============== 6. 给所有报价单加数据 ==============
all_qs = created_singles + line_quotations + created_children
print(f'\n🔧 为 {len(all_qs)} 个报价单加数据...', flush=True)

total_modules = 0
total_module_materials = 0
total_labor = 0
total_travel_trips = 0
total_travel_days = 0
total_packing = 0
total_participants = 0

for q in all_qs:
    # 6.1 模块 2-3 个
    n_modules = random.randint(2, 3)
    for k in range(n_modules):
        module = Module(
            quotation_id=q.id,
            name=f'{random.choice(modules_pool)}{k+1:02d}',
            code=f'M{q.id:03d}{k+1:02d}',
            description=f'模块{k+1}：{q.name} 的关键工序',
        )
        session.add(module)
        session.flush()
        total_modules += 1

        # 6.2 物料 5-8 个
        n_mats = random.randint(5, 8)
        sample_mats = random.sample(materials, min(n_mats, len(materials)))
        for mat in sample_mats:
            mm = ModuleMaterial(
                module_id=module.id,
                material_id=mat.id,
                is_other=False,
                quantity=random.randint(1, 10),
                selected_by_id=admin.id,
            )
            session.add(mm)
            total_module_materials += 1

    # 6.3 工时 2-3 个
    n_labor = random.randint(2, 3)
    for k in range(n_labor):
        hours = round(random.uniform(20, 200), 1)
        unit_price = round(random.uniform(300, 800), 2)
        lh = LaborHour(
            quotation_id=q.id,
            name=f'{random.choice(labor_names)}{k+1:02d}',
            hours=hours,
            unit_price=unit_price,
            total=round(hours * unit_price, 2),
            created_by=admin.id,
        )
        session.add(lh)
        total_labor += 1

    # 6.4 差旅人次 1-2
    n_trips = random.randint(1, 2)
    sample_fees = random.sample(travel_person_fees, min(n_trips, len(travel_person_fees)))
    for fee in sample_fees:
        person_count = random.randint(1, 4)
        trip = TravelPersonTrip(
            quotation_id=q.id,
            travel_category_id=fee.travel_category_id,
            travel_mode_id=fee.travel_mode_id,
            person_count=person_count,
            unit_price=float(fee.unit_price),
            visa_fee=float(fee.visa_fee) if fee.visa_fee else 0,
            remark='自动生成',
        )
        session.add(trip)
        total_travel_trips += 1

    # 6.5 差旅人天 1-2
    n_days = random.randint(1, 2)
    sample_rates = random.sample(day_rate_list, min(n_days, len(day_rate_list)))
    for rate in sample_rates:
        person_days = round(random.uniform(5, 30), 1)
        tpd = TravelPersonDays(
            quotation_id=q.id,
            travel_category_id=rate['travel_category_id'],
            person_days=person_days,
            unit_price=float(rate['unit_price']),
            remark='自动生成',
        )
        session.add(tpd)
        total_travel_days += 1

    # 6.6 包装 0-1
    if packing_types and random.random() < 0.7:
        pt = random.choice(packing_types)
        pe = PackingEntry(
            quotation_id=q.id,
            packing_type_id=pt.id,
            quantity=random.randint(1, 10),
            unit_price=float(pt.unit_price) if pt.unit_price else None,
            remark='自动生成',
        )
        session.add(pe)
        total_packing += 1

    # 6.7 参与人 admin + 1-2
    participants = [admin.id]
    if users:
        participants.extend(random.sample([u.id for u in users], min(2, len(users))))
    for uid in participants:
        ptype = 'project' if uid == admin.id else random.choice(['project', 'agency', 'electrical'])
        qp = QuotationParticipant(
            quotation_id=q.id,
            user_id=uid,
            participant_type=ptype,
        )
        session.add(qp)
        total_participants += 1

session.commit()
print(f'   ✅ 模块: {total_modules}')
print(f'   ✅ 物料关联: {total_module_materials}')
print(f'   ✅ 工时: {total_labor}')
print(f'   ✅ 差旅人次: {total_travel_trips}')
print(f'   ✅ 差旅人天: {total_travel_days}')
print(f'   ✅ 包装: {total_packing}')
print(f'   ✅ 参与人: {total_participants}')

# ============== 7. 验证 ==============
print('\n📊 最终统计:')
total_q = session.execute(text('SELECT count(*) FROM quotations')).scalar()
total_singles = session.execute(text("SELECT count(*) FROM quotations WHERE type='single' AND parent_id IS NULL")).scalar()
total_lines = session.execute(text("SELECT count(*) FROM quotations WHERE type='line'")).scalar()
total_children = session.execute(text('SELECT count(*) FROM quotations WHERE parent_id IS NOT NULL')).scalar()
print(f'   报价单总数: {total_q}')
print(f'   单机(无父): {total_singles}')
print(f'   线体: {total_lines}')
print(f'   子报价单: {total_children}')
print('   状态分布:')
for status, count in session.execute(text('SELECT status, count(*) FROM quotations GROUP BY status')).all():
    print(f'     {status}: {count}')

session.close()
print('\n✅ 完成！')
