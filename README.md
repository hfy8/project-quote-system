# 项目报价系统

> V2.2（2026-06-12） · [仓库](https://github.com/hfy8/project-quote-system) · 技术栈：**Vue 3 + FastAPI + PostgreSQL**（v17 彻底移除 Flask）

基于 Vue3 + FastAPI 的企业级项目报价管理系统，支持报价单管理、物料配置、费用计算、版本控制、变更审批、消息通知、定时同步等完整业务闭环。

## 功能特性

### 核心功能
- **报价单管理** - 创建、编辑、归档报价单，支持版本历史（PDF/Word 导出）
- **模块管理** - 报价单下的模块划分，成员任务分配
- **物料管理** - 物料库维护，支持分类、检索、Excel 导入
- **费用管理** - 厂内/厂外费用配置，支持费用类型自定义
- **费用系数** - 大件/普通件/其他件分类系数配置
- **汇率管理** - 多币种汇率配置与转换（含基准货币切换）
- **运输差旅** - 包装/人员/差旅条目 + 运输差旅配置
- **人工工时** - 模块人工工时配置
- **变更申请** - 物料/费用变更审批流程
- **版本控制** - 报价单版本快照，PDF/Word 导出，支持回退与对比
- **消息通知** - 实时消息推送，变更提醒，自动清理
- **权限管理** - 基于角色的权限控制 (RBAC) — 4 个默认角色 / 40+ 权限码
- **操作日志** - 完整的操作审计追踪（IP/UA 记录）
- **数据同步** - 每天 22:00 从 SQL Server (RSHRIS) 同步员工/部门/职位
- **消息清理** - 每天 03:00 清理过期消息

### 技术亮点
- JWT 无状态认证（python-jose）
- 纯 SQLAlchemy 2.x ORM（无 Flask-SQLAlchemy）
- 清新商务风 UI（#0D9488 主色调）
- 响应式表格滚动
- 异步 PDF/Word 导出（中文字体嵌入）

## 技术栈

### 前端
| 技术 | 版本 | 说明 |
|-----|------|------|
| Vue 3 | 3.4+ | 前端框架 |
| Vite | 5+ | 构建工具 |
| Element Plus | 2.6+ | UI 组件库 |
| Pinia | 2.1+ | 状态管理 |
| Vue Router | 4.3+ | 路由管理 |
| Axios | 1.6+ | HTTP 客户端 |
| Sass | 1.71+ | CSS 预处理器 |

### 后端
| 技术 | 版本 | 说明 |
|-----|------|------|
| Python | 3.12 | 编程语言 |
| FastAPI | 0.110+ | Web 框架（**取代 Flask**） |
| Uvicorn | 0.27+ | ASGI 服务器 |
| SQLAlchemy | 2.0+ | ORM（**纯 2.x，无 Flask-SQLAlchemy**） |
| python-jose | 3.3+ | JWT 认证（**取代 flask-jwt-extended**） |
| APScheduler | 3.10+ | 定时任务 |
| reportlab | 4.0+ | PDF 导出 |
| python-docx | 1.0+ | Word 导出 |
| openpyxl | 3.1+ | Excel 导入导出 |
| werkzeug | 3.0+ | 密码哈希（**scrypt 格式兼容**） |
| psycopg2-binary | 2.9+ | PostgreSQL 驱动 |

### 数据库
| 数据库 | 用途 |
|-------|------|
| PostgreSQL | 主数据库（业务数据） |
| SQL Server (RSHRIS) | 同步数据源（员工/部门/职位） |

## 快速开始

### 环境要求
- Node.js >= 16
- Python >= 3.9
- PostgreSQL >= 13
- SQL Server (可选，用于数据同步)

### 后端启动

```bash
# 进入后端目录
cd backend_fastapi

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置数据库连接（通过环境变量或 core/config.py）
# DATABASE_URL=postgresql://postgres:password@localhost:5432/quote_db

# 启动服务（uvicorn 加载 main:fastapi_app）
python -m uvicorn main:fastapi_app --host 0.0.0.0 --port 5001 --reload

# 或直接运行
python main.py
```

后端服务运行在 **http://localhost:5001**

### 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 开发模式
npm run dev

# 生产构建
npm run build
```

前端服务运行在 **http://localhost:3000**

## 默认账号

| 角色 | 用户名 | 密码 |
|-----|--------|------|
| 管理员 | admin | admin123 |

## 项目结构

```
project-quote-system/
├── backend_fastapi/                # 🚀 后端（FastAPI，无 Flask）
│   ├── main.py                     # FastAPI 入口（uvicorn 加载 fastapi_app）
│   ├── db.py                       # 纯 SQLAlchemy 2.x 启动 + _DBProxy
│   ├── requirements.txt            # 无 flask / flask-* / a2wsgi
│   ├── api/                        # 19 个 FastAPI 路由
│   │   ├── auth.py                 # 登录/登出/改密
│   │   ├── quotations.py           # 报价单（CRUD + 归档 + PDF/Word 导出）
│   │   ├── modules.py              # 模块管理
│   │   ├── materials.py            # 物料库
│   │   ├── fees.py                 # 费用管理
│   │   ├── fee_rates.py            # 费用系数
│   │   ├── exchange_rates.py       # 汇率（含 set-base 端点）
│   │   ├── labor_hours.py          # 人工工时
│   │   ├── travel_entries.py       # 包装条目
│   │   ├── travel_fees.py          # 运输差旅
│   │   ├── versions.py             # 版本对比
│   │   ├── change_requests.py      # 变更申请
│   │   ├── messages.py             # 消息通知
│   │   ├── users.py / roles.py     # 用户/角色
│   │   ├── logs.py                 # 操作日志
│   │   ├── module_participants.py  # 模块成员
│   │   ├── participant_type_permissions.py
│   │   ├── exports.py / sync.py
│   │
│   ├── core/                       # ⭐ 核心业务包
│   │   ├── __init__.py             # 触发 models 注册
│   │   ├── config.py               # 数据库连接配置
│   │   ├── schemas.py              # Pydantic 数据模型
│   │   ├── models/                 # 21 个数据模型
│   │   │   ├── user.py, quotation.py, material.py
│   │   │   ├── module.py, fee.py, fee_rate.py
│   │   │   ├── labor_hour.py, travel.py, travel_entry.py
│   │   │   ├── packing.py, version.py, message.py
│   │   │   ├── change_request.py, operation_log.py
│   │   │   ├── exchange_rate.py, permission.py
│   │   │   ├── organization.py, department.py
│   │   │   ├── position.py, employee.py
│   │   │   └── participant_type_permission.py
│   │   ├── services/               # 业务服务
│   │   │   ├── export_service.py   # PDF/Word 生成（19805 bytes 一致性已验证）
│   │   │   └── message_service.py
│   │   └── tasks/
│   │       └── sync_task.py        # SQL Server 同步任务
│   │
│   ├── utils/                      # 工具
│   │   ├── permissions.py          # 权限检查 + seed（无 flask_jwt_extended）
│   │   └── logger.py               # 操作日志（threading.local 替代 flask.request）
│   │
│   ├── fonts/                      # 中文字体（simhei.ttf, msyh.ttc）
│   ├── static/versions/            # 归档 PDF/Word 存储（统一路径）
│   └── tests/                      # （预留测试目录）
│
├── frontend/                       # Vue3 + Vite 前端
│   ├── src/
│   │   ├── api/                    # 16 个 API 模块
│   │   ├── components/             # 布局组件
│   │   ├── views/                  # 17+ 个页面
│   │   ├── stores/                 # Pinia 状态
│   │   └── router/                 # 路由配置
│   ├── package.json
│   └── vite.config.js
│
├── docs/                           # 项目文档
├── screenshots/                    # 截图
├── SPEC.md                         # 旧版技术规格
├── 使用说明书.md                    # 旧版用户手册
├── DEVELOPMENT.md                  # 详细开发文档
└── README.md                       # 本文件（快速索引）
```

## 页面导航

| 路径 | 页面 | 说明 |
|-----|------|------|
| /login | 登录 | 用户登录 |
| /dashboard | 工作台 | 首页概览 |
| /quotations | 报价单 | 报价单列表 |
| /quotations/new | 新建报价单 | 创建报价单 |
| /quotations/:id | 报价单详情 | 编辑报价单 |
| /change-requests | 变更申请 | 变更审批 |
| /materials | 原材料库 | 物料管理 |
| /fee-types | 费用类型 | 费用类型配置 |
| /fees | 费用管理 | 费用配置 |
| /fee-rates | 费用系数 | 大件/普通件/其他件系数 |
| /exchange-rates | 汇率配置 | 货币汇率 |
| /users | 用户管理 | 用户管理 |
| /roles | 角色管理 | 角色权限 |
| /logs | 操作日志 | 审计日志 |
| /my-assignments | 我的任务 | 模块任务分配 |

## 消息类型

| 类型 | 触发时机 | 接收人 |
|-----|---------|-------|
| module_member_added | 添加成员到模块 | 被添加成员 |
| change_request_submitted | 成员提交变更 | 业务员 |
| change_request_approved | 变更批准 | 申请人 |
| change_request_rejected | 变更拒绝 | 申请人 |
| version_updated | 版本更新 | 相关成员 |

## 费用字段规范

| 字段 | 说明 |
|-----|------|
| internal | 厂内费用 |
| external | 厂外费用 |

## 定时任务

| 任务 | 周期 | 说明 |
|-----|------|------|
| 数据同步 | 每天 22:00 | 从 SQL Server 同步员工/部门/职位 |
| 消息清理 | 每天 03:00 | 清理已读 30 天/未读 60 天消息 |

## API 概览

> 完整 131+ 个端点索引见 [DEVELOPMENT.md](./DEVELOPMENT.md)

### 认证
- `POST /api/auth/login` - 登录
- `POST /api/auth/logout` - 登出
- `GET /api/auth/me` - 当前用户
- `POST /api/auth/change-password` - 修改密码

### 报价单
- `GET /api/quotations` - 列表
- `POST /api/quotations` - 创建
- `GET /api/quotations/:id` - 详情
- `PUT /api/quotations/:id` - 更新
- `POST /api/quotations/:id/archive` - 归档
- `POST /api/quotations/:id/unarchive` - 取消归档
- `GET /api/quotations/:id/versions` - 版本历史

### 汇率
- `GET /api/exchange_rates` - 列表
- `POST /api/exchange_rates` - 创建
- `GET /api/exchange_rates/base` - 基准货币
- `POST /api/exchange_rates/:id/set-base` - 设为基准
- `GET /api/exchange_rates/convert` - 货币转换

## 文档地图

| 文档 | 用途 | 状态 |
|------|------|------|
| [README.md](./README.md) | 快速索引（本文） | ✅ 维护中 |
| [DEVELOPMENT.md](./DEVELOPMENT.md) | 详细开发 + 使用文档（131+ API） | ✅ 维护中 |
| [SPEC.md](./SPEC.md) | 旧版产品技术规格 | 归档 |
| [使用说明书.md](./使用说明书.md) | 旧版用户使用手册 | 归档 |

**新成员请直接读 DEVELOPMENT.md**。本文（README）作为快速索引。

## 版本演进

| 版本 | 日期 | 变更 |
|-----|------|------|
| V1.0 | 2026-04 | 初始提交（Flask 时代） |
| V2.0 | 2026-05 | Flask → FastAPI 迁移（19 路由 + 21 models） |
| V2.1 | 2026-06-10 | 功能完善（运输差旅、变更申请、消息） |
| **V2.2** | **2026-06-12** | **彻底移除 Flask + 目录整理（v17）** |

## 许可证

MIT License
