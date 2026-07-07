"""2026-07-07: B6 + B7 数据清理
- B6: travel_categories 清测试脏数据 (id=5/10/11) + 合并 cat=17 (国内出差) 到 cat=1
- B7: travel_modes 清测试脏数据 (id=8/10/11)

执行: docker exec backend python3 /tmp/2026_07_07_B6_B7_clean_travel_data.py
验证: SELECT count(*) FROM travel_categories  # 应为 9
     SELECT count(*) FROM travel_modes       # 应为 5
"""
import sys
sys.path.insert(0, '/app')
from db import db
session = db.session
from sqlalchemy import text

# B6 day_rate/fee 合并
session.execute(text("UPDATE travel_day_rates SET unit_price=200.00, is_active=True WHERE id=1"))
session.execute(text("DELETE FROM travel_day_rates WHERE id=11"))
session.execute(text("UPDATE travel_person_trip_fees SET unit_price=800.00, is_active=True WHERE id=1"))
session.execute(text("DELETE FROM travel_person_trip_fees WHERE id=15"))
session.execute(text("UPDATE travel_person_trips SET travel_category_id=1 WHERE travel_category_id=17"))
session.execute(text("UPDATE travel_person_days SET travel_category_id=1 WHERE travel_category_id=17"))
session.execute(text("UPDATE travel_categories SET is_active=True WHERE id=1"))
session.execute(text("DELETE FROM travel_categories WHERE id=17"))
for tid in [5, 10, 11]:
    session.execute(text(f"DELETE FROM travel_categories WHERE id={tid}"))

# B7 mode 清脏
for tid in [8, 10, 11]:
    session.execute(text(f"DELETE FROM travel_modes WHERE id={tid}"))

session.commit()
print("B6+B7 cleanup committed")
