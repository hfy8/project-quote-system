# 数据库初始化数据

## 文件说明

- **quotation_db_data.sql** — 从生产环境导出的纯数据 SQL（pg_dump --data-only）

## 覆盖范围

- 32 张业务表的数据
- 不包含 schema（表结构），需要先跑 `backend_fastapi/migrations/` 下的迁移建表
- 不包含 owner/privileges

## 用途

1. 新环境初始化（schema 建好后灌种子数据）
2. 跨环境数据迁移（开发 → 测试 → 生产）
3. 灾难恢复

## 重建步骤

```bash
# 1. 建库（如未建）
psql -U postgres -c "CREATE DATABASE quotation_db;"

# 2. 跑 migration 建表
for f in backend_fastapi/migrations/*.sql; do
    psql -U postgres -d quotation_db -f "$f"
done

# 3. 灌种子数据
psql -U postgres -d quotation_db -f database/quotation_db_data.sql

# 4. 创建管理员用户（不在 dump 里，需要手动跑）
docker exec <backend-container> python -c "
from db import db
from core.models.user import User, Role
admin = User(username='admin', email='admin@example.com', is_active=True)
admin.set_password('admin123')
db.session.add(admin)
db.session.commit()
"

# 5. 灌权限和参与人类型
docker exec <backend-container> python -c "
from utils.permissions import seed_permissions_and_roles
from core.models.participant_type_permission import seed_participant_type_tabs
seed_permissions_and_roles()
seed_participant_type_tabs()
"
```

## 数据规模（2026-07-13）

| 表 | 行数 |
|---|---|
| materials | 492 |
| users | 285 |
| employees | 284 |
| positions | 234 |
| operation_logs | 201 |
| exchange_rates | 166 |
| module_materials | 140 |
| departments | 140 |
| permissions | 45 |
| landing_projects | 41 |
| role_permissions | 29 |
| participant_type_permissions | 29 |
| packing_types | 8 |
| travel_person_trip_fees | 6 |
| 其他 20 张 | 少量配置数据 |

## 注意事项

- SQL Server 同步数据（users/employees/positions/departments）来自 `192.168.100.70:1433`，如网络不通需要单独跑 `core/tasks/sync_task.py:trigger_sync_now()`
- 汇率来自 `https://open.er-api.com/v6/latest/CNY`，同样可以单独同步
- 文件包含 `\restrict` 指令（PostgreSQL 16+），导入时如遇版本问题可手动去掉