# 项目报价系统

基于 Vue3 + Flask 的企业级项目报价管理系统，支持报价单管理、物料配置、费用计算、版本控制等功能。

## 功能特性

### 核心功能
- **报价单管理** - 创建、编辑、归档报价单，支持版本管理
- **物料管理** - 物料分类、价格维护、参数配置
- **费用管理** - 厂内/厂外费用配置，税率管理
- **汇率管理** - 多币种汇率配置
- **变更申请** - 物料/费用变更审批流程
- **消息通知** - 实时消息推送，变更提醒
- **权限管理** - 基于角色的权限控制
- **操作日志** - 完整的操作审计追踪

### 技术亮点
- JWT 无状态认证
- RESTful API 设计
- 响应式表格滚动
- 清新商务风 UI

## 技术栈

### 前端
- **框架**: Vue 3 (Composition API)
- **构建**: Vite
- **UI**: Element Plus
- **状态**: Pinia
- **路由**: Vue Router
- **HTTP**: Axios

### 后端
- **框架**: Flask
- **ORM**: SQLAlchemy
- **认证**: Flask-JWT-Extended
- **数据库**: PostgreSQL / SQL Server
- **任务**: APScheduler

## 项目结构

```
project-quote-system/
├── frontend/                 # Vue3 前端项目
│   ├── src/
│   │   ├── api/             # API 接口封装
│   │   │   ├── auth.js
│   │   │   ├── quotations.js
│   │   │   ├── materials.js
│   │   │   ├── messages.js
│   │   │   └── ...
│   │   ├── components/       # 公共组件
│   │   │   ├── Layout.vue   # 页面布局
│   │   │   └── Sidebar.vue  # 侧边栏
│   │   ├── views/           # 页面视图
│   │   │   ├── Quotations.vue
│   │   │   ├── Materials.vue
│   │   │   ├── Fees.vue
│   │   │   └── ...
│   │   ├── stores/          # Pinia 状态管理
│   │   ├── router/          # 路由配置
│   │   └── utils/           # 工具函数
│   ├── package.json
│   └── vite.config.js
│
├── backend/                  # Flask 后端项目
│   ├── app/
│   │   ├── models/          # 数据模型
│   │   │   ├── quotation.py
│   │   │   ├── material.py
│   │   │   ├── module.py
│   │   │   ├── message.py
│   │   │   └── ...
│   │   ├── routes/          # API 路由
│   │   │   ├── auth.py
│   │   │   ├── quotations.py
│   │   │   ├── materials.py
│   │   │   └── ...
│   │   ├── services/        # 业务逻辑
│   │   ├── utils/          # 工具函数
│   │   └── tasks/          # 定时任务
│   ├── versions/            # 报价单版本文件
│   ├── run.py              # 启动入口
│   └── requirements.txt
│
├── SPEC.md                  # 项目规格说明
└── README.md
```

## 快速开始

### 环境要求
- Node.js >= 16
- Python >= 3.9
- PostgreSQL >= 13 或 SQL Server

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
# 编辑 .env 文件或设置以下环境变量:
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

## API 文档

### 认证接口

| 方法 | 路径 | 说明 |
|-----|------|------|
| POST | /api/auth/login | 用户登录 |
| POST | /api/auth/logout | 用户登出 |
| GET | /api/auth/me | 获取当前用户信息 |
| POST | /api/auth/change-password | 修改密码 |

### 报价单接口

| 方法 | 路径 | 说明 |
|-----|------|------|
| GET | /api/quotations | 获取报价单列表 |
| POST | /api/quotations | 创建报价单 |
| GET | /api/quotations/:id | 获取报价单详情 |
| PUT | /api/quotations/:id | 更新报价单 |
| PUT | /api/quotations/:id/archive | 归档报价单 |
| GET | /api/quotations/:id/versions | 获取版本列表 |
| POST | /api/quotations/:id/versions | 创建新版本 |

### 物料接口

| 方法 | 路径 | 说明 |
|-----|------|------|
| GET | /api/materials | 获取物料列表 |
| POST | /api/materials | 创建物料 |
| PUT | /api/materials/:id | 更新物料 |
| DELETE | /api/materials/:id | 删除物料 |

### 消息接口

| 方法 | 路径 | 说明 |
|-----|------|------|
| GET | /api/messages | 获取消息列表 |
| GET | /api/messages/unread-count | 获取未读消息数 |
| PUT | /api/messages/:id/read | 标记已读 |
| PUT | /api/messages/read-all | 全部已读 |

### 费用接口

| 方法 | 路径 | 说明 |
|-----|------|------|
| GET | /api/fees | 获取费用列表 |
| POST | /api/fees | 创建费用 |
| PUT | /api/fees/:id | 更新费用 |
| GET | /api/fee-rates | 获取费用配置 |
| PUT | /api/fee-rates | 更新费用配置 |

### 汇率接口

| 方法 | 路径 | 说明 |
|-----|------|------|
| GET | /api/exchange-rates | 获取汇率列表 |
| PUT | /api/exchange-rates | 更新汇率 |

### 变更申请接口

| 方法 | 路径 | 说明 |
|-----|------|------|
| GET | /api/change-requests | 获取变更申请列表 |
| POST | /api/change-requests | 创建变更申请 |
| PUT | /api/change-requests/:id/approve | 批准申请 |
| PUT | /api/change-requests/:id/reject | 拒绝申请 |

### 用户权限接口

| 方法 | 路径 | 说明 |
|-----|------|------|
| GET | /api/users | 获取用户列表 |
| GET | /api/roles | 获取角色列表 |
| GET | /api/permissions | 获取权限列表 |
| GET | /api/logs | 获取操作日志 |

## 数据模型

### 报价单 (Quotation)
- id, name, customer_name, status
- created_by, created_at
- archived_at, version

### 报价模块 (Module)
- id, quotation_id, name
- business_负责人, technician_负责人
- internal_total, external_total

### 物料 (Material)
- id, code, name, unit_price
- category, supplier

### 消息 (Message)
- id, sender_id, recipient_id
- title, content, type
- related_id, related_type
- is_read, created_at

### 变更申请 (ChangeRequest)
- id, quotation_id, module_id
- type, status
- applicant_id, reviewer_id
- changes, created_at

## 消息类型

| 类型 | 说明 | 触发时机 |
|-----|------|---------|
| module_member_added | 成员加入 | 添加成员到模块 |
| change_request_submitted | 变更提交 | 提交变更申请 |
| change_request_approved | 变更批准 | 审批通过 |
| change_request_rejected | 变更拒绝 | 审批拒绝 |
| version_updated | 版本更新 | 创建新版本 |

## 费用字段说明

| 字段 | 说明 |
|-----|------|
| internal | 厂内费用 |
| external | 厂外费用 |

## 权限说明

系统采用基于角色的权限控制 (RBAC)，主要权限包括：

| 权限 | 说明 |
|-----|------|
| quotation.view | 查看报价单 |
| quotation.create | 创建报价单 |
| quotation.edit | 编辑报价单 |
| quotation.delete | 删除报价单 |
| quotation.archive | 归档报价单 |
| material.view | 查看物料 |
| material.edit | 编辑物料 |
| fee.edit | 编辑费用 |
| change_request.approve | 审批变更 |
| user.edit | 管理用户 |

## 开发指南

### 添加新的 API

1. 在 `backend/app/routes/` 创建路由文件
2. 注册蓝图到 `backend/app/routes/__init__.py`
3. 在 `frontend/src/api/` 创建前端 API 封装

### 添加新的数据模型

1. 在 `backend/app/models/` 创建模型文件
2. 更新 `backend/app/models/__init__.py` 导出
3. 执行数据库迁移

### 前端页面开发

1. 在 `frontend/src/views/` 创建 Vue 组件
2. 在 `frontend/src/router/index.js` 添加路由
3. 配置权限映射

## 定时任务

系统自动执行以下定时任务：
- **消息清理**: 每天凌晨 3:00，清理已读超过 30 天或未读超过 60 天的消息
- **数据同步**: 从 SQL Server 同步员工/部门/职位数据

## 许可证

MIT License
