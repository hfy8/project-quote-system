# 项目报价系统 - 技术规格说明书

## 1. 项目概述

### 1.1 项目信息
- **项目名称**: 项目报价管理系统
- **版本**: V2.1
- **项目类型**: 企业级 Web 应用
- **仓库**: https://github.com/hfy8/project-quote-system

### 1.2 核心业务流程
```
创建报价单 → 创建模块 → 从原材料库选入物料 → 配置其他费用 → 生成报价单 → 归档管理
```

### 1.3 技术栈

| 层级 | 技术 | 说明 |
|-----|------|------|
| 前端框架 | Vue 3.4 + Composition API | 响应式前端 |
| UI 组件 | Element Plus 2.6 | PC 端组件库 |
| 状态管理 | Pinia 2.1 | Vue3 状态管理 |
| 构建工具 | Vite 5.1 | 快速构建 |
| 后端框架 | Flask 3.0 | Python Web 框架 |
| ORM | SQLAlchemy | 数据库 ORM |
| 认证 | Flask-JWT-Extended | JWT 无状态认证 |
| 定时任务 | APScheduler | 定时任务调度 |
| 数据库 | PostgreSQL + SQL Server | 主库 + 同步数据源 |

### 1.4 系统架构图
```
┌─────────────────────────────────────────────────────────────┐
│                        前端 (Vue3)                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │报价单管理│  │物料管理 │  │费用管理 │  │消息通知 │       │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘       │
└───────┼────────────┼────────────┼────────────┼─────────────┘
        │            │            │            │
        └────────────┴─────┬──────┴────────────┘
                           │ HTTP REST API
        ┌──────────────────┼──────────────────┐
        │           后端 (Flask)              │
        │  ┌─────────┐  ┌─────────┐        │
        │  │ API路由  │  │ 业务服务 │        │
        │  └────┬────┘  └────┬────┘        │
        │       │           │              │
        │  ┌────┴───────────┴────┐        │
        │  │     SQLAlchemy ORM   │        │
        │  └──────────┬───────────┘        │
        └─────────────┼────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
   PostgreSQL                  SQL Server
   (主数据库)                  (RSHRIS同步源)
```

---

## 2. 数据模型设计

### 2.1 模型总览 (17个)

| 模型 | 说明 | 主要字段 |
|-----|------|---------|
| User | 用户 | id, username, password_hash, real_name, role |
| Quotation | 报价单 | id, name, status, business_owner_id, tax_rate |
| QuotationParticipant | 报价单参与人 | quotation_id, user_id |
| Module | 报价模块 | id, quotation_id, name, business_lead_id, technician_lead_id |
| ModuleParticipant | 模块参与人 | module_id, user_id |
| Material | 物料 | id, code, name, unit_price, category, supplier |
| ModuleMaterial | 模块物料 | module_id, material_id, quantity |
| OtherFee | 其他费用 | quotation_id, module_id, fee_type, location, amount |
| FeeType | 费用类型 | id, name, location |
| FeeRate | 费用系数 | category, rate |
| ExchangeRate | 汇率 | currency, rate, is_base |
| VersionSnapshot | 版本快照 | quotation_id, version_no, snapshot_data |
| ChangeRequest | 变更申请 | quotation_id, type, status, applicant_id |
| Message | 消息通知 | sender_id, recipient_id, title, content, type, is_read |
| OperationLog | 操作日志 | user_id, action, module, resource_type |
| Employee | 员工(SQL Server同步) | employee_id, name, department, position |
| Department/Position/Organization | 组织架构同步 | ... |

### 2.2 核心关系图
```
用户 (User)
   │
   ├────< 报价单 (Quotation) >──── 报价单参与人 (QuotationParticipant)
   │              │
   │              ├────< 模块 (Module) >──── 模块参与人 (ModuleParticipant)
   │              │              │
   │              │              ├────< 模块物料 (ModuleMaterial) >──── 物料 (Material)
   │              │              │
   │              │              └──── 其他费用 (OtherFee)
   │              │
   │              └────< 版本快照 (VersionSnapshot)
   │              │
   │              └────< 变更申请 (ChangeRequest)
   │
   └────< 消息 (Message)
```

### 2.3 字段命名规范

| 规范 | 说明 |
|-----|------|
| 费用位置 | `internal` = 厂内, `external` = 厂外 |
| 物料分类 | `large` = 大件, `normal` = 普通件, `other` = 其他件 |
| 状态流转 | `draft` → `in_progress` → `approved` → `archived` |

---

## 3. API 接口设计

### 3.1 认证模块 (/api/auth)
| 方法 | 路径 | 说明 |
|-----|------|------|
| POST | /api/auth/login | 用户登录 |
| POST | /api/auth/logout | 用户登出 |
| GET | /api/auth/me | 获取当前用户信息 |
| POST | /api/auth/change-password | 修改密码 |

### 3.2 报价单模块 (/api/quotations)
| 方法 | 路径 | 说明 |
|-----|------|------|
| GET | /api/quotations | 获取报价单列表 |
| POST | /api/quotations | 创建报价单 |
| GET | /api/quotations/:id | 获取报价单详情 |
| PUT | /api/quotations/:id | 更新报价单 |
| DELETE | /api/quotations/:id | 删除报价单 |
| PUT | /api/quotations/:id/archive | 归档报价单 |
| PUT | /api/quotations/:id/unarchive | 撤销归档 |
| GET | /api/quotations/:id/summary | 获取汇总数据 |
| GET | /api/quotations/:id/versions | 获取版本列表 |
| POST | /api/quotations/:id/versions | 创建新版本 |
| GET | /api/quotations/:id/participants | 获取参与人员 |
| POST | /api/quotations/:id/participants | 添加参与人员 |
| DELETE | /api/quotations/:id/participants/:uid | 移除参与人员 |

### 3.3 模块管理 (/api/modules)
| 方法 | 路径 | 说明 |
|-----|------|------|
| GET | /api/quotations/:qid/modules | 获取模块列表 |
| POST | /api/quotations/:qid/modules | 创建模块 |
| GET | /api/modules/:id | 获取模块详情 |
| PUT | /api/modules/:id | 更新模块 |
| DELETE | /api/modules/:id | 删除模块 |
| GET | /api/modules/:id/participants | 获取模块参与人员 |
| POST | /api/modules/:id/participants | 添加模块参与人员 |
| DELETE | /api/modules/:id/participants/:uid | 移除模块参与人员 |
| GET | /api/modules/:id/materials | 获取模块物料 |

### 3.4 物料模块 (/api/materials)
| 方法 | 路径 | 说明 |
|-----|------|------|
| GET | /api/materials | 获取物料列表 |
| POST | /api/materials | 创建物料 |
| PUT | /api/materials/:id | 更新物料 |
| DELETE | /api/materials/:id | 删除物料 |
| POST | /api/materials/import | 批量导入 |

### 3.5 费用模块 (/api/fees)
| 方法 | 路径 | 说明 |
|-----|------|------|
| GET | /api/fees | 获取费用列表 |
| POST | /api/fees | 创建费用 |
| PUT | /api/fees/:id | 更新费用 |
| DELETE | /api/fees/:id | 删除费用 |
| GET | /api/fee-types | 获取费用类型 |
| POST | /api/fee-types | 创建费用类型 |
| PUT | /api/fee-types/:id | 更新费用类型 |

### 3.6 版本模块 (/api/versions)
| 方法 | 路径 | 说明 |
|-----|------|------|
| GET | /api/versions/:id | 获取版本详情 |
| POST | /api/versions/:id/rollback | 回退版本 |
| GET | /api/versions/:id/export | 导出版本 |

### 3.7 变更申请 (/api/change-requests)
| 方法 | 路径 | 说明 |
|-----|------|------|
| GET | /api/change-requests | 获取变更申请列表 |
| POST | /api/change-requests | 创建变更申请 |
| GET | /api/change-requests/:id | 获取详情 |
| PUT | /api/change-requests/:id/approve | 批准申请 |
| PUT | /api/change-requests/:id/reject | 拒绝申请 |

### 3.8 消息模块 (/api/messages)
| 方法 | 路径 | 说明 |
|-----|------|------|
| GET | /api/messages | 获取消息列表 |
| GET | /api/messages/unread-count | 获取未读数量 |
| PUT | /api/messages/:id/read | 标记已读 |
| PUT | /api/messages/read-all | 全部已读 |

### 3.9 系统配置
| 方法 | 路径 | 说明 |
|-----|------|------|
| GET | /api/fee-rates | 获取费用系数 |
| PUT | /api/fee-rates | 更新费用系数 |
| GET | /api/exchange-rates | 获取汇率配置 |
| PUT | /api/exchange-rates | 更新汇率配置 |

### 3.10 用户权限 (/api/users, /api/roles)
| 方法 | 路径 | 说明 |
|-----|------|------|
| GET | /api/users | 获取用户列表 |
| POST | /api/users | 创建用户 |
| PUT | /api/users/:id | 更新用户 |
| DELETE | /api/users/:id | 删除用户 |
| GET | /api/roles | 获取角色列表 |
| GET | /api/permissions | 获取权限列表 |
| GET | /api/logs | 获取操作日志 |

### 3.11 数据同步 (/api/sync)
| 方法 | 路径 | 说明 |
|-----|------|------|
| POST | /api/sync/employees | 同步员工数据 |
| POST | /api/sync/departments | 同步部门数据 |
| POST | /api/sync/positions | 同步职位数据 |

---

## 4. 前端页面结构

### 4.1 页面清单 (17个)

| 路径 | 页面 | 权限 | 说明 |
|-----|------|------|------|
| /login | 登录页 | 公开 | 用户登录 |
| /dashboard | 工作台 | dashboard.view | 首页概览 |
| /quotations | 报价单列表 | quotation.view | 报价单管理 |
| /quotations/new | 新建报价单 | quotation.create | 创建报价单 |
| /quotations/:id | 报价单详情 | quotation.view | 编辑报价单 |
| /change-requests | 变更申请 | change_request.view | 变更审批 |
| /materials | 原材料库 | material.view | 物料管理 |
| /fee-types | 费用类型 | fee_type.view | 费用类型配置 |
| /fees | 费用管理 | fee.view | 费用配置 |
| /fee-rates | 费用系数 | fee_rate.view | 大件/普通件/其他件系数 |
| /exchange-rates | 汇率配置 | exchange_rate.view | 货币汇率 |
| /users | 用户管理 | user.view | 用户管理 |
| /roles | 角色管理 | role.view | 角色权限配置 |
| /logs | 操作日志 | log.view | 审计日志 |
| /system | 系统设置 | system.view | 系统配置 |
| /my-assignments | 我的任务 | 公开 | 模块任务分配 |

### 4.2 布局结构
```
┌─────────────────────────────────────────────────┐
│  Logo    报价系统          🔔[铃铛]  [用户菜单] │
├─────────┬───────────────────────────────────────┤
│         │                                       │
│  导航菜单 │           主内容区域                  │
│         │                                       │
│  🏠 首页  │    ┌─────────────────────────┐      │
│  📋 报价单│    │                         │      │
│  📦 物料  │    │    <router-view />      │      │
│  💰 费用  │    │                         │      │
│  📊 汇率  │    └─────────────────────────┘      │
│  ...    │                                       │
│         │                                       │
├─────────┼───────────────────────────────────────┤
│ 用户信息 │  🔑 修改密码  🚪 退出登录              │
└─────────┴───────────────────────────────────────┘
```

---

## 5. 消息通知系统

### 5.1 消息类型
| 类型 | 触发时机 | 接收人 |
|-----|---------|-------|
| module_member_added | 添加成员到模块 | 被添加成员 |
| change_request_submitted | 成员提交变更 | 业务员 |
| change_request_approved | 变更批准 | 申请人 |
| change_request_rejected | 变更拒绝 | 申请人 |
| version_updated | 版本更新 | 相关成员 |

### 5.2 消息清理规则
- 已读消息：30天后自动清理
- 未读消息：60天后自动清理
- 清理时间：每日凌晨 3:00

---

## 6. 权限系统

### 6.1 权限列表
| 权限 | 说明 |
|-----|------|
| dashboard.view | 查看工作台 |
| quotation.view | 查看报价单 |
| quotation.create | 创建报价单 |
| quotation.edit | 编辑报价单 |
| quotation.delete | 删除报价单 |
| quotation.archive | 归档报价单 |
| material.view | 查看物料 |
| material.edit | 编辑物料 |
| material.delete | 删除物料 |
| fee_type.view | 查看费用类型 |
| fee_type.edit | 编辑费用类型 |
| fee_rate.view | 查看费用系数 |
| fee_rate.edit | 编辑费用系数 |
| exchange_rate.view | 查看汇率 |
| exchange_rate.edit | 编辑汇率 |
| change_request.view | 查看变更申请 |
| change_request.approve | 审批变更 |
| user.view | 查看用户 |
| user.edit | 编辑用户 |
| role.view | 查看角色 |
| role.edit | 编辑角色 |
| log.view | 查看日志 |
| * | 超级管理员(所有权限) |

### 6.2 角色预设
| 角色 | 权限 |
|-----|------|
| admin | 所有权限 (*) |
| business | 报价单/物料/费用/汇率/变更申请相关 |
| technician | 模块物料/费用查看 |
| viewer | 仅查看权限 |

---

## 7. 费用计算逻辑

### 7.1 费用系数
| 物料分类 | 说明 | 默认系数 |
|---------|------|---------|
| large | 大件 | 1.0 |
| normal | 普通件 | 1.0 |
| other | 其他件 | 1.0 |

### 7.2 税率选项
- 0% (免税)
- 3%
- 6%
- 13%
- 17%

### 7.3 计算公式
```
物料小计 = Σ(物料单价 × 数量)
物料小计(含系数) = Σ(物料小计 × 对应分类系数)
税额 = 物料小计(含系数) × 税率
最终报价 = 物料小计(含系数) + 税额
```

---

## 8. 定时任务

| 任务 | 周期 | 说明 |
|-----|------|------|
| 消息清理 | 每天 03:00 | 清理过期消息 |
| 员工同步 | 每天 00:00 | 从 SQL Server 同步员工数据 |
| 部门同步 | 每天 00:00 | 从 SQL Server 同步部门数据 |
| 职位同步 | 每天 00:00 | 从 SQL Server 同步职位数据 |

---

## 9. 目录结构

```
project-quote-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask 应用工厂
│   │   ├── config.py            # 配置管理
│   │   ├── models/              # 数据模型 (17个)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── quotation.py
│   │   │   ├── module.py
│   │   │   ├── material.py
│   │   │   ├── fee.py
│   │   │   ├── version.py
│   │   │   ├── fee_rate.py
│   │   │   ├── exchange_rate.py
│   │   │   ├── change_request.py
│   │   │   ├── message.py
│   │   │   ├── operation_log.py
│   │   │   ├── employee.py
│   │   │   ├── department.py
│   │   │   ├── position.py
│   │   │   └── organization.py
│   │   ├── routes/              # API 路由 (17个蓝图)
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── quotations.py
│   │   │   ├── modules.py
│   │   │   ├── materials.py
│   │   │   ├── fees.py
│   │   │   ├── versions.py
│   │   │   ├── users.py
│   │   │   ├── exports.py
│   │   │   ├── logs.py
│   │   │   ├── roles.py
│   │   │   ├── fee_rates.py
│   │   │   ├── exchange_rates.py
│   │   │   ├── module_participants.py
│   │   │   ├── sync.py
│   │   │   ├── change_requests.py
│   │   │   └── messages.py
│   │   ├── services/            # 业务逻辑
│   │   │   └── message_service.py
│   │   ├── utils/               # 工具函数
│   │   │   ├── logger.py
│   │   │   └── permissions.py
│   │   └── tasks/               # 定时任务
│   │       └── sync_task.py
│   ├── versions/                # 版本文件存储
│   ├── run.py                   # 启动入口
│   ├── init_db.py               # 数据库初始化
│   ├── requirements.txt         # Python 依赖
│   └── venv_new/                # 虚拟环境
│
├── frontend/
│   ├── src/
│   │   ├── api/                 # API 封装 (16个)
│   │   │   ├── index.js
│   │   │   ├── request.js
│   │   │   ├── auth.js
│   │   │   ├── quotations.js
│   │   │   ├── modules.js
│   │   │   ├── materials.js
│   │   │   ├── fees.js
│   │   │   ├── versions.js
│   │   │   ├── users.js
│   │   │   ├── roles.js
│   │   │   ├── logs.js
│   │   │   ├── messages.js
│   │   │   ├── change_requests.js
│   │   │   ├── fee_rates.js
│   │   │   ├── exchange_rates.js
│   │   │   └── module_participants.js
│   │   ├── components/         # 公共组件
│   │   │   ├── Layout.vue       # 页面布局
│   │   │   └── Sidebar.vue     # 侧边栏
│   │   ├── views/              # 页面视图 (17个)
│   │   │   ├── Login.vue
│   │   │   ├── Dashboard.vue
│   │   │   ├── Quotations.vue
│   │   │   ├── QuotationEdit.vue
│   │   │   ├── ChangeRequests.vue
│   │   │   ├── Materials.vue
│   │   │   ├── FeeTypes.vue
│   │   │   ├── Fees.vue
│   │   │   ├── FeeRatesConfig.vue
│   │   │   ├── ExchangeRatesConfig.vue
│   │   │   ├── Users.vue
│   │   │   ├── Roles.vue
│   │   │   ├── Logs.vue
│   │   │   ├── SystemSettings.vue
│   │   │   ├── ModuleAssignments.vue
│   │   │   └── Messages.vue
│   │   ├── stores/              # Pinia 状态
│   │   │   └── auth.js
│   │   ├── router/             # 路由配置
│   │   │   └── index.js
│   │   ├── composables/        # 组合式函数
│   │   │   └── usePermission.js
│   │   ├── utils/             # 工具函数
│   │   │   └── request.js
│   │   ├── styles/           # 样式文件
│   │   │   └── variables.css
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── SPEC.md                     # 本文档
└── README.md                   # 项目说明
```

---

## 10. 开发规范

### 10.1 API 返回格式
```json
// 成功
{ "success": true, "data": {...} }

// 列表
{ "success": true, "items": [...], "total": 100, "page": 1, "page_size": 20 }

// 错误
{ "success": false, "error": "错误信息" }
```

### 10.2 前端 API 模块规范
```javascript
// 统一使用对象导出模式
export const xxxAPI = {
  getList: (params) => request.get('/xxx', { params }),
  getById: (id) => request.get(`/xxx/${id}`),
  create: (data) => request.post('/xxx', data),
  update: (id, data) => request.put(`/xxx/${id}`, data),
  delete: (id) => request.delete(`/xxx/${id}`)
}
```

### 10.3 表格高度规范
```css
/* 全屏页面容器 */
.page-container {
  height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* 表格 */
.el-table {
  height: calc(-200px + 100vh);
}
```

---

## 11. V2.1 新增功能

### 11.1 运输包装费用（Tab A）

**业务层配置（系统管理员）**：
- 包装类型：纸箱、木箱、托盘
- 每类包装的单价（元/个）

**项目层填写**：
- 每类包装的使用数量（单元数量）
- 项目层不显示单价，只显示单元数量

**计算逻辑**：
```
包装小计 = Σ(包装类型单价 × 使用数量)
```

---

### 11.2 人员差旅人天费用（Tab B）

**统一差旅分类**（4类，复用于 Tab B 和 Tab C）：
- 国内出差
- 东南亚出差
- 欧洲出差
- 美国出差

**业务层配置（系统管理员）**：
- 每类出差的人天单价（元/人天）

**项目层填写**：
- 每类出差的出星人天数

**计算逻辑**：
```
差旅人天小计 = Σ(出差分类人天单价 × 出星人天数)
```

---

### 11.3 差旅人次费用（Tab C）

**统一差旅分类**（与 Tab B 相同，4类）：
- 国内出差
- 东南亚出差
- 欧洲出差
- 美国出差

**出行方式（项目填写）**：
- 飞机 / 高铁 / 开车

**项目层填写**（根据出行方式动态显示）：
| 出行方式 | 项目填写 | 业务填写 |
|---------|---------|---------|
| 飞机 | 人次 | 往返机票费用（单人）+ 签证费用（非国内需填） |
| 高铁 | 人次 | 高铁票往返单价（单人） |
| 开车 | 人次 | 单人次往返单价 |

**计算逻辑**：
```
人次小计 = Σ(人次 × 对应交通单价)
非国内小计 = Σ(人次 × 签证费用)  // 仅非国内出差
差旅人次总费用 = 人次小计 + 非国内小计
```

---

### 11.4 新增数据模型

| 模型 | 说明 | 主要字段 |
|-----|------|---------|
| PackingType | 包装类型 | id, name, unit_price |
| PackingEntry | 包装条目 | quotation_id, packing_type_id, quantity |
| TravelCategory | 差旅分类 | id, name, code |
| TravelDayRate | 差旅人天单价 | travel_category_id, unit_price |
| TravelPersonDays | 差旅人天条目 | quotation_id, travel_category_id, person_days |
| TravelMode | 出行方式 | id, name, code |
| TravelPersonTrip | 差旅人次条目 | quotation_id, travel_category_id, travel_mode_id, person_count |
| TravelPersonTripFee | 差旅人次费用 | quotation_id, travel_category_id, travel_mode_id, unit_price, visa_fee |

---

### 11.5 新增 API 接口

| 方法 | 路径 | 说明 |
|-----|------|------|
| GET | /api/packing-types | 获取包装类型 |
| POST | /api/packing-types | 创建包装类型 |
| PUT | /api/packing-types/:id | 更新包装类型 |
| DELETE | /api/packing-types/:id | 删除包装类型 |
| GET | /api/packing-entries | 获取包装条目 |
| POST | /api/packing-entries | 创建/更新包装条目 |
| PUT | /api/packing-entries/:id | 更新包装条目 |
| DELETE | /api/packing-entries/:id | 删除包装条目 |
| GET | /api/travel-categories | 获取差旅分类 |
| POST | /api/travel-categories | 创建差旅分类 |
| PUT | /api/travel-categories/:id | 更新差旅分类 |
| DELETE | /api/travel-categories/:id | 删除差旅分类 |
| GET | /api/travel-day-rates | 获取差旅人天单价 |
| PUT | /api/travel-day-rates | 更新差旅人天单价 |
| GET | /api/travel-person-days | 获取差旅人天条目 |
| POST | /api/travel-person-days | 创建/更新差旅人天条目 |
| PUT | /api/travel-person-days/:id | 更新差旅人天条目 |
| DELETE | /api/travel-person-days/:id | 删除差旅人天条目 |
| GET | /api/travel-modes | 获取出行方式 |
| POST | /api/travel-modes | 创建出行方式 |
| PUT | /api/travel-modes/:id | 更新出行方式 |
| DELETE | /api/travel-modes/:id | 删除出行方式 |
| GET | /api/travel-person-trips | 获取差旅人次条目 |
| POST | /api/travel-person-trips | 创建/更新差旅人次条目 |
| PUT | /api/travel-person-trips/:id | 更新差旅人次条目 |
| DELETE | /api/travel-person-trips/:id | 删除差旅人次条目 |
| GET | /api/travel-person-trip-fees | 获取差旅人次费用 |
| PUT | /api/travel-person-trip-fees | 更新差旅人次费用 |

---

### 11.6 报价单编辑页面 Tab 结构（V2.1）

```
报价单详情 (QuotationEdit.vue)
├── Tab 1: 基本信息
├── Tab 2: 模块管理
├── Tab 3: 物料清单
├── Tab 4: 运输包装费用（新增）
├── Tab 5: 人员差旅人天费用（新增）
├── Tab 6: 差旅人次费用（新增）
├── Tab 7: 版本管理
└── Tab 8: 汇总
```

---

### 11.7 权限说明

- **系统层配置**：业务管理员可编辑包装类型单价、差旅人天单价、差旅人次单价
- **项目层填写**：项目参与人可填写运输数量、人天数、人次
- **权限控制**：通过「分配项目报价单参与人员」Tab 控制，不按部门隔离

---

## 12. 待完成功能

| 优先级 | 功能 | 说明 |
|-------|------|------|
| P0 | 报价单导出 | Word/Excel/PDF 导出 |
| P0 | 版本对比 | 两个版本之间的差异对比 |
| P1 | 数据备份 | 数据库备份功能 |
| P1 | 导入功能 | 物料批量导入 |
| P2 | 邮件通知 | 变更申请邮件提醒 |
| P2 | 移动端适配 | 响应式布局优化 |
