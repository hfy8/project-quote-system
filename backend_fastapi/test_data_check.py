"""检查实际数据 + contains 问题"""
import sys
sys.path.insert(0, ".")

from db import db_session_factory
from core.models.material import Material
from core.models.module import Module
from core.models.material import ModuleMaterial
from sqlalchemy import text

session = db_session_factory()
try:
    print("=== 物料 ===")
    for m in session.query(Material).limit(5).all():
        print(f"  #{m.id} {m.name} | {m.spec}")
    print(f"  总数: {session.query(Material).count()}")
    
    print("\n=== 模块 ===")
    for m in session.query(Module).limit(10).all():
        print(f"  #{m.id} qid={m.quotation_id} {m.name} | {m.code}")
    print(f"  总数: {session.query(Module).count()}")
    
    print("\n=== 模块物料 ===")
    count = session.query(ModuleMaterial).count()
    print(f"  总数: {count}")
    for mm in session.query(ModuleMaterial).limit(5).all():
        print(f"  #{mm.id} module_id={mm.module_id} material_id={mm.material_id} qty={mm.quantity}")
    
    print("\n=== SQL LIKE 验证 ===")
    for kw in ['酒精', '螺丝', '铝', '散热', '机柜']:
        r = session.execute(text("SELECT count(*) FROM materials WHERE name LIKE :kw"), {"kw": f"%{kw}%"}).scalar()
        print(f"  materials LIKE '%{kw}%': {r}")
    
    print("\n=== modules LIKE ===")
    for kw in ['散热', '机柜', '主体', '外壳', '工位']:
        r = session.execute(text("SELECT count(*) FROM modules WHERE name LIKE :kw"), {"kw": f"%{kw}%"}).scalar()
        print(f"  modules LIKE '%{kw}%': {r}")
finally:
    session.close()
