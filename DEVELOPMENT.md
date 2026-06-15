# 项目报价系统 — 开发与使用文档

> 版本：V2.2（2026-06-12） · v17（彻底移除 Flask）  
> 仓库：https://github.com/hfy8/project-quote-system  
> 技术栈：Vue 3 + **FastAPI** + PostgreSQL（SQLAlchemy 2.x，无 Flask）

本文档面向三类读者：
- **开发者**（加入项目、写新功能、调试问题）→ 看第一、二章
- **运维**（部署、迁移、监控）→ 看第三章
- **最终用户**（报价人员、商务、管理员）→ 看第四章使用手册

---

## 目录

1. [开发环境搭建](#1-开发环境搭建)
2. [项目结构与代码规范](#2-项目结构与代码规范)
3. [部署与运维](#3-部署与运维)
4. [使用手册（面向用户）](#4-使用手册面向用户)
5. [完整 API 索引（131 个端点）](#5-完整-api-索引131-个端点)
6. [数据库表结构](#6-数据库表结构)
7. [V2.1 新功能详解](#7-v21-新功能详解)
8. [业务规则与公式](#8-业务规则与公式)
9. [已知陷阱与解决方案](#9-已知陷阱与解决方案)
10. [附录](#10-附录)

---

## 1. 开发环境搭建

### 1.1 环境要求

| 软件 | 版本 | 说明 |
|------|------|------|
| Node.js | ≥ 18 | 前端构建（Vite 7） |
| pnpm 或 npm | pnpm 8 推荐 | 前端包管理 |
| Python | ≥ 3.12 | 后端（用到 `int \| None` 类型注解） |
| PostgreSQL | ≥ 14 | 主数据库 |
| SQL Server | 2016+ | 可选，员工/部门/职位同步源 |
| Git | 任意 | |

### 1.2 克隆与初始化

```bash
git clone https://github.com/hfy8/project-quote-system.git
cd project-quote-system
```

### 1.3 后端启动

```bash
cd backend_fastapi

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate     # Linux/WSL
# venv\Scripts\activate      # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（复制 .env.example 改）
cp .env.example .env
# 编辑 .env，填入 DATABASE_URL 等
```

`.env` 必须项：

```bash
DATABASE_URL=postgresql://quote_user:***@localhost:5432/quote_db
SECRET_KEY=your-secret-key-change-me
JWT_SECRET_KEY=jwt-secret-change-me

# 可选：SQL Server 同步源（员工/部门/职位）
SQL_SERVER_HOST=192.168.100.70
SQL_SERVER_PORT=1433
SQL_SERVER_DB=RSHRIS
SQL_SERVER_USER=sa
SQL_SERVER_PASSWORD=***
```

初始化数据库（建表 + seed 角色 + 默认账号）：

```bash
python init_db.py
```

启动后端（**不要加 `--reload`** —— 见第 9 章 ASGI reload 陷阱）：

```bash
python -m uvicorn main:fastapi_app --host=0.0.0.0 --port=5001
# 或：python main.py
```

后端跑在 **http://localhost:5001**

### 1.4 前端启动

```bash
cd frontend
npm install          # 或 pnpm install
npm run dev
```

前端跑在 **http://localhost:3000**

### 1.5 默认账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| `admin` | `admin123` | 超级管理员（全部权限）|

### 1.6 健康检查

```bash
# 后端
curl http://localhost:5001/api/auth/me
# 前端
curl -I http://localhost:3000/
```

### 1.7 WSL 环境特别注意

用户在 WSL 下开发，常见坑：

- **服务挂掉不自启**：每次改完代码后用下面脚本检查并重启
  ```bash
  bash scripts/check-services.sh
  ```
- **前端 vite 装不上**：`npm install --include=dev`（不是 `--omit=dev`）
- **后端修改必须重启** uvicorn 进程（无 debug auto-reload），前端 Vite 有 HMR 但要看网络代理是否拦截

### 1.8 项目里的脚本

`scripts/` 目录下：
- `check-services.sh` — 检查并重启前后端服务

---

## 2. 项目结构与代码规范

### 2.1 顶层目录

```
project-quote-system/
├── backend_fastapi/        # FastAPI 后端（v17 彻底无 Flask）
├── frontend/               # Vue3 前端
├── docs/                   # 临时文档
├── scripts/                # 运维脚本
├── screenshots/            # 截图
├── README.md               # 快速索引
├── SPEC.md                 # 产品技术规格（归档）
├── 使用说明书.md              # 旧版用户使用手册（归档）
└── DEVELOPMENT.md          # 本文件（开发 + 使用文档，V2.1 之后唯一权威）
```

### 2.2 后端结构

```
backend_fastapi/
├── main.py                 # FastAPI 入口（uvicorn 加载 fastapi_app）
├── db.py                   # 纯 SQLAlchemy 2.x 启动 + _DBProxy 代理
├── requirements.txt        # 无 flask / flask-* / a2wsgi
│
├── api/                    # 19 个 FastAPI 路由
│   ├── __init__.py
│   ├── auth.py / users.py / roles.py
│   ├── quotations.py / versions.py / exports.py
│   ├── modules.py / materials.py / module_participants.py
│   ├── fees.py / fee_rates.py / labor_hours.py
│   ├── travel_entries.py / travel_fees.py
│   ├── exchange_rates.py / messages.py / logs.py
│   ├── participant_type_permissions.py
│   └── change_requests.py / sync.py
│
├── core/                   # 核心业务包
│   ├── __init__.py         # 触发 models 注册
│   ├── config.py           # 数据库连接配置
│   ├── schemas.py          # Pydantic 数据模型
│   ├── models/             # 21 个 SQLAlchemy 2.x 模型
│   │   ├── user.py / role.py / permission.py
│   │   ├── quotation.py / material.py / module.py
│   │   ├── fee.py / fee_rate.py / labor_hour.py
│   │   ├── travel.py / travel_entry.py / packing.py
│   │   ├── version.py / change_request.py
│   │   ├── message.py / operation_log.py / exchange_rate.py
│   │   ├── organization.py / department.py
│   │   ├── position.py / employee.py
│   │   └── participant_type_permission.py
│   ├── services/           # 业务服务层
│   │   ├── export_service.py  # PDF/Word 生成（v17 已验证 19805 bytes 一致性）
│   │   └── message_service.py
│   └── tasks/              # APScheduler 定时任务（无 Flask app 参数）
│       └── sync_task.py
│
├── utils/                  # 工具
│   ├── permissions.py      # 权限检查 + seed（无 flask_jwt_extended）
│   └── logger.py           # 操作日志（threading.local 替代 flask.request）
│
├── fonts/                  # 中文字体（PDF 用）
├── static/versions/        # 归档 PDF/Word 存储（不入 git）
├── init_db.py              # 建表 + seed
├── migrate_coeff.py        # 系数数据迁移脚本
└── Dockerfile
```

### 2.3 前端结构

```
frontend/
├── src/
│   ├── api/                   # 18 个 API 模块（按后端路由 1:1）
│   │   ├── request.js         # axios + 拦截器 + JWT
│   │   ├── auth.js / users.js / roles.js
│   │   ├── quotations.js / versions.js
│   │   ├── modules.js / materials.js
│   │   ├── fees.js / fee_rates.js / labor_hours.js
│   │   ├── travel_entries.js / travel_fees.js
│   │   ├── exchange_rates.js / logs.js / messages.js
│   │   ├── module_participants.js
│   │   └── changeRequests.js
│   ├── views/                 # 22 个页面（单文件组件）
│   │   ├── Login.vue
│   │   ├── Dashboard.vue
│   │   ├── Quotations.vue / QuotationEdit.vue / QuotationView.vue
│   │   ├── VersionCompare.vue
│   │   ├── Materials.vue / Fees.vue / FeeTypes.vue / FeeRatesConfig.vue
│   │   ├── ExchangeRatesConfig.vue / TravelFeeConfig.vue
│   │   ├── Users.vue / Roles.vue / PermissionsTable.vue
│   │   ├── ParticipantTypePermissions.vue / ModuleAssignments.vue
│   │   ├── ChangeRequests.vue / Logs.vue / Messages.vue
│   │   └── SystemSettings.vue
│   ├── components/            # 复用组件
│   ├── stores/                # Pinia stores
│   │   └── auth.js            # authStore：login/logout/getUserInfo/clearAuth
│   ├── router/index.js
│   ├── assets/
│   └── main.js
├── index.html
├── vite.config.js             # Vite 配置（含代理 /api → :5001）
├── package.json
└── pnpm-workspace.yaml
```

### 2.4 代码规范

#### 后端
- **Python 3.12** 类型注解必填：`def foo(x: int) -> dict[str, Any]:`
- FastAPI 路由：`router = APIRouter(prefix='/api/<domain>')`
- 依赖注入用 `Depends(get_db)` / `Depends(get_current_user_id)`
- 错误响应统一 `HTTPException(status_code=..., detail="...")`
- 业务异常抛 `HTTPException`，由全局 exception_handler 统一返回
- 业务事务：`db.session.add() → db.session.commit()`，失败 `db.session.rollback()`

#### 前端
- Vue 3 **Composition API + `<script setup>`**
- 所有 API 调用走 `frontend/src/api/*.js` 模块，**禁止组件内直接 axios**
- `<style scoped>` 隔离，主色 `#0D9488`
- CSS 变量统一在 `:root` 定义：`--color-primary`、`--spacing-md`、`--radius-md`、`--shadow-sm` 等
- 数字保留两位：`value.toFixed(2)`；金额展示前加 `¥` 或 `${currency}`

### 2.5 开发流程（贡献代码）

```bash
# 1. 拉最新代码
git pull origin master

# 2. 建分支（命名：feat/xxx、fix/xxx、refactor/xxx）
git checkout -b feat/new-export-format

# 3. 写代码 → 自测 → 跑 linter
cd frontend && npm run lint
cd backend_fastapi && python -m py_compile api/ core/ utils/

# 4. 提交（commit 信息格式 feat:/fix:/docs:/refactor: 描述）
git commit -m "feat: 增加 Excel 多 sheet 导出"

# 5. 推 + 建 PR
git push origin feat/new-export-format
gh pr create --title "feat: Excel 多 sheet 导出" --body "..."
```

### 2.6 服务健康自检脚本

```bash
#!/bin/bash
# scripts/check-services.sh
ps aux | grep -E "uvicorn|npm|vite" | grep -v grep
if ! pgrep -f "uvicorn" > /dev/null; then
  echo "⚠️  Uvicorn 已挂，重启中..."
  cd backend_fastapi && nohup python -m uvicorn main:fastapi_app --host=0.0.0.0 --port=5001 > /tmp/fastapi.log 2>&1 &
fi
if ! pgrep -f "vite" > /dev/null; then
  echo "⚠️  Vite 已挂，重启中..."
  cd frontend && nohup npm run dev > /tmp/vite.log 2>&1 &
fi
```

### 2.7 文档知识库（额外资源）

项目根目录外还有一个用 Karpathy LLM Wiki 模式构建的知识库：

```
~/wiki/                       # /home/rs8568/wiki/
├── SCHEMA.md                 # 规范
├── index.md                  # 总目录
├── log.md                    # 行动日志
├── entities/  (9 页)         # 数据库模型
├── concepts/  (9 页)         # 业务概念、流程、陷阱
├── api/       (6 页)         # REST API 按域分组
└── schema/    (1 页)         # 数据库 ER 总览
```

Obsidian 直接打开 `~/wiki/` 即可浏览，[[wikilinks]] 自动识别。

---

## 3. 部署与运维

### 3.1 生产环境部署（Docker）

```bash
# 后端
cd backend_fastapi
docker build -t quote-backend:latest .
docker run -d --name quote-backend \
  -p 5001:5001 \
  -e DATABASE_URL=postgresql://... \
  -e SECRET_KEY=... \
  -v /var/quote-static:/app/static/versions \
  quote-backend:latest

# 前端构建静态文件
cd frontend
npm install && npm run build
# dist/ 目录用 Nginx 服务
```

### 3.2 Nginx 反向代理

```nginx
server {
  listen 80;
  server_name quote.example.com;

  # 前端静态文件
  root /var/quote-frontend/dist;
  index index.html;

  # API 反代
  location /api/ {
    proxy_pass http://127.0.0.1:5001;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    client_max_body_size 20M;
  }

  # SPA 路由 fallback
  location / {
    try_files $uri $uri/ /index.html;
  }
}
```

### 3.3 数据库迁移

```bash
# 导出当前 schema
pg_dump -U postgres quote_db > backup_$(date +%Y%m%d).sql

# 增量迁移（手写 SQL）
psql -U postgres quote_db < migrations/2026_06_10_add_cascade.sql

# 重新 seed
python init_db.py --reset-roles
```

### 3.4 定时任务

| 任务 | 周期 | 说明 |
|------|------|------|
| 消息清理 | 每天 03:00 | 清理已读 30 天/未读 60 天的消息 |
| 数据同步 | 每天 22:00 | 从 SQL Server 同步员工/部门/职位 |

在 `core/tasks/` 下注册，scheduler 在 `main.py` lifespan 启动。

### 3.5 日志位置

- Uvicorn / FastAPI：`/tmp/fastapi.log`（开发）或 stdout（生产）
- Vite：`/tmp/vite.log`（开发）
- 归档 PDF：`backend_fastapi/static/versions/`（**git 忽略**）

### 3.6 备份策略

- 数据库：每天 `pg_dump` 到备份盘，保留 30 天
- 归档 PDF：跟随数据库备份，每周一次
- SQL Server 同步源：本系统只读，不需要备份

---

## 4. 使用手册（面向用户）

### 4.1 系统概览

项目报价系统用于非标设备的报价全流程管理：
- 创建报价单 → 添加模块 → 选物料 → 加费用 → 算汇总 → 归档出 PDF

**三类用户角色**：
- **业务/销售**（admin）：报价、归档、查看全部数据
- **技术工程师**：被指派模块任务，添加物料/工时
- **管理员**：用户/角色/权限、系统配置

### 4.2 报价单状态机

```
[草稿 draft] ──归档──> [已归档 approved]
   ↑                      │
   └────── 撤销归档 ───────┘
                            │
                            └── 修改走 ChangeRequest 审核
```

### 4.3 单机报价流程（典型场景）

#### 步骤 1：登录
访问 http://localhost:3000/login  
输入 `admin` / `admin123`

#### 步骤 2：创建报价单
1. 左侧导航 → **📋 报价单管理** → 右上 **+ 新建**
2. 填基本信息：
   - 名称（如「厦门某某公司 XX 设备」）
   - 类型：**单机**
   - 方案编号（可选）
   - 税率（默认 13%）
   - 对外利润率（默认 0）
   - 币种（默认 CNY）
3. 点 **创建**

#### 步骤 3：配置费用系数
在 **费用系数 tab** 设置：
- 大件系数（如 1.3）
- 普通件系数（如 1.2）
- 其他件系数（如 1.1）

> 系数影响汇总的「物料合计（含系数）」

#### 步骤 4：添加模块
1. 切到 **模块管理 tab**
2. 点 **+ 添加模块**，输入模块名（如「数控模块」）
3. 重复添加多个模块

#### 步骤 5：物料清单
1. 切到 **物料清单 tab**
2. 每个模块旁边点 **+ 添加物料**
3. 弹窗里：
   - 左侧选物料分类（大件/普通件/其他件）筛选
   - 选具体物料 → 填数量 → 点 **添加到模块**
4. 关键参数 01/02/03 显示物料额外属性（机构/电控选料参考）

#### 步骤 6：添加费用
切到 **费用 tab**：
1. 选费用类型（如「认证费」）
2. 位置（厂内/厂外）
3. 填金额
4. 可选挂到具体模块（不挂表示整单费用）

#### 步骤 7：人力工时
切到 **人力工时 tab**：
1. 输入工时项名（如「电气调试」）
2. 填工时数 × 单价 → 自动算 total

#### 步骤 8：（可选）运输 + 差旅
- **运输包装 tab**：选包装类型 → 填数量 → 单价自动带出
- **差旅人天 tab**：选目的地 → 填人天数 → 单价自动带出
- **差旅人次 tab**：选目的地 + 交通方式 → 填人次 → 含签证费

#### 步骤 9：查看汇总
切到 **汇总 tab**：
- **上方**：物料合计 / 物料合计（含系数）/ 小计 / 含利润小计 / 最终报价
- **占比分析**：硬件 / 人力 / 差旅 / 利润 / 税 五张卡片 + 堆叠条
- **硬件成本结构**：大件/普通件/其他件 三档分类
- **模块汇总**：每个模块的物料数和金额
- **费用明细**：合并所有费用
- **货币切换**：右上角下拉切 CNY/USD/EUR/SGD

可以点 **🖼️ 导出汇总 PDF（按网页）**：生成与网页一模一样的 PDF 截图（5mm 边距）。

#### 步骤 10：导出 PDF
切到 **导出 tab**：
- **导出 PDF**：中英双语，自动三 section 合并
- **导出 Word**：可二次编辑
- **导出 Excel**：财务对账用

#### 步骤 11：归档
回到报价单列表，点报价单 → 右上 **📥 归档**：
- 系统自动：
  1. 拍快照（含 modules/fees/labor/packing/travel/coefficients）
  2. 生成中英两份 PDF
  3. 生成 Word 文件
  4. 状态改为 `approved`
  5. current_version +1

已归档后任何修改必须走 **变更审核** 流程。

#### 步骤 12：版本对比
1. 列表报价单 → 右上 **🔀 版本对比**
2. 选两个版本（v1、v2、v3...）
3. 逐项对比：物料差异 / 费用差异 / 人力工时差异 / 差旅差异
4. 物料差异用 MM ID 作 key，同物料在不同模块下不合并

### 4.4 线体报价单（Line Body）

适用于多工位复杂设备：
1. 创建时类型选 **线体**
2. 编辑页加 **子报价单** tab（在模块管理附近）
3. 给线体添加子报价单（如「工位01」、「工位02」）
4. 物料清单 tab 显示**所有子报价单模块**，每个模块头部带归属 tag
5. 汇总 tab：**聚合所有子报价单**
6. PDF：**只展示汇总数字**，不展示单机明细

**重要规则**：
- 子报价单**禁止独立归档**
- 父线体归档 → 自动归档所有子
- 父线体有 children 时**禁止删除**

### 4.5 变更审核（已归档后修改）

1. 已归档报价单所有修改字段都会被禁用
2. 改数据时弹窗提示：「已归档，请提交变更审核」
3. 提交后系统发消息给原业务员
4. 业务员在 **📤 变更审核** 页面批准/拒绝
5. 批准后变更自动应用，报价单维持已归档状态
6. 如需新版本，批准前选择「生成新版本」选项

### 4.6 个人任务

- **📌 我的分配**：列出我作为参与人的报价单
- 进入查看模式（只读 + 部分 tab）
- 我被指派的模块任务高亮显示

### 4.7 消息中心

- 顶部铃铛显示未读数
- 点击看所有消息
- 消息类型：
  - `module_member_added` — 被加入模块
  - `change_request_submitted` — 提交了变更申请
  - `change_request_approved` — 变更被批准
  - `change_request_rejected` — 变更被拒绝
  - `version_updated` — 版本更新

### 4.8 系统管理（仅管理员）

- **👤 用户管理**：CRUD 用户、重置密码
- **👥 角色管理**：CRUD 角色、勾选权限码
- **🔐 参与人权限**：按参与类型（项目/机构/电控）分配 tab 可见性
- **🚚 运输差旅配置**：packing_types / travel_categories / travel_modes 等字典
- **💱 汇率配置**：多币种 + 设置基础币种
- **📊 费用系数**：全局大件/普通件/其他件系数默认值
- **📝 操作日志**：审计所有用户操作

---

## 5. 完整 API 索引（131 个端点）

> 所有端点前缀 `/api`，鉴权方式：除 `/api/auth/login` 外全部需要 `Authorization: Bearer *** 格式端点 = `/api/<blueprint>/<path>`。

### 5.1 通用约定

| 项 | 说明 |
|-----|------|
| 鉴权头 | `Authorization: Bearer <access_token>` |
| Content-Type | `application/json`（除 GET 下载） |
| 业务响应 | `{ "code": 0, "data": ... }` 或直接对象 |
| 错误响应 | `{ "error": "错误描述", "code": "可选业务码" }` |
| 列表分页 | 部分端点支持 `?page=1&per_page=20` |

### 5.2 API 分组

##### 5.2 API 分组明细

每个 blueprint 一个分组，路径前缀 `/api/<blueprint>`。


#### `auth`（4 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| POST   | `/api/auth/change-password` | `change_password` |
| POST   | `/api/auth/login` | `login` |
| POST   | `/api/auth/logout` | `logout` |
| GET    | `/api/auth/me` | `get_current_user` |


#### `change-requests`（3 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| POST   | `/api/change-requests/<int:request_id>/approve` | `approve_change_request` |
| POST   | `/api/change-requests/<int:request_id>/reject` | `reject_change_request` |
| GET    | `/api/change-requests/pending` | `get_pending_requests` |


#### `exchange_rates`（5 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| PUT    | `/api/exchange_rates/<int:rate_id>` | `update_exchange_rate` |
| DELETE | `/api/exchange_rates/<int:rate_id>` | `delete_exchange_rate` |
| POST   | `/api/exchange_rates/<int:rate_id>/set-base` | `set_base_currency` |
| GET    | `/api/exchange_rates/base` | `get_base_currency` |
| GET    | `/api/exchange_rates/convert` | `convert_currency` |


#### `fee-types`（4 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| GET    | `/api/fee-types` | `get_fee_types` |
| POST   | `/api/fee-types` | `create_fee_type` |
| PUT    | `/api/fee-types/<int:fee_type_id>` | `update_fee_type` |
| DELETE | `/api/fee-types/<int:fee_type_id>` | `delete_fee_type` |


#### `fee_rates`（3 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| PUT    | `/api/fee_rates/<int:rate_id>` | `update_fee_rate` |
| DELETE | `/api/fee_rates/<int:rate_id>` | `delete_fee_rate` |
| GET    | `/api/fee_rates/category/<string:category>` | `get_fee_rate_by_category` |


#### `fees`（2 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| PUT    | `/api/fees/<int:fee_id>` | `update_fee` |
| DELETE | `/api/fees/<int:fee_id>` | `delete_fee` |


#### `logs`（2 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| GET    | `/api/logs/actions` | `get_log_actions` |
| GET    | `/api/logs/modules` | `get_log_modules` |


#### `materials`（4 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| PUT    | `/api/materials/<int:material_id>` | `update_material` |
| DELETE | `/api/materials/<int:material_id>` | `delete_material` |
| PUT    | `/api/materials/<int:material_id>/toggle` | `toggle_material` |
| POST   | `/api/materials/import` | `import_materials` |


#### `messages`（4 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| PUT    | `/api/messages/<int:message_id>/read` | `mark_as_read` |
| POST   | `/api/messages/cleanup` | `cleanup_old_messages` |
| PUT    | `/api/messages/read-all` | `mark_all_as_read` |
| GET    | `/api/messages/unread-count` | `get_unread_count` |


#### `module_materials`（2 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| PUT    | `/api/module_materials/<int:id>` | `update_module_material` |
| DELETE | `/api/module_materials/<int:id>` | `remove_module_material` |


#### `modules`（9 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| GET    | `/api/modules/<int:module_id>` | `get_module` |
| PUT    | `/api/modules/<int:module_id>` | `update_module` |
| DELETE | `/api/modules/<int:module_id>` | `delete_module` |
| GET    | `/api/modules/<int:module_id>/materials` | `get_module_materials` |
| POST   | `/api/modules/<int:module_id>/materials` | `add_material_to_module` |
| GET    | `/api/modules/<int:module_id>/participants` | `get_module_participants` |
| POST   | `/api/modules/<int:module_id>/participants` | `add_module_participants` |
| DELETE | `/api/modules/<int:module_id>/participants/<int:participant_id>` | `remove_module_participant` |
| GET    | `/api/modules/<int:module_id>/summary` | `get_module_summary` |


#### `packing-entries`（4 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| GET    | `/api/packing-entries` | `get_packing_entries` |
| POST   | `/api/packing-entries` | `upsert_packing_entry` |
| PUT    | `/api/packing-entries/<int:eid>` | `update_packing_entry` |
| DELETE | `/api/packing-entries/<int:eid>` | `delete_packing_entry` |


#### `packing-types`（4 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| GET    | `/api/packing-types` | `get_packing_types` |
| POST   | `/api/packing-types` | `create_packing_type` |
| PUT    | `/api/packing-types/<int:tid>` | `update_packing_type` |
| DELETE | `/api/packing-types/<int:tid>` | `delete_packing_type` |


#### `participant-type-permissions`（8 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| PUT    | `/api/participant-type-permissions/<int:id>` | `update` |
| DELETE | `/api/participant-type-permissions/<int:id>` | `delete` |
| PUT    | `/api/participant-type-permissions/batch` | `batch_update` |
| GET    | `/api/participant-type-permissions/by-type/<ptype>` | `get_by_type` |
| POST   | `/api/participant-type-permissions/initialize` | `initialize` |
| GET    | `/api/participant-type-permissions/tabs/<ptype>` | `get_tabs_by_type` |
| POST   | `/api/participant-type-permissions/types` | `create_type` |
| DELETE | `/api/participant-type-permissions/types/<ptype>` | `delete_type` |


#### `quotations`（35 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| GET    | `/api/quotations/<int:quotation_id>/all-modules` | `get_all_modules` |
| POST   | `/api/quotations/<int:quotation_id>/archive` | `archive_quotation` |
| POST   | `/api/quotations/<int:quotation_id>/copy` | `copy_quotation` |
| GET    | `/api/quotations/<int:quotation_id>/export/excel` | `export_excel` |
| GET    | `/api/quotations/<int:quotation_id>/export/pdf` | `export_pdf` |
| GET    | `/api/quotations/<int:quotation_id>/export/word` | `export_word` |
| GET    | `/api/quotations/<int:quotation_id>/fees` | `get_fees` |
| POST   | `/api/quotations/<int:quotation_id>/fees` | `create_fee` |
| GET    | `/api/quotations/<int:quotation_id>/labor-hours` | `get_labor_hours` |
| POST   | `/api/quotations/<int:quotation_id>/labor-hours` | `create_labor_hour` |
| PUT    | `/api/quotations/<int:quotation_id>/labor-hours/<int:item_id>` | `update_labor_hour` |
| DELETE | `/api/quotations/<int:quotation_id>/labor-hours/<int:item_id>` | `delete_labor_hour` |
| GET    | `/api/quotations/<int:quotation_id>/modules` | `get_modules` |
| POST   | `/api/quotations/<int:quotation_id>/modules` | `create_module` |
| GET    | `/api/quotations/<int:quotation_id>/participants` | `get_participants` |
| POST   | `/api/quotations/<int:quotation_id>/participants` | `add_participant` |
| PUT    | `/api/quotations/<int:quotation_id>/participants/<int:user_id>` | `update_participant_type` |
| DELETE | `/api/quotations/<int:quotation_id>/participants/<int:user_id>` | `remove_participant` |
| PUT    | `/api/quotations/<int:quotation_id>/status` | `update_status` |
| GET    | `/api/quotations/<int:quotation_id>/summary` | `get_quotation_summary` |
| POST   | `/api/quotations/<int:quotation_id>/unarchive` | `unarchive_quotation` |
| GET    | `/api/quotations/<int:quotation_id>/versions` | `get_versions` |
| GET    | `/api/quotations/<int:quotation_id>/versions` | `get_versions` |
| POST   | `/api/quotations/<int:quotation_id>/versions` | `create_version` |
| GET    | `/api/quotations/<int:quotation_id>/versions/<int:version_no>` | `get_version_detail` |
| GET    | `/api/quotations/<int:quotation_id>/versions/<int:version_no>/export/excel` | `export_version_excel` |
| GET    | `/api/quotations/<int:quotation_id>/versions/<int:version_no>/export/pdf` | `export_version_pdf` |
| GET    | `/api/quotations/<int:quotation_id>/versions/<int:version_no>/export/word` | `export_version_word` |
| GET    | `/api/quotations/<int:quotation_id>/versions/compare` | `compare_versions_by_quotaion` |
| GET    | `/api/quotations/<quotation_id>` | `get_quotation` |
| PUT    | `/api/quotations/<quotation_id>` | `update_quotation` |
| DELETE | `/api/quotations/<quotation_id>` | `delete_quotation` |
| GET    | `/api/quotations/<quotation_id>/permissions` | `get_quotation_permissions` |
| GET    | `/api/quotations/my-assigned-modules` | `get_my_assigned_modules` |
| GET    | `/api/quotations/my-assignments` | `get_my_assignments` |


#### `roles`（5 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| GET    | `/api/roles/<int:role_id>` | `get_role` |
| PUT    | `/api/roles/<int:role_id>` | `update_role` |
| DELETE | `/api/roles/<int:role_id>` | `delete_role` |
| GET    | `/api/roles/permissions` | `get_permissions` |
| POST   | `/api/roles/seed` | `seed` |


#### `sync`（2 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| GET    | `/api/sync/status` | `sync_status` |
| POST   | `/api/sync/trigger` | `trigger_sync` |


#### `travel-categories`（4 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| GET    | `/api/travel-categories` | `get_travel_categories` |
| POST   | `/api/travel-categories` | `create_travel_category` |
| PUT    | `/api/travel-categories/<int:tid>` | `update_travel_category` |
| DELETE | `/api/travel-categories/<int:tid>` | `delete_travel_category` |


#### `travel-day-rates`（4 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| GET    | `/api/travel-day-rates` | `get_travel_day_rates` |
| POST   | `/api/travel-day-rates` | `create_travel_day_rate` |
| PUT    | `/api/travel-day-rates/<int:rid>` | `update_travel_day_rate` |
| DELETE | `/api/travel-day-rates/<int:rid>` | `delete_travel_day_rate` |


#### `travel-modes`（4 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| GET    | `/api/travel-modes` | `get_travel_modes` |
| POST   | `/api/travel-modes` | `create_travel_mode` |
| PUT    | `/api/travel-modes/<int:tid>` | `update_travel_mode` |
| DELETE | `/api/travel-modes/<int:tid>` | `delete_travel_mode` |


#### `travel-person-days`（4 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| GET    | `/api/travel-person-days` | `get_travel_person_days` |
| POST   | `/api/travel-person-days` | `upsert_travel_person_days` |
| PUT    | `/api/travel-person-days/<int:eid>` | `update_travel_person_days` |
| DELETE | `/api/travel-person-days/<int:eid>` | `delete_travel_person_days` |


#### `travel-person-trip-fees`（4 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| GET    | `/api/travel-person-trip-fees` | `get_travel_person_trip_fees` |
| POST   | `/api/travel-person-trip-fees` | `create_travel_person_trip_fee` |
| PUT    | `/api/travel-person-trip-fees/<int:fid>` | `update_travel_person_trip_fee` |
| DELETE | `/api/travel-person-trip-fees/<int:fid>` | `delete_travel_person_trip_fee` |


#### `travel-person-trips`（4 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| GET    | `/api/travel-person-trips` | `get_travel_person_trips` |
| POST   | `/api/travel-person-trips` | `upsert_travel_person_trip` |
| PUT    | `/api/travel-person-trips/<int:tid>` | `update_travel_person_trip` |
| DELETE | `/api/travel-person-trips/<int:tid>` | `delete_travel_person_trip` |


#### `users`（4 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| PUT    | `/api/users/<int:user_id>` | `update_user` |
| DELETE | `/api/users/<int:user_id>` | `delete_user` |
| POST   | `/api/users/<int:user_id>/reset-password` | `reset_password` |
| GET    | `/api/users/roles` | `get_roles` |


#### `versions`（3 个端点）

| 方法 | 路径 | 函数 |
|------|------|------|
| GET    | `/api/versions/<int:version_id>` | `get_version` |
| GET    | `/api/versions/<int:version_id>/compare/<int:other_id>` | `compare_versions` |
| POST   | `/api/versions/<int:version_id>/rollback` | `rollback_version` |


---

## 6. 数据库表结构

> 共 30 张表：业务核心 20 张 + 系统 10 张。完整 ER 图见 `~/wiki/schema/database-overview.md`。

### 6.1 业务核心表（20 张）

| 表名 | Model | 说明 | 关键字段 |
|------|-------|------|----------|
| `quotations` | Quotation | 报价单（自引用 parent_id） | id, name, type(single/line), status(draft/approved), parent_id, business_owner_id, tax_rate, profit_rate, currency, current_version, coefficients(JSON) |
| `quotation_participants` | QuotationParticipant | 报价单参与人 | quotation_id, user_id, participant_type(project/agency/electrical) |
| `modules` | Module | 模块 | id, quotation_id, name, name_en, code, description |
| `module_participants` | ModuleParticipant | 模块参与人 | module_id, user_id |
| `materials` | Material | 原材料库 | id, name, spec, brand, unit, unit_price, category(large/standard/other), param1/2/3, status |
| `module_materials` | ModuleMaterial | 模块物料关联 | id, module_id, material_id, quantity, is_other, unit_price_override, selected_by_id |
| `other_fees` | OtherFee | 费用明细 | id, quotation_id, module_id(可空), fee_type, location(inside/outside), amount |
| `fee_types` | FeeType | 费用类型字典 | id, name, name_en, location, is_active |
| `fee_rates` | FeeRate | 费用系数（全局默认值） | id, category(large/standard/other), rate |
| `labor_hours` | LaborHour | 人力工时 | id, quotation_id, name, hours, unit_price, total, created_by |
| `packing_types` | PackingType | 运输包装类型字典 | id, name, name_en, unit_price, is_active |
| `packing_entries` | PackingEntry | 运输包装条目 | id, quotation_id, packing_type_id, quantity, unit_price, remark |
| `travel_categories` | TravelCategory | 差旅目的地字典 | id, name, code, description, sort_order, is_active |
| `travel_day_rates` | TravelDayRate | 差旅人天单价 | id, travel_category_id, unit_price, currency |
| `travel_modes` | TravelMode | 交通方式字典 | id, name, name_en, code, description |
| `travel_person_trip_fees` | TravelPersonTripFee | 差旅人次单价 | id, travel_category_id, travel_mode_id, unit_price, visa_fee, currency |
| `travel_person_days` | TravelPersonDays | 差旅人天条目 | id, quotation_id, travel_category_id, person_days, unit_price |
| `travel_person_trips` | TravelPersonTrip | 差旅人次条目 | id, quotation_id, travel_category_id, travel_mode_id, person_count, unit_price, visa_fee |
| `version_snapshots` | VersionSnapshot | 版本快照 | id, quotation_id, version_no, snapshot_data(JSON), export_data(JSON), operation_type(archive/manual), remark, word_file, pdf_file |

### 6.2 系统表（10 张）

| 表名 | Model | 说明 |
|------|-------|------|
| `users` | User | 用户 |
| `roles` | Role | 角色 |
| `permissions` | Permission | 权限码（role_id + code + name + module） |
| `participant_type_permissions` | ParticipantTypePermission | 按参与类型分配 tab 可见性 |
| `organizations` | Organization | 组织（顶层） |
| `departments` | Department | 部门（FK→organizations） |
| `positions` | Position | 职位（FK→departments） |
| `employees` | Employee | 员工（从 SQL Server 同步） |
| `exchange_rates` | ExchangeRate | 汇率（currency + rate + is_base） |
| `change_requests` | ChangeRequest | 变更审核 |
| `operation_logs` | OperationLog | 操作日志 |
| `messages` | Message | 站内消息 |

### 6.3 ER 关系图

```
users ─┬─< quotation_participants >─ quotations ─< modules ─< module_materials >─ materials
       │                                  │     │
       │                                  ├─────┘
       │                                  ├─< other_fees >─ fee_types
       │                                  ├─< labor_hours
       │                                  ├─< version_snapshots
       │                                  ├─< packing_entries >─ packing_types
       │                                  ├─< travel_person_days >─ travel_categories
       │                                  └─< travel_person_trips >─ travel_categories
                                       │                         ─< travel_modes
                                       └─< self (parent_id) ─< self (children)

roles ─< permissions
participant_type_permissions ─< 用户访问报价单时按 participant_type 过滤
```

### 6.4 Cascade 行为（2026-06 修复）

所有引用 `quotations.id` 的外键均设为 `ON DELETE CASCADE`：

```sql
ALTER TABLE modules DROP CONSTRAINT modules_quotation_id_fkey,
                   ADD CONSTRAINT modules_quotation_id_fkey
                       FOREIGN KEY (quotation_id) REFERENCES quotations(id) ON DELETE CASCADE;
-- 同样处理 other_fees / labor_hours / quotation_participants /
-- version_snapshots / packing_entries / travel_person_days / travel_person_trips
```

**效果**：删除子报价单会真正级联删除全部子实体。

### 6.5 索引

- `quotations.parent_id`（线体聚合快速查询）
- 常用过滤字段均建索引
- 详见 `backend/migrations/`

### 6.6 各 model 完整字段

详细字段说明见 `~/wiki/entities/` 下的 9 个 entity 页面：
- `quotation-model.md` — 报价单
- `material-model.md` — 物料
- `module-model.md` — 模块
- `fee-model.md` — 费用
- `labor-hour-model.md` — 人力工时
- `travel-model.md` — 运输差旅
- `version-snapshot-model.md` — 版本快照
- `user-role-permission-model.md` — 用户权限
- `auxiliary-models.md` — 辅助模型

---

## 7. V2.1 新功能详解

V2.1（2026-05~06）相对 V2.0 新增：

### 7.1 线体报价单（Line Body）
详见使用手册 §4.4 + `~/wiki/concepts/line-body-concept.md`

### 7.2 三大费用 Tab（运输包装 / 差旅人天 / 差旅人次）
- 字典管理在 **🚚 运输差旅配置**
- 每个 Tab 都按 destination 聚合
- 权限码 `travel_fee_config.view` / `travel_fee_config.edit`

### 7.3 物料关键参数（param1/2/3）
- 物料库新增 3 个灵活字段
- 用于机构/电控选料参考（如「5 匹制冷量」、「R410A 环保冷媒」）
- 报价单物料清单 Tab 按需展示列

### 7.4 占比分析（汇总 tab 新增）
- 5 张占比卡片：硬件 / 人力 / 差旅 / 利润 / 税
- 硬件成本结构：大件/标准件/其他件 三档
- 堆叠条可视化
- 分母：`subtotal_with_profit`（含利润小计，不含税）

### 7.5 导出汇总 PDF（按网页样式）
- 用 `html2canvas` + `jsPDF`
- A4 四边各 5mm 边距
- 自动隐藏不需要元素（货币切换器、汇总 tab 内导出按钮）
- scale=2 高清

### 7.6 版本对比增强
- 物料差异用 `mm.id`（ModuleMaterial 主键）作 key，同物料在不同模块下不合并
- 差旅人天/人次字段名对齐（`quantity` 替代 `person_days`/`person_count`）
- 线体版本对比按 `version_no` 聚合所有子报价单快照

### 7.7 数据库 Cascade 强化
所有引用 `quotations.id` 的外键 `ON DELETE CASCADE`，子报价单删除真正级联。

### 7.8 UI 增强
- 查看页汇总 tab 与编辑页风格统一
- 占比卡片 + 硬件卡片改白底圆角大方块
- 导出按钮统一卡片风格
- 货币切换器默认隐藏（PDF 内不出现）

---

## 8. 业务规则与公式

### 8.1 汇总计算公式

```
material_total            = Σ module_materials.subtotal
material_total_with_rates = Σ subtotal × coefficient[category]

fee_total                = Σ other_fees.amount
labor_total              = Σ labor_hours.total
packing_total            = Σ packing_entries.total
                          = Σ (quantity × unit_price)
travel_person_days_total = Σ travel_person_days.total
                          = Σ (person_days × unit_price)
travel_person_trips_total = Σ travel_person_trips.total
                          = Σ (person_count × (unit_price + visa_fee))

fees_total = fee_total + labor_total + packing_total
           + travel_person_days_total + travel_person_trips_total

subtotal              = material_total + fees_total
subtotal_with_profit  = subtotal × (1 + profit_rate)
tax_amount            = subtotal_with_profit × tax_rate
grand_total           = subtotal_with_profit + tax_amount
```

### 8.2 物料分类归一化

物料表 `category` 字段（中文「大件/普通件/其他件」对应英文 large/standard/other）：
- 计算时统一转英文作为 `coefficients` 的 key
- 2026-06-09 修复：物料表 category 直接存英文，不再做中文映射

### 8.3 线体业务规则

| 规则 | 说明 |
|------|------|
| 子报价单上限 | 99 个 |
| 父线体删除 | 有 children 时禁止；否则按单机规则 |
| 子报价单删除 | 真正 cascade |
| 子报价单归档 | 禁止独立归档 |
| 父线体归档 | 自动归档所有子报价单 |
| 父线体撤销 | 同步撤销所有子报价单 |
| 线体 PDF | 只展示汇总数字，不展示单机明细 |

### 8.4 版本对比 key 规则

| 实体 | 对比 key | 备注 |
|------|----------|------|
| 物料 | `mat.id`（ModuleMaterial 主键） | **不用 material_id**，避免跨模块错误合并 |
| 费用 | `fee_type + location` | |
| 人力工时 | `name` | |
| 差旅人天 | `destination`（category name） | |
| 差旅人次 | `destination + travel_mode` | |
| 运输包装 | `packing_type_id` | |

### 8.5 权限码列表

| 权限码 | 说明 |
|--------|------|
| `quotation.view` | 查看报价单 |
| `quotation.edit` | 编辑报价单 |
| `quotation.archive` | 归档 |
| `quotation.delete` | 删除 |
| `quotation.export` | 导出 PDF/Word/Excel |
| `material.view` / `material.edit` | 物料库 |
| `fee_rate.view` / `fee_rate.edit` | 费用系数 |
| `travel_fee_config.view` / `travel_fee_config.edit` | 运输差旅字典 |
| `user.manage` / `role.manage` | 用户/角色管理 |
| `version.compare` / `version.rollback` | 版本对比/回滚 |
| `change_request.approve` | 变更审核 |
| `participant_type_permissions.view/edit` | 参与人权限 |

---

## 9. 已知陷阱与解决方案

### 9.1 后端 Python 陷阱

#### 🔴 Decimal(0.00) truthiness
```python
# ❌ 错
if entry.unit_price is not None:
    # Decimal(0.00) is not None = True，0 也会被当作有值
# ✅ 对
if entry.unit_price or entry.visa_fee:
    # 显式 truthy 判断
```
源：`travel_entries.py` 2026-06 修复

#### 🔴 ASGI reload 模式吞异常
**绝对不要**用 `uvicorn --reload`：
- reloader 会**静默吞 NameError**
- 前端看到「网络错误」但后端无任何日志
- 始终用 `python -m uvicorn main:fastapi_app`（不带 `--reload`）
- v17 已经验证：手动重启后无静默异常

#### 🔴 线体 PUT/DELETE 必须扩展查找范围
挂在子报价单上的所有实体，在 `quotation.type==='line'` 时 PUT/DELETE 都要扩展：

```python
# labor_hours.py update/delete
if quotation.type == 'line':
    all_ids = [quotation_id] + [c.id for c in quotation.children.all()]
    item = LaborHour.query.filter(
        LaborHour.id == item_id,
        LaborHour.quotation_id.in_(all_ids)
    ).first()
```
**必须扩展查找的实体**：LaborHour / OtherFee / ModuleMaterial / PackingEntry / TravelPersonDays / TravelPersonTrip

#### 🔴 物料差异 key
版本对比时**必须用 `mat.id`**（ModuleMaterial 主键），不要用 `material_id`。否则同物料在不同模块下会被错误合并。

### 9.2 前端 Vue 陷阱

#### 🔴 401 路由守卫 vs API 拦截器
```js
// 路由守卫
if (resp.code === 401) {
  authStore.clearAuth()  // 纯本地清，不调 API
  next('/login')
}
// axios 拦截器
if (resp.code === 401) {
  authStore.clearAuth()  // 只清本地，不自动跳转
  // 让路由守卫统一跳转
}
```
**绝对不要**用 `authStore.logout()` —— 它会调 API，可能再 401，进死循环。

#### 🔴 修改代码后必须重启服务
每次改完前后端代码后必跑：
```bash
ps aux | grep -E "uvicorn|npm|vite" | grep -v grep
```
挂了就用 `scripts/check-services.sh` 重启。

#### 🔴 is_other override 价
`is_other=true` 时单价 = `unit_price_override`，不是 `material.unit_price`。  
PDF 生成代码 4 处都要保留 override 价，不被 live 价覆盖。

### 9.3 数据库陷阱

#### 🔴 CASCADE 约束
2026-06 已将所有引用 `quotations.id` 的外键改为 `ondelete='CASCADE'`。  
子报价单删除会真正级联删除全部子实体（modules/fees/labor/packing/travel/versions）。

### 9.4 调试技巧

| 问题 | 排查步骤 |
|------|----------|
| 前端 500 无日志 | 后端关 reload 重启；看 `/tmp/fastapi.log` |
| 编辑子报价单 404 | 找后端路由是否漏了 line 类型扩展查找 |
| PDF 缺运输/差旅 | 检查 `calculate_version_totals` 的 fees_total 是否含三项 |
| 物料分类错了 | 物料表 category 字段；现统一英文 |
| 版本对比物料数量异常 | 检查 mat.id 是否正确传递 |
| 线体汇总少了某子 | 看 `all-modules` 是否被调用，`coefficients` 用哪个 |
| PDF/Word 字节数与旧版对不上 | v17 基准：v15/zh=19805, en=15372, docx=37409 bytes |

---

## 10. 附录

### 10.1 默认账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| `admin` | `admin123` | 超级管理员 |

### 10.2 端口分配

| 服务 | 端口 |
|------|------|
| 前端 Vite | 3000 |
| 后端 FastAPI | 5001 |
| PostgreSQL | 5432 |
| SQL Server（同步源） | 1433 |

### 10.3 定时任务

| 任务 | 周期 | 说明 |
|------|------|------|
| 消息清理 | 每天 03:00 | 已读 30 天/未读 60 天的消息 |
| 数据同步 | 每天 00:00 | 从 SQL Server 同步员工/部门/职位 |

### 10.4 文档地图

| 文档 | 用途 |
|------|------|
| `DEVELOPMENT.md`（本文） | 唯一权威开发 + 使用文档 |
| `SPEC.md` | 旧版产品技术规格 |
| `使用说明书.md` | 旧版用户使用手册 |
| `README.md` | 旧版快速介绍 |
| `~/wiki/index.md` | 知识库目录（28 页） |
| `~/wiki/concepts/` | 业务概念、流程、陷阱详解 |
| `~/wiki/api/` | REST API 按域分组详细说明 |
| `~/wiki/entities/` | 数据库 model 字段详解 |
| `~/wiki/schema/database-overview.md` | ER 图与 cascade 详解 |

### 10.5 术语表

| 术语 | 英文 | 含义 |
|------|------|------|
| 报价单 | Quotation | 一份完整报价，包含模块/物料/费用 |
| 线体 | Line Body | 包含多个子报价单的父报价单 |
| 子报价单 | Sub-quotation / Child | 线体下的独立可报价单元（工位） |
| 模块 | Module | 报价单下的功能分组 |
| 物料 | Material | 原材料/零件库 |
| 大件 | Large | 物料分类：价值高/体积大 |
| 普通件 | Standard | 物料分类：通用 |
| 其他件 | Other | 物料分类：杂项，可改单价不可改数量 |
| 费用系数 | Fee Rate | 按物料分类的乘数 |
| 归档 | Archive | 报价单锁定，生成 PDF/快照 |
| 快照 | Snapshot | VersionSnapshot.snapshot_data JSON |
| 参与人 | Participant | 报价单/模块上的协作人员 |
| 参与类型 | Participant Type | project/agency/electrical（项目/机构/电控） |

### 10.6 变更记录

| 日期 | 版本 | 内容 |
|------|------|------|
| 2026-06-10 | V2.1 | 新增线体、占比分析、运输差旅 Tab、版本对比增强、汇总截图 PDF；本文档整合 README/SPEC/使用说明书 |
| 2026-05 | V2.0 | 多币种、变更审核、操作日志 |
| 2025 | V1.x | 初版报价单/物料/费用基础功能 |

### 10.7 联系与反馈

- 仓库 Issues：https://github.com/hfy8/project-quote-system/issues
- 内部 Wiki：`~/wiki/`
- 代码规范：见 §2.4
