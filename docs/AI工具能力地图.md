# AI 工具能力地图

> 项目报价系统 AI 助手支持的工具清单（共 33 个）
> 更新日期：2026-06-16

## 快速分类

| 类别 | 工具数 | 代表工具 |
|---|---|---|
| 🔍 报价单查询 | 5 | list_quotations_v2 / get_quotation_full / get_quotation_summary |
| 📦 物料库 | 3 | search_materials_v2 / list_material_categories / list_materials(原始) |
| 💰 费用/差旅 | 3 | get_quotation_fees / get_quotation_travel_cost |
| 👤 人员/组织 | 3 | find_user / list_org_structure / who_can_approve |
| 📚 知识库 | 5 | search_knowledge / search_knowledge_hybrid / add_knowledge / list_knowledge / delete_knowledge |
| 📊 分析/审计 | 7 | analyze_profitability / audit_quotation / estimate_labor_hours |
| ⚙️ 工作流 | 4 | list_pending_tasks / update_quotation_status / export_quotation |
| 📜 其他 | 3 | list_my_conversations / get_knowledge_stats / upsert_knowledge_embedding |

## 完整清单

### 🔍 报价单

| 工具 | 功能 | 读/写 | 需要权限 |
|---|---|---|---|
| `list_quotations_v2` | 多条件查报价单（status/type/keyword） | 读 | — |
| `get_quotation_full` | 一次返回完整详情（模块+物料+费用+差旅） | 读 | — |
| `get_quotation_summary` | 报价单摘要（原始版） | 读 | — |
| `list_modules` | 模块列表 | 读 | — |
| `calculate_quotation_cost` | 成本计算 | 读 | — |
| `update_quotation_status` | 改状态（draft↔approved） | 写 | quotation.edit |
| `export_quotation` | 生成导出下载链接（word/excel/pdf） | 读 | — |

### 📦 物料

| 工具 | 功能 | 读/写 | 需要权限 |
|---|---|---|---|
| `search_materials_v2` | 物料多维搜索（关键词/分类/价格区间） | 读 | — |
| `list_material_categories` | 物料分类+数量 | 读 | — |
| `search_materials` | 物料搜索（原始版） | 读 | — |
| `recommend_materials_for_module` | 模块物料推荐 | 读 | — |

### 💰 费用/差旅

| 工具 | 功能 | 读/写 |
|---|---|---|
| `get_quotation_fees` | 其他费用明细+按类型汇总 | 读 |
| `get_quotation_travel_cost` | 差旅费明细+总额（人/次+人/天） | 读 |
| `estimate_labor_hours` | 工时估算 | 读 |

### 👤 人员/组织

| 工具 | 功能 | 读/写 |
|---|---|---|
| `find_user` | 搜索用户（username/real_name） | 读 |
| `list_org_structure` | 部门树+员工数 | 读 |
| `who_can_approve` | 权限查询（谁能审批/编辑/删除） | 读 |

### 📚 知识库

| 工具 | 功能 | 读/写 | 需要权限 |
|---|---|---|---|
| `search_knowledge` | 关键词匹配搜索 | 读 | — |
| `search_knowledge_hybrid` | 混合搜索（关键词+向量） | 读 | — |
| `add_knowledge` | 添加知识文档 | 写 | system.edit |
| `list_knowledge` | 列出知识库文档（按类型过滤） | 读 | — |
| `delete_knowledge` | 删除知识文档 | 写 | system.edit |
| `get_knowledge_stats` | 知识库统计 | 读 | — |
| `upsert_knowledge_embedding` | 重算 embedding | 写 | system.edit |

### 📊 分析/审计

| 工具 | 功能 | 读/写 |
|---|---|---|
| `analyze_profitability` | 毛利率分析 | 读 |
| `analyze_trends` | 趋势分析 | 读 |
| `get_quotation_compare` | 报价单对比 | 读 |
| `simulate_quotation_change` | 降价模拟 | 读 |
| `audit_quotation` | 报价单审计 | 读 |
| `audit_materials_price` | 物料价格审计 | 读 |
| `audit_labor_hours` | 工时审计 | 读 |

### ⚙️ 工作流

| 工具 | 功能 | 读/写 |
|---|---|---|
| `list_pending_tasks` | 待办汇总（待审批/变更/总数） | 读 |
| `export_quotation` | 导出下载链接 | 读 |

### 📜 其他

| 工具 | 功能 | 读/写 |
|---|---|---|
| `list_my_conversations` | 历史对话列表（内存存储） | 读 |
| `get_knowledge_stats` | 知识库统计信息 | 读 |
| `upsert_knowledge_embedding` | 嵌入更新 | 写 |

## 用户角色能力对照

| 工具 | admin | business | purchaser | viewer |
|---|---|---|---|---|
| 所有读工具 | ✅ | ✅ | ✅ | ✅ |
| `update_quotation_status` | ✅ | ✅ quotation.edit | ❌ | ❌ |
| `add_knowledge` | ✅ | ❌ | ❌ | ❌ |
| `delete_knowledge` | ✅ | ❌ | ❌ | ❌ |

> admin 为超级管理员，放行所有操作
> business（业务员）有 quotation.edit → 能改报价单状态
> viewer（普通用户）只能读，写操作被拒绝

## 写操作权限校验流程

```
用户提问 → LLM 决策调工具 → execute_tool(tool_name, args, user_id)
                                     │
                           ┌─────────┴─────────┐
                           │ 工具在 TOOL_PERMISSIONS 中? │
                           └─────────┬─────────┘
                                     │
                      ┌──────YES─────┴────NO──────┐
                      │                          │
              ┌───────┴───────┐            直接执行
              │ 校验权限       │           （只读工具）
              │ admin → 放行  │
              │ role → 查权限 │
              └───────┬───────┘
                      │
            ┌─────通过──┴───不通过─────┐
            │                          │
       执行 + 记日志             返回 error JSON
        (success=True)           + 记失败日志
                                 (success=False)
```
