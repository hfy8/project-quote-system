# 项目报价系统 - 技术规格说明书

## 1. 项目概述

### 1.1 项目信息
- **项目名称**: 项目报价管理系统
- **版本**: V1.0
- **开发周期**: 10周
- **项目类型**: 单机 + 线体两种类型

### 1.2 核心业务流程
```
创建报价单 → 创建模块 → 从原材料库选入物料 → 配置其他费用 → 生成报价单 → 导出
```

### 1.3 技术栈
- **前端**: Vue3 + Element Plus + Vite
- **后端**: Python Flask + SQLAlchemy
- **数据库**: SQLite (开发) / MySQL (生产)
- **导出**: python-docx, openpyxl, reportlab

---

## 2. 数据库设计

### 2.1 ER关系图
```
用户 ────< 报价单 >──── 方案号
          │
          ├────< 模块 >────< 模块物料 >──── 原材料
          │
          ├────< 其他费用 >
          │
          └────< 版本快照 >

原材料库（独立）: 大件 / 普通件 / 其他件
```

### 2.2 数据模型

#### 用户表 (users)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 用户ID |
| username | VARCHAR(50) | 用户名 |
| password_hash | VARCHAR(255) | 密码哈希 |
| real_name | VARCHAR(50) | 真实姓名 |
| role | VARCHAR(20) | admin/business |
| created_at | DATETIME | 创建时间 |

#### 报价单表 (quotations)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 报价单ID |
| name | VARCHAR(100) | 项目名称 |
| type | VARCHAR(20) | single/line |
| scheme_no | VARCHAR(50) | 方案号 |
| status | VARCHAR(20) | draft/in_progress/completed/archived |
| business_owner_id | INTEGER FK | 业务负责人 |
| creator_id | INTEGER FK | 创建人 |
| tax_rate | FLOAT | 税率（默认0.13） |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### 模块表 (modules)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 模块ID |
| quotation_id | INTEGER FK | 报价单ID |
| name | VARCHAR(100) | 模块名称 |
| code | VARCHAR(50) | 模块编号 |
| description | TEXT | 模块描述 |
| created_at | DATETIME | 创建时间 |

#### 模块参与人员表 (module_participants)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | ID |
| module_id | INTEGER FK | 模块ID |
| user_id | INTEGER FK | 用户ID |

#### 原材料表 (materials)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | 物料ID |
| name | VARCHAR(100) | 品名 |
| spec | VARCHAR(100) | 规格型号 |
| brand | VARCHAR(50) | 品牌 |
| unit | VARCHAR(20) | 单位 |
| unit_price | DECIMAL(10,2) | 单价 |
| category | VARCHAR(20) | 大件/普通件/其他件 |
| status | VARCHAR(20) | active/inactive |
| created_at | DATETIME | 创建时间 |

#### 模块物料表 (module_materials)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | ID |
| module_id | INTEGER FK | 模块ID |
| material_id | INTEGER FK | 物料ID |
| quantity | INTEGER | 数量 |
| selected_by_id | INTEGER FK | 添加人 |
| created_at | DATETIME | 创建时间 |

#### 其他费用表 (other_fees)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | ID |
| quotation_id | INTEGER FK | 报价单ID |
| module_id | INTEGER FK | 模块ID(可空) |
| fee_type | VARCHAR(50) | 费用类型 |
| location | VARCHAR(20) | 厂内/厂外 |
| amount | DECIMAL(10,2) | 金额 |
| description | TEXT | 说明 |
| created_at | DATETIME | 创建时间 |

#### 费用类型配置表 (fee_types)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | ID |
| name | VARCHAR(50) | 费用类型名称 |
| location | VARCHAR(20) | 厂内/厂外 |
| is_active | BOOLEAN | 是否启用 |
| created_at | DATETIME | 创建时间 |

#### 版本快照表 (version_snapshots)
| 字段 |类型 | 说明 |
|------|------|------|
| id | INTEGER PK | ID |
| quotation_id | INTEGER FK | 报价单ID |
| version_no | INTEGER | 版本号 |
| snapshot_data | TEXT | JSON快照数据 |
| operation_type | VARCHAR(20) | 操作类型 |
| remark | TEXT | 备注 |
| operator_id | INTEGER FK | 操作人 |
| created_at | DATETIME | 创建时间 |

#### 费用系数配置表 (fee_rates)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | ID |
| category | VARCHAR(50) | 物料分类（大件/普通件/其他件） |
| rate | FLOAT | 费用系数 |
| description | VARCHAR(200) | 描述 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

#### 汇率配置表 (exchange_rates)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | ID |
| currency | VARCHAR(20) | 货币代码（CNY/USD/EUR） |
| rate | FLOAT | 汇率（相对于基准货币） |
| is_base | BOOLEAN | 是否为基准货币 |
| description | VARCHAR(200) | 描述 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## 3. API接口设计

### 3.1 认证接口
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/logout` - 用户登出
- `GET /api/auth/me` - 获取当前用户信息

### 3.2 报价单接口
- `GET /api/quotations` - 获取报价单列表
- `POST /api/quotations` - 创建报价单
- `GET /api/quotations/:id` - 获取报价单详情
- `PUT /api/quotations/:id` - 更新报价单
- `DELETE /api/quotations/:id` - 删除报价单
- `POST /api/quotations/:id/copy` - 复制报价单
- `PUT /api/quotations/:id/status` - 更新状态
- `GET /api/quotations/:id/participants` - 获取参与人员
- `POST /api/quotations/:id/participants` - 添加参与人员
- `DELETE /api/quotations/:id/participants/:uid` - 移除参与人员

### 3.3 汇总视图接口
- `GET /api/quotations/:id/summary` - 获取报价单汇总数据（含费用系数、税率计算）

### 3.4 费用系数接口
- `GET /api/fee_rates` - 获取所有费用系数
- `POST /api/fee_rates` - 创建费用系数
- `PUT /api/fee_rates/:id` - 更新费用系数
- `DELETE /api/fee_rates/:id` - 删除费用系数
- `GET /api/fee_rates/category/:category` - 按分类获取费用系数

### 3.5 汇率接口
- `GET /api/exchange_rates` - 获取所有汇率
- `POST /api/exchange_rates` - 创建汇率
- `PUT /api/exchange_rates/:id` - 更新汇率
- `DELETE /api/exchange_rates/:id` - 删除汇率
- `GET /api/exchange_rates/convert` - 货币转换

### 3.6 模块接口
- `GET /api/quotations/:qid/modules` - 获取模块列表
- `POST /api/quotations/:qid/modules` - 创建模块
- `PUT /api/modules/:id` - 更新模块
- `DELETE /api/modules/:id` - 删除模块
- `GET /api/modules/:id` - 获取模块详情
- `GET /api/modules/:id/summary` - 获取模块物料汇总

### 3.6.1 模块参与人员接口
- `GET /api/modules/:id/participants` - 获取模块参与人员
- `POST /api/modules/:id/participants` - 添加模块参与人员
- `DELETE /api/modules/:id/participants/:pid` - 移除模块参与人员

### 3.7 原材料库接口
- `GET /api/materials` - 获取物料列表
- `POST /api/materials` - 创建物料
- `PUT /api/materials/:id` - 更新物料
- `DELETE /api/materials/:id` - 删除物料
- `POST /api/materials/import` - 批量导入物料
- `PUT /api/materials/:id/toggle` - 启用/禁用物料

### 3.8 物料选入接口
- `GET /api/modules/:mid/materials` - 获取模块物料列表
- `POST /api/modules/:mid/materials` - 添加物料到模块
- `PUT /api/module_materials/:id` - 更新模块物料
- `DELETE /api/module_materials/:id` - 从模块移除物料

### 3.9 其他费用接口
- `GET /api/quotations/:qid/fees` - 获取费用列表
- `POST /api/quotations/:qid/fees` - 添加费用
- `PUT /api/fees/:id` - 更新费用
- `DELETE /api/fees/:id` - 删除费用
- `GET /api/fee-types` - 获取费用类型配置
- `POST /api/fee-types` - 创建费用类型
- `PUT /api/fee-types/:id` - 更新费用类型

### 3.10 版本接口
- `GET /api/quotations/:qid/versions` - 获取版本列表
- `POST /api/quotations/:qid/versions` - 创建版本快照
- `GET /api/versions/:id` - 获取版本详情
- `POST /api/versions/:id/rollback` - 回退到指定版本
- `GET /api/versions/:id/compare/:other_id` - 对比两个版本

### 3.11 导出接口
- `GET /api/quotations/:id/export/word` - 导出Word
- `GET /api/quotations/:id/export/excel` - 导出Excel
- `GET /api/quotations/:id/export/pdf` - 导出PDF

### 3.12 系统管理接口
- `GET /api/users` - 获取用户列表
- `POST /api/users` - 创建用户
- `PUT /api/users/:id` - 更新用户
- `DELETE /api/users/:id` - 删除用户
- `GET /api/roles` - 获取角色列表
- `POST /api/roles` - 创建角色
- `PUT /api/roles/:id` - 更新角色
- `GET /api/permissions` - 获取权限列表
- `GET /api/logs` - 获取操作日志

---

## 4. 前端页面结构

```
/login                 - 登录页
/dashboard             - 工作台/首页
/quotations            - 报价单列表
/quotations/new        - 新建报价单
/quotations/:id        - 报价单详情
/materials             - 原材料库
/fee-types             - 费用类型配置
/fees                  - 费用管理
/fee-rates             - 费用系数配置（大件/普通件/其他件系数）
/exchange-rates        - 汇率配置（货币转换）
/users                 - 用户管理
/roles                 - 角色管理
/logs                  - 操作日志
```

## 5. 汇总计算逻辑

### 5.1 费用系数计算
- 物料按分类（大件/普通件/其他件）应用不同的费用系数
- 费用系数在 `/fee-rates` 页面配置
- 物料小计(含系数) = 物料小计 × 对应分类的系数

### 5.2 税率计算
- 报价单可配置税率（0%/3%/6%/13%/17%）
- 税额 = 小计(含系数) × 税率
- 最终报价 = 小计(含系数) + 税额

### 5.3 汇率转换
- 基准货币默认为 CNY（人民币）
- 可在 `/exchange-rates` 配置多种货币汇率
- 支持货币转换计算

---

## 6. 开发优先级

### P0 (必须完成 - 10周内)
1. 用户认证 + 基础框架
2. 报价单管理（CRUD + 状态流转）
3. 原材料库管理
4. 模块管理
5. 物料选入
6. 其他费用
7. 报价单导出
8. 历史版本
9. 汇总视图（线体）
10. 系统管理（用户/角色/权限）

### P1 (重要 - 可延后)
- 操作日志
- 数据备份

### P2 (增强 - 上线后迭代)
- 消息通知
- 审批流程

---

## 7. 目录结构

```
project-quote-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   └── utils/
│   ├── migrations/
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   ├── stores/
│   │   └── utils/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── docs/
└── README.md
```
