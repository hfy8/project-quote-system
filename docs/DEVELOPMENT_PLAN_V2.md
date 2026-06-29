# 项目报价系统 V2.1 开发规划

> 规划周期：**2026 年 6 月 – 8 月中旬**（约 10 周）
> 当前基线：V2.0（生产运行）
> 目标版本：V2.1
> 核心理念：从零开始详细规划，报价核心模块优先，**部门级数据隔离 + 完整权限控制**贯穿全局

---

## 一、系统愿景与核心变革

### 1.1 现状问题
- 所有用户可见所有报价单（无部门隔离）
- 权限粗糙（admin 全能，普通用户仅按角色区分 view/edit）
- 部门数据完全共享，无法做部门业绩独立统计

### 1.2 V2.1 核心目标
**"部门自治 + 全栈权限"** — 每个部门只能操作本部门数据，部门内按角色分配细粒度权限。

```
┌──────────────────────────────────────────────────────┐
│                    V2.1 权限架构                       │
├──────────────┬───────────────────────────────────────┤
│ 维度          │ 说明                                 │
├──────────────┼───────────────────────────────────────┤
│ 部门隔离       │ 部门A用户 → 只能看/操作部门A的报价单   │
│ 角色分级       │ 部门经理(本部门全权) / 技术员 / 查看者 │
│ 功能权限       │ view / create / edit / delete / approve│
│ 跨部门协作     │ 部门经理可发起「跨部门协作申请」        │
│ 超级管理员     │ admin → 全局所有数据，不受部门限制      │
└──────────────┴───────────────────────────────────────┘
```

---

## 二、数据模型重构（部门隔离基础）

### 2.1 新增/变更模型

```python
# 新增：部门 (Department)
Department
├── id
├── name              # 部门名称
├── code              # 部门编码（如 "MECH", "ELEC"）
├── manager_id        # 部门经理 user_id
└── created_at

# 变更：User 新增字段
User
├── ...现有字段...
├── department_id     # 所属部门（FK）← 新增
└── is_cross_dept     # 是否可访问跨部门数据（bool）← 新增

# 变更：Quotation 新增字段
Quotation
├── ...现有字段...
├── department_id     # 所属部门（FK）← 新增
└── owner_dept_id      # 业务归属部门（FK）← 新增
```

### 2.2 部门隔离规则

| 场景 | 普通用户 | 部门经理 | 超级管理员 |
|------|---------|---------|-----------|
| 查看本部门报价单 | ✅ | ✅ | ✅ |
| 查看跨部门报价单 | ❌ | ❌（需协作申请） | ✅ |
| 新建报价单 | ✅（自动归属本部门） | ✅ | ✅ |
| 编辑本部门报价单 | ✅（有 edit 权限时） | ✅ | ✅ |
| 删除本部门报价单 | ❌ | ✅ | ✅ |
| 归档本部门报价单 | ❌ | ✅ | ✅ |
| 管理本部门用户 | ❌ | ✅（仅查看/角色分配） | ✅ |
| 系统级管理 | ❌ | ❌ | ✅ |

---

## 三、报价核心模块详细设计（Week 1-2）

### 3.1 模块结构总览

```
报价核心模块
├── 1.1 报价单管理（CRUD + 状态流转）
├── 1.2 模块管理（Module → 业务子项目）
├── 1.3 物料配置（原材料库 → 模块物料）
├── 1.4 费用配置（OtherFee / FeeType / FeeRate）
├── 1.5 金额计算引擎（含税/含系数/含利润）
├── 1.6 参与人权限（项目/机构/电气三类）
└── 1.7 部门数据隔离（贯穿所有接口）
```

### 3.2 Week 1：后端核心重构（部门隔离 + 报价单引擎）

#### 1.1 报价单管理

**数据模型变更：**
```
Quotation（变更）
├── department_id        # 必填，报价单归属部门
├── business_owner_id    # 业务负责人（user_id）
├── status: draft → in_progress → pending_approve → approved → archived
├── tax_rate             # 税率（0/3/6/13/17%）
├── profit_rate          # 利润率（默认 10%）
├── is_cross_dept        # 是否跨部门协作
├── cross_dept_note     # 跨部门说明
└── approved_by / approved_at
```

**API 变更（全部加 department 过滤）：**

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/quotations` | 列表（自动过滤：本部门或 admin 全量） | dept-filter |
| POST | `/api/quotations` | 创建（自动带 department_id） | quotation.create |
| GET | `/api/quotations/:id` | 详情（校验部门归属） | quotation.view |
| PUT | `/api/quotations/:id` | 更新（校验本部门 + edit 权限） | quotation.edit |
| DELETE | `/api/quotations/:id` | 删除（部门经理 + admin） | quotation.delete |
| PUT | `/api/quotations/:id/submit` | 提交审批（状态流转） | quotation.edit |
| PUT | `/api/quotations/:id/approve` | 审批通过 | quotation.approve |
| PUT | `/api/quotations/:id/reject` | 审批驳回 | quotation.approve |
| PUT | `/api/quotations/:id/archive` | 归档 | quotation.archive |

**部门隔离实现（伪码）：**
```python
def get_quotations(query, current_user):
    if current_user.is_admin:
        return query.all()  # admin 不受限制
    return query.filter(
        Quotation.department_id == current_user.department_id
    )
```

#### 1.2 模块管理（Module）

```
Module（不变，新增 department_link）
├── quotation_id         # 所属报价单
├── name                 # 模块名称
├── seq                  # 排序序号
├── business_lead_id     # 业务负责人
├── technician_lead_id   # 技术负责人
├── engineering_lead_id  # 工程负责人
├── status: active / inactive
└── department_id        # 从报价单继承（冗余字段，加速过滤）
```

**API：**

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/quotations/:qid/modules` | 列表 |
| POST | `/api/quotations/:qid/modules` | 创建 |
| GET | `/api/modules/:id` | 详情 |
| PUT | `/api/modules/:id` | 更新 |
| DELETE | `/api/modules/:id` | 删除 |
| PUT | `/api/modules/:id/participants` | 全量更新参与人 |

#### 1.3 物料配置

```
ModuleMaterial
├── module_id
├── material_id
├── quantity
├── seq                  # 排序
└── remark

Material（不变，已有）
├── code, name, unit, category, supplier, specification
└── department_id       # 物料归属部门（null = 全局物料）
```

**API（加 department 过滤）：**
- 部门私有物料：只给本部门用户可见
- 全局物料（department_id=null）：所有部门可见
- 创建/编辑/删除：校验 department_id 一致性

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/materials` | 列表（部门过滤） |
| POST | `/api/materials` | 创建（自动归属当前用户部门） |
| PUT/DELETE | `/api/materials/:id` | 编辑/删除 |

#### 1.4 费用配置

```
OtherFee
├── quotation_id
├── module_id            # 可选（模块级费用）
├── fee_type             # human/traffic/logistics/accommodation/other
├── location             # internal/external
├── amount               # 金额
├── currency             # 币种
├── remark
└── department_id        # 归属部门
```

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/fees?quotation_id=X` | 列表 |
| POST | `/api/fees` | 创建 |
| PUT/DELETE | `/api/fees/:id` | 编辑/删除 |

#### 1.5 金额计算引擎（核心）

```python
class QuotationCalculator:
    """报价单金额计算引擎"""

    def calc_material_subtotal(module_id):
        """物料小计 = Σ(物料单价 × 数量)"""
        items = ModuleMaterial.query.filter_by(module_id=module_id).all()
        return sum(m.material.unit_price * m.quantity for m in items)

    def calc_fee_rateAdjustment(subtotal, category):
        """分类系数调整 = 小计 × 分类系数（大件/普通/其他）"""
        rate = FeeRate.query.filter_by(category=category).first().rate
        return subtotal * rate

    def calc_tax(subtotal_with_rate, tax_rate):
        """税额 = (物料+系数调整) × 税率"""
        return subtotal_with_rate * tax_rate

    def calc_total(quotation_id):
        """报价单总价 = Σ(各模块含系数小计) + Σ(其他费用) + 税额"""
        # 含人力成本（Week 3 联动）
        ...

    def get_summary(quotation_id) -> dict:
        """返回完整汇总数据（供前端表格展示）"""
        return {
            "material_subtotal": Decimal,
            "fee_adjustment_total": Decimal,
            "labor_cost_total": Decimal,      # Week 3 新增
            "other_fee_total": Decimal,
            "tax_amount": Decimal,
            "grand_total": Decimal,
            "by_module": [{module_id, module_name, subtotal}, ...],
            "by_category": [{category, subtotal}, ...]
        }
```

**汇总 API：**
- `GET /api/quotations/:id/summary` → 返回上述完整结构

#### 1.6 参与人权限（ModuleParticipant）

```
ModuleParticipant
├── module_id
├── user_id
├── role_type: business_lead / technician_lead / engineering_lead / viewer
├── can_edit: bool
├── can_delete: bool
└── added_at / added_by
```

**权限矩阵：**

| 角色类型 | can_view | can_edit | can_delete |
|---------|----------|----------|-----------|
| business_lead | ✅ | ✅ | ❌ |
| technician_lead | ✅ | ✅ | ❌ |
| engineering_lead | ✅ | ✅ | ❌ |
| viewer | ✅ | ❌ | ❌ |

**API：**

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/modules/:id/participants` | 获取参与人列表 |
| POST | `/api/modules/:id/participants` | 添加参与人 |
| PUT | `/api/modules/:id/participants/:uid` | 更新参与人权限 |
| DELETE | `/api/modules/:id/participants/:uid` | 移除参与人 |

---

### 3.3 Week 2：前端核心重构（部门隔离 + 权限控制）

#### 前端架构变更

**路由守卫（department + permission 双重校验）：**
```javascript
// router.beforeEach
router.beforeEach((to, from) => {
  const { user } = useAuthStore()

  // 1. 登录校验
  if (!user && to.path !== '/login') return '/login'

  // 2. 部门隔离：普通用户访问非本部门资源 → 403 页
  if (to.meta.departmentId && user.department_id !== to.meta.departmentId && !user.is_admin) {
    return '/forbidden'
  }

  // 3. 权限校验
  const required = to.meta.permission  // 如 'quotation.create'
  if (required && !hasPermission(user, required)) {
    return '/forbidden'
  }
})
```

**报价单管理页面（`Quotations.vue`）：**
- 列表页：只展示当前用户部门数据（admin 展示全部）
- 新建报价单：自动带入当前用户 department_id
- 状态标签：草稿(灰) / 审批中(蓝) / 已通过(绿) / 已归档(金)
- 快捷操作：根据权限显示 编辑/删除/提交/审批 按钮
- 筛选器：状态 / 部门(仅 admin) / 日期范围 / 负责人

**新建/编辑报价单（`QuotationEdit.vue`）：**
```
├── 基本信息 Tab
│   ├── 报价单名称（必填）
│   ├── 业务负责人（下拉，选用户）
│   ├── 部门（自动带入，当前用户部门）
│   ├── 税率（下拉 0/3/6/13/17%）
│   ├── 利润率（默认 10%）
│   └── 备注
│
├── 模块 Tab（核心）
│   ├── 模块列表（可拖拽排序）
│   ├── 添加模块（名称 + 业务负责人 + 技术负责人）
│   ├── 展开模块 → 物料配置（从原材料库选择）
│   ├── 展开模块 → 参与人管理（添加/设权限）
│   └── 展开模块 → 其他费用（人力/物流/差旅/其他）
│
├── 汇总 Tab
│   ├── 物料小计（含分类系数）
│   ├── 其他费用合计
│   ├── 税额
│   ├── 利润率调整
│   └── 最终报价
│
└── 历史 Tab（版本列表）
```

**模块物料选择器（`MaterialSelector.vue`）：**
- 左侧：原材料库列表（按分类/供应商筛选）
- 右侧：已选物料列表（可编辑数量）
- 搜索：支持品名/规格/编码模糊搜索
- 分类展示：大件 / 核心部件 / 其他件（带分类标签）
- 部门标签：部门私有 / 全局物料 区分显示

**权限指令：**
```javascript
// v-permission="'quotation.edit'"
app.directive('permission', {
  mounted(el, binding) {
    if (!hasPermission(binding.value)) {
      el.style.display = 'none'  // 或 el.remove()
    }
  }
})
```

#### 交付物（Week 1-2）
- [ ] 部门隔离 API 中间件（department filter）
- [ ] 报价单 CRUD + 状态流转 API
- [ ] 金额计算引擎 API
- [ ] 模块管理 + 参与人权限 API
- [ ] 物料管理 API（部门过滤）
- [ ] 费用管理 API
- [ ] 前端路由守卫（部门 + 权限双重校验）
- [ ] 报价单列表页（部门过滤 + 权限按钮）
- [ ] 报价单编辑页（完整 Tab 页面）
- [ ] 物料选择器组件
- [ ] 汇总计算展示组件

---

## 四、版本管理域（Week 3）

### 4.1 版本快照增强

```python
VersionSnapshot
├── quotation_id
├── version_no           # 自动递增
├── snapshot_data        # JSON 完整快照
├── export_data          # JSON 脱敏导出数据（用于高效渲染）
├── created_by
├── created_at
└── remark
```

**自动生成时机：** 报价单每次「保存」+ 每次「提交审批」+ 每次「审批完成」

### 4.2 版本对比 API

```
GET /api/versions/<id>/compare?v1=X&v2=Y

Response:
{
  "v1": { version_no, created_at, created_by },
  "v2": { version_no, created_at, created_by },
  "changes": {
    "modules": [
      {
        "name": "模块A",
        "status": "modified",
        "fields": {
          "materials": [
            { "name": "物料X", "v1_qty": 10, "v2_qty": 15, "change": "+5" },
            { "name": "物料Y", "status": "added" }
          ]
        }
      }
    ],
    "fees": [...],
    "summary": { "v1_total": 10000, "v2_total": 12000, "delta": +2000 }
  }
}
```

### 4.3 多格式导出

| 格式 | 技术 | 内容 |
|------|------|------|
| PDF | reportlab | 封面 + 目录 + 完整报价（已实现 v2.0） |
| Word | python-docx | 含水印、版本号、审核状态 |
| Excel | openpyxl | 封面页 + 项目信息 + 物料明细（含分类小计）+ 费用汇总 + 人力成本 |

### 4.4 前端版本对比页

```
VersionCompare.vue
├── 版本选择器（v1 下拉 + v2 下拉，当前版本 vs 历史版本）
├── 变更汇总卡片（金额变化 + 物料变化统计）
├── 变更详情（可折叠，按模块展开）
│   ├── 物料变更（绿色新增 / 红色删除 / 橙色修改）
│   ├── 费用变更
│   └── 金额变化
└── 导出按钮组（PDF / Word / Excel，可选导出版本）
```

---

## 五、人力工时域（Week 4）

### 5.1 数据模型

```
LaborHour（工时记录）
├── id
├── module_id             # 关联模块
├── user_id              # 填报人
├── date                 # 工作日期
├── hours                # 工时数（小时）
├── work_content         # 工作内容
├── labor_type           # 工种（design/assembly/debugging/installation）
├── status               # draft/submitted/approved/rejected
└── created_at / updated_at

LaborHourRate（工时单价配置）
├── id
├── department_id         # 部门（支持部门差异化定价）
├── labor_type           # 工种
├── unit_price            # 单价（元/小时）
└── currency             # 币种
```

### 5.2 工时流程

```
填报人录入工时 → 提交（status=draft→submitted）→ 部门经理审批（approved/rejected）
                                      ↓
                         通过后自动写入 OtherFee（fee_type=human）
                                      ↓
                         联动更新报价单 summary.total
```

### 5.3 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/labor-hours?module_id=X` | 工时列表 |
| POST | `/api/labor-hours` | 录入工时 |
| PUT | `/api/labor-hours/:id` | 编辑工时（仅填报人，draft 状态） |
| DELETE | `/api/labor-hours/:id` | 删除（填报人，draft 状态） |
| PUT | `/api/labor-hours/:id/submit` | 提交审批 |
| PUT | `/api/labor-hours/:id/approve` | 审批通过（部门经理/admin） |
| GET | `/api/labor-hours/summary?module_id=X` | 工时汇总（总工时/总成本） |
| CRUD | `/api/labor-hour-rates` | 工时单价配置（admin） |

### 5.4 前端页面

| 页面 | 说明 |
|------|------|
| `LaborHours.vue` | 工时列表（日期范围 + 模块 + 人员筛选，部门过滤） |
| `LaborHoursEntry.vue` | 录入/编辑表单 |
| `LaborHourRates.vue` | 工时单价配置（admin） |
| `LaborHourReport.vue` | 报表（柱状：人员工时对比 / 折线：月度趋势） |
| `QuotationEdit.vue` 新增 Tab | 报价单内嵌「人力成本」Tab |

---

## 六、数据导入导出（Week 5）

### 6.1 物料批量导入

```
POST /api/materials/import
流程：上传 Excel → 服务端解析（openpyxl）→ 预览数据（返回前10行预览）→ 用户确认 → 批量写入
匹配规则：按 code（物料编码）精确匹配，存在则覆盖，不存在则新增
错误处理：返回错误行号 + 原因（品名不能为空 / 单价格式错误等）
```

**导入模板字段：** 编码, 品名, 规格, 单位, 类别, 单价, 供应商, 备注

### 6.2 报价单数据导入

支持 Excel 整单导入（创建新报价单），包含：基本信息 + 模块列表 + 物料明细

### 6.3 数据备份

```
POST /api/admin/backup → 触发 pg_dump → 返回下载链接（保留最近7份）
备份内容：全量数据（不含 operation_log）
```

---

## 七、统计报表（Week 6）

### 7.1 报表类型

| 报表 | 图表 | 说明 |
|------|------|------|
| 报价金额趋势 | 折线图 | 按月/季度统计已归档报价单总金额 |
| 部门业绩对比 | 柱状图 | 各部门报价单数量 + 总金额对比 |
| 模块成本分布 | 饼图 | 物料/人力/物流/差旅占比 |
| 人员工时统计 | 柱状图 | 每人总工时 / 有效工时 |
| 报价周期分析 | 折线图 | 创建→归档平均天数（按月） |

### 7.2 筛选器（统一）
- 日期范围（默认本月）
- 部门（仅 admin 可选全部，普通用户仅本部门）
- 负责人
- 报价单状态

---

## 八、系统设置与审批流程（Week 7）

### 8.1 审批流程配置

```
ApprovalFlow（审批流程）
├── id
├── name                 # 流程名称（如"标准项目报价审批"）
├── quotation_type       # 报价单类型（standard/project/spare）
├── steps                # JSON 数组：[ {step:1, role:"dept_manager", approvers:[]}, ... ]
└── is_active

Example steps:
[
  { "step": 1, "role": "dept_manager", "name": "部门经理审批" },
  { "step": 2, "role": "finance", "name": "财务复核" },
  { "step": 3, "role": "general_manager", "name": "总经理审批" }
]
```

### 8.2 部门管理

```
Department（不变，CRUD admin）
├── name, code, manager_id, parent_id（支持多级部门）
└── display_order
```

### 8.3 系统参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| default_tax_rate | 默认税率 | 13% |
| default_profit_rate | 默认利润率 | 10% |
| max_export_file_size | 导出文件大小上限 | 50MB |
| labor_hour_reminder_days | 工时补录提醒（天） | 7 |

### 8.4 消息通知（内置）

- 状态变更时自动发站内消息（已实现 v2.0）
- 审批节点变更时通知下一审批人

---

## 九、消息增强（Week 8）

### 9.1 邮件通知

```
SMTP 配置（系统设置页配置）
├── SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
├── from_name（发件人昵称）
└── use_tls

触发场景：
- 报价单审批通过 → 申请人 + 业务负责人（邮件 + 站内消息）
- 报价单审批驳回 → 申请人（邮件 + 站内消息）
- 工时提交待审批 → 部门经理（邮件 + 站内消息）
```

### 9.2 钉钉/企业微信 Webhook

```
Webhook 配置（系统设置页）
├── webhook_url
├── secret（签名密钥）
└── enabled（开关）

推送内容：卡片式消息（标题 + 摘要 + 操作按钮链接）
```

---

## 十、国际化（Week 8-9）

### 10.1 前端 i18n

- vue-i18n，所有中文标签替换为 i18n key
- 新增 `locales/zh.json` + `locales/en.json`
- 登录页 + Header 语言切换按钮（🌐 图标）
- 记住用户语言偏好（localStorage）

### 10.2 后端 API i18n

```
?name=报价单&lang=zh
?name=Quotation&lang=en
```

- 导出接口（PDF/Word/Excel）支持 `?lang=zh|en`
- 后端数据库 `name_en` 字段 fallback 到 `name`
- 关键字段：`exports.py` 中已有 `I18N_MAP` + `t(key, lang)` 函数，扩展覆盖

---

## 十一、技术债务（全程并行）

| # | 事项 | 说明 |
|---|------|------|
| T1 | 数据库索引 | `quotations.department_id`, `modules.quotation_id`, `operation_logs.created_at` 加索引 |
| T2 | 统一错误处理 | 全局 `@bp.errorhandler`，统一返回 `{success, error}` |
| T3 | JWT 续期 | AccessToken 15min + RefreshToken 7d，401 时前端自动刷新 |
| T4 | 请求限流 | 登录 5 次/分钟，导出 3 次/分钟 |
| T5 | Docker 多阶段构建 | 目标镜像 < 500MB |
| T6 | API 文档 | Flasgger / OpenAPI 3.0 |

---

## 十二、10 周开发周期总览

```
功能                    │ W1  │ W2  │ W3  │ W4  │ W5  │ W6  │ W7  │ W8  │ W9  │ W10 │
───────────────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───── │
1.报价核心模块           │     │     │     │     │     │     │     │     │     │      │
  1.1 部门数据模型重构    │ ██  │     │     │     │     │     │     │     │     │      │
  1.2 报价单API+状态流转  │ ██  │     │     │     │     │     │     │     │     │      │
  1.3 金额计算引擎       │ ██  │     │     │     │     │     │     │     │     │      │
  1.4 模块+参与人API     │ ██  │     │     │     │     │     │     │     │     │      │
  1.5 前端报价单管理页    │     │ ██  │     │     │     │     │     │     │     │      │
  1.6 前端编辑页+物料选择  │     │ ██  │     │     │     │     │     │     │     │      │
  1.7 路由守卫+权限指令   │     │ ██  │     │     │     │     │     │     │     │      │
───────────────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───── │
2.版本管理域             │     │     │     │     │     │     │     │     │     │      │
  2.1 版本快照+对比API   │     │     │ ██  │     │     │     │     │     │     │      │
  2.2 Word/Excel导出    │     │     │ ██  │     │     │     │     │     │     │      │
  2.3 前端版本对比页     │     │     │ ██  │     │     │     │     │     │     │      │
───────────────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───── │
3.人力工时域             │     │     │     │     │     │     │     │     │     │      │
  3.1 工时API+审批流     │     │     │     │ ██  │     │     │     │     │     │      │
  3.2 工时前端页面        │     │     │     │ ██  │     │     │     │     │     │      │
  3.3 联动报价单成本     │     │     │     │ ██  │     │     │     │     │     │      │
───────────────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───── │
4.数据导入导出           │     │     │     │     │     │     │     │     │     │      │
  4.1 物料批量导入       │     │     │     │     │ ██  │     │     │     │     │      │
  4.2 报价单导入         │     │     │     │     │ ██  │     │     │     │     │      │
  4.3 数据备份           │     │     │     │     │ ██  │     │     │     │     │      │
───────────────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───── │
5.统计报表               │     │     │     │     │     │     │     │     │     │      │
  5.1 报表API            │     │     │     │     │     │ ██  │     │     │     │      │
  5.2 图表前端页          │     │     │     │     │     │ ██  │     │     │     │      │
───────────────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───── │
6.系统设置+审批          │     │     │     │     │     │     │     │     │     │      │
  6.1 审批流程配置API    │     │     │     │     │     │     │ ██  │     │     │      │
  6.2 前端审批配置页      │     │     │     │     │     │     │ ██  │     │     │      │
  6.3 部门+系统参数      │     │     │     │     │     │     │ ██  │     │     │      │
───────────────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───── │
7.消息增强               │     │     │     │     │     │     │     │     │     │      │
  7.1 邮件通知           │     │     │     │     │     │     │     │ ██  │     │      │
  7.2 钉钉Webhook       │     │     │     │     │     │     │     │ ██  │     │      │
───────────────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───── │
8.国际化                 │     │     │     │     │     │     │     │ ██  │ ██  │      │
  8.1 前端i18n           │     │     │     │     │     │     │     │ ██  │     │      │
  8.2 后端API双语        │     │     │     │     │     │     │     │     │ ██  │      │
───────────────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───── │
9.技术债务               │ ◑   │ ◑   │ ◑   │ ◑   │ ◑   │ ◑   │ ◑   │ ◑   │ ◑   │  ◑   │
10.测试+部署             │     │     │     │     │     │     │     │     │     │ ██  │
```

> ██ = 主要开发　◑ = 并行推进

---

## 十三、里程碑

| 里程碑 | 周次 | 交付内容 |
|--------|------|---------|
| **M0** | Week 2 末 | 报价核心模块重构完成，部门隔离 + 权限控制上线 |
| M1 | Week 3 末 | 版本对比 + Word/Excel 导出完成 |
| M2 | Week 4 末 | 人力工时管理（含审批流 + 联动报价单）完成 |
| M3 | Week 5 末 | 数据批量导入 + 备份完成 |
| M4 | Week 6 末 | 统计报表（5类）完成 |
| M5 | Week 7 末 | 审批流程配置 + 系统参数完成 |
| M6 | Week 8 末 | 邮件/钉钉消息增强完成 |
| M7 | Week 9 末 | 国际化（中英双语）完成 |
| M8 | Week 10 末 | 全量测试通过，V2.1 正式上线 |

---

## 十四、风险与对策

| 风险 | 影响 | 对策 |
|------|------|------|
| 部门隔离改造影响现有数据 | 高 | Week 1 先做数据迁移脚本（给现有报价单打 department_id） |
| 审批流程配置复杂 | 高 | Week 7 先确认审批流 DSL 设计，再开发 |
| 报表查询慢影响主业务 | 中 | 报表走只读库或定时生成统计表 |
| 国际化翻译质量 | 中 | 机器翻译 + 人工 Review 关键字段 |
| 测试覆盖不足 | 高 | Week 10 核心路径 100% 覆盖，API 用 Postman 批量测试 |
