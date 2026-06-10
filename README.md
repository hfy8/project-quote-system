# 项目报价系统

基于 Vue3 + Flask 的企业级项目报价管理系统，支持报价单管理、物料配置、费用计算、版本控制、变更审批、消息通知等功能。

## 功能特性

### 核心功能
- **报价单管理** - 创建、编辑、归档报价单，支持版本历史
- **模块管理** - 报价单下的模块划分，成员任务分配
- **物料管理** - 物料库维护，支持分类检索
- **费用管理** - 厂内/厂外费用配置，支持费用类型自定义
- **费用系数** - 大件/普通件/其他件分类系数配置
- **汇率管理** - 多币种汇率配置与转换
- **变更申请** - 物料/费用变更审批流程
- **版本控制** - 报价单版本快照，支持回退
- **消息通知** - 实时消息推送，变更提醒
- **权限管理** - 基于角色的权限控制 (RBAC)
- **操作日志** - 完整的操作审计追踪
- **数据同步** - 从 SQL Server 同步员工/部门/职位数据

### 技术亮点
- JWT 无状态认证
- RESTful API 设计
- 响应式表格滚动
- 清新商务风 UI (#0D9488 主色调)
- 消息自动清理（定时任务）

## 技术栈

### 前端
| 技术 | 版本 | 说明 |
|-----|------|------|
| Vue 3 | 3.4.21 | 前端框架 |
| Vite | 5.1.6 | 构建工具 |
| Element Plus | 2.6.1 | UI 组件库 |
| Pinia | 2.1.7 | 状态管理 |
| Vue Router | 4.3 | 路由管理 |
| Axios | 1.6.7 | HTTP 客户端 |
| Sass | 1.71.1 | CSS 预处理器 |

### 后端
| 技术 | 版本 | 说明 |
|-----|------|------|
| Python | 3.12 | 编程语言 |
| Flask | 3.0 | Web 框架 |
| SQLAlchemy | 2.0 | ORM |
| Flask-JWT-Extended | 4.6 | JWT 认证 |
| APScheduler | 4.6 | 定时任务 |
| python-docx | 1.1 | Word 文档生成 |
| openpyxl | 3.1 | Excel 操作 |

### 数据库
| 数据库 | 用途 |
|-------|------|
| PostgreSQL | 主数据库 |
| SQL Server | 同步数据源 (RSHRIS) |

## 快速开始

### 环境要求
- Node.js >= 16
- Python >= 3.9
- PostgreSQL >= 13
- SQL Server (可选，用于数据同步)

### 后端部署

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
# 设置以下环境变量:
# DATABASE_URL=postgresql://user:pass@localhost:5432/quote_db
# SECRET_KEY=your-secret-key
# SQL_SERVER_HOST=192.168.100.70
# SQL_SERVER_PORT=1433
# SQL_SERVER_DB=RSHRIS
# SQL_SERVER_USER=sa
# SQL_SERVER_PASSWORD=Kayang123#

# 初始化数据库
python init_db.py

# 启动服务
python run.py
```

后端服务运行在 http://localhost:5000

### 前端部署

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

前端服务运行在 http://localhost:3000

## 默认账号

| 角色 | 用户名 | 密码 |
|-----|--------|------|
| 管理员 | admin | admin123 |

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
| 消息清理 | 每天 03:00 | 清理已读30天/未读60天消息 |
| 数据同步 | 每天 00:00 | 同步员工/部门/职位数据 |

## API 概览

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
- `PUT /api/quotations/:id/archive` - 归档

### 模块
- `GET /api/quotations/:qid/modules` - 列表
- `POST /api/quotations/:qid/modules` - 创建
- `GET /api/modules/:id/participants` - 成员

### 消息
- `GET /api/messages` - 列表
- `GET /api/messages/unread-count` - 未读数
- `PUT /api/messages/:id/read` - 标记已读

## 项目结构

```
project-quote-system/
├── backend/
│   ├── app/
│   │   ├── models/          # 17个数据模型
│   │   ├── routes/          # 17个API蓝图
│   │   ├── services/        # 业务逻辑
│   │   ├── utils/           # 工具函数
│   │   └── tasks/           # 定时任务
│   ├── versions/            # 版本文件存储
│   ├── run.py               # 启动入口
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── api/             # 16个API模块
│   │   ├── components/      # 布局组件
│   │   ├── views/           # 17个页面
│   │   ├── stores/          # Pinia状态
│   │   └── router/          # 路由配置
│   ├── package.json
│   └── vite.config.js
│
├── SPEC.md                  # 技术规格说明
└── README.md                # 本文件
```

## 文档地图

| 文档 | 用途 | 状态 |
|------|------|------|
| [DEVELOPMENT.md](./DEVELOPMENT.md) | **唯一权威开发 + 使用文档** | V2.1 推荐 |
| [SPEC.md](./SPEC.md) | 旧版产品技术规格 | 归档 |
| [使用说明书.md](./使用说明书.md) | 旧版用户使用手册 | 归档 |
| `~/wiki/index.md` | LLM Wiki 知识库目录（28 页） | 持续维护 |

**新成员请直接读 DEVELOPMENT.md**。本文（README）保留作为快速索引。

## 许可证

MIT License
