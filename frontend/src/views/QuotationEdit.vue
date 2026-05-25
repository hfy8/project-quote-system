<template>
  <div class="quotation-edit">
    <!-- 页面标题栏 -->
    <div class="page-header">
      <div class="page-header-left">
        <button class="back-btn" @click="goBack">←</button>
        <h1 class="page-title">{{ isEdit ? '编辑报价单' : '新建报价单' }}</h1>
        <span v-if="isEdit && quotation.name" class="page-title-sub">- {{ quotation.name }}</span>
      </div>
    </div>

    <!-- 主内容卡片 -->
    <div class="edit-card">
      <el-tabs v-model="activeTab">
        <!-- 基本信息 -->
        <el-tab-pane label="基本信息" name="basic">
          <el-form :model="quotation" :rules="formRules" label-width="120px">
            <el-form-item label="报价单名称">
              <el-input v-model="quotation.name" placeholder="请输入报价单名称" :disabled="isEdit" />
            </el-form-item>
            <el-form-item label="项目类型">
              <el-select v-model="quotation.type" placeholder="请选择类型" :disabled="isEdit">
                <el-option label="单机 (single)" value="single" />
                <el-option label="线体 (line)" value="line" />
              </el-select>
            </el-form-item>
            <el-form-item label="方案编号" prop="scheme_no">
              <el-input v-model="quotation.scheme_no" placeholder="请输入方案编号" :disabled="isEdit" />
            </el-form-item>
            <el-form-item label="状态">
              <el-select v-model="quotation.status" placeholder="请选择状态" :disabled="isEdit">
                <el-option label="草稿" value="draft" />
                <el-option label="已提交" value="submitted" />
                <el-option label="已批准" value="approved" />
                <el-option label="已拒绝" value="rejected" />
              </el-select>
            </el-form-item>
            <el-form-item label="业务负责人">
              <span v-if="isEdit && quotation.business_owner_name">{{ quotation.business_owner_name }}</span>
              <el-select v-else v-model="quotation.business_owner_id" placeholder="请选择业务负责人">
                <el-option
                  v-for="user in businessUsers"
                  :key="user.id"
                  :label="user.real_name"
                  :value="user.id"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="币种">
              <el-select v-model="quotation.currency" placeholder="请选择币种" :disabled="isEdit">
                <el-option v-for="opt in currencyOptions" :key="opt.value" :label="opt.label" :value="opt.value" />
              </el-select>
            </el-form-item>
            <el-form-item label="税率">
              <el-select v-model="quotation.tax_rate" placeholder="请选择税率" :disabled="isEdit">
                <el-option label="不含税 (0%)" :value="0" />
                <el-option label="3%" :value="0.03" />
                <el-option label="6%" :value="0.06" />
                <el-option label="13%" :value="0.13" />
                <el-option label="17%" :value="0.17" />
              </el-select>
            </el-form-item>
            <el-form-item label="对外利润率">
              <el-input-number
                v-model="quotation.profit_rate"
                :precision="2" :step="0.01" :min="0" :max="10"
                placeholder="如 0.15 表示 15%"
                @change="isEdit && saveProfitRate()"
              />
            </el-form-item>
            <el-form-item v-if="!isEdit">
              <el-button type="primary" @click="saveBasic">创建报价单</el-button>
            </el-form-item>
            <el-form-item v-else>
              <el-alert title="基本信息已保存，无法修改" type="info" :closable="false" show-icon />
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <!-- 模块管理 -->
        <el-tab-pane v-if="isEdit" label="模块管理" name="modules">
          <div class="module-actions">
            <el-button type="primary" @click="showAddModule">添加模块</el-button>
          </div>

          <el-table :data="modules" border style="width: 100%; margin-top: 16px;">
            <el-table-column prop="name" label="模块名称" />
            <el-table-column prop="name_en" label="英文名称" />
            <el-table-column prop="description" label="描述" />
            <el-table-column label="操作" width="180">
              <template #default="{ row }">
                <el-button size="small" @click="editModule(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteModule(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 添加/编辑模块弹窗 -->
          <el-dialog v-model="moduleDialogVisible" :title="moduleDialogTitle" width="500px">
            <el-form :model="moduleForm" label-width="100px">
              <el-form-item label="模块名称">
                <el-input v-model="moduleForm.name" placeholder="请输入模块名称" />
              </el-form-item>
              <el-form-item label="英文名称">
                <el-input v-model="moduleForm.name_en" placeholder="English name (optional)" />
              </el-form-item>
              <el-form-item label="描述">
                <el-input v-model="moduleForm.description" type="textarea" rows="3" placeholder="请输入描述" />
              </el-form-item>
            </el-form>
            <template #footer>
              <el-button @click="moduleDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="saveModule">确定</el-button>
            </template>
          </el-dialog>
        </el-tab-pane>

        <!-- 参与人员 -->
        <el-tab-pane v-if="isEdit" label="参与人员" name="participants">
          <div class="participant-actions">
            <el-button type="primary" @click="showAddParticipantDialog">+ 添加人员</el-button>
          </div>

          <el-table :data="quotationParticipants" border style="width: 100%; margin-top: 16px;">
            <el-table-column prop="user.real_name" label="姓名" />
            <el-table-column prop="user.username" label="用户名" />
            <el-table-column label="参与类型" width="150">
              <template #default="{ row }">
                <el-select v-model="row.participant_type" placeholder="选择类型" size="small" @change="updateParticipantType(row)">
                  <el-option v-for="t in participantTypes" :key="t.type" :label="t.type_name + ' (' + t.type + ')'" :value="t.type" />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100" align="center">
              <template #default="{ row }">
                <el-button size="small" type="danger" @click="removeQuotationParticipant(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 添加人员弹窗 -->
          <el-dialog v-model="addParticipantDialogVisible" title="添加人员" width="500px">
            <div class="add-participant-form">
              <el-input v-model="participantSearch" placeholder="搜索人员姓名或用户名" clearable style="width: 100%; margin-bottom: 16px;" />
              <el-table :data="filteredAvailableUsers" v-loading="participantLoading" border size="small" max-height="300" @selection-change="handleParticipantSelection">
                <el-table-column type="selection" width="50" :selectable="checkParticipantSelectable"></el-table-column>
                <el-table-column prop="real_name" label="姓名" />
                <el-table-column prop="username" label="用户名" />
              </el-table>
            </div>
            <template #footer>
              <el-button @click="addParticipantDialogVisible = false">取消</el-button>
              <el-button type="primary" :disabled="!selectedParticipantUsers.length" @click="addParticipantsConfirm">添加 ({{ selectedParticipantUsers.length }})</el-button>
            </template>
          </el-dialog>
        </el-tab-pane>

        <!-- 费用系数 -->
        <el-tab-pane v-if="isEdit" label="费用系数" name="coefficients">
          <div class="coefficient-card">
            <div class="coefficient-header">
              <div class="coefficient-title">
                <span>费用系数配置</span>
              </div>
              <div class="coefficient-actions">
                <el-button size="small" @click="resetCoefficientsToDefault">重置为系统默认</el-button>
                <el-button type="primary" @click="saveCoefficients">保存配置</el-button>
              </div>
            </div>
            <div class="coefficient-desc">
              费用系数用于调整大件、普通件、其他件的成本计算系数，仅影响当前报价单
            </div>
            <div class="coefficient-items">
              <div class="coefficient-item">
                <div class="coefficient-item-icon large"><span>大</span></div>
                <div class="coefficient-item-content">
                  <div class="coefficient-item-label">大件系数</div>
                  <div class="coefficient-item-tip">大型设备/材料成本系数</div>
                </div>
                <el-input-number v-model="quotation.coefficients.large" :min="0" :max="10" :precision="2" :step="0.05" style="width: 140px;" />
              </div>
              <div class="coefficient-item">
                <div class="coefficient-item-icon standard"><span>通</span></div>
                <div class="coefficient-item-content">
                  <div class="coefficient-item-label">普通件系数</div>
                  <div class="coefficient-item-tip">标准常规材料成本系数</div>
                </div>
                <el-input-number v-model="quotation.coefficients.standard" :min="0" :max="10" :precision="2" :step="0.05" style="width: 140px;" />
              </div>
              <div class="coefficient-item">
                <div class="coefficient-item-icon other"><span>其</span></div>
                <div class="coefficient-item-content">
                  <div class="coefficient-item-label">其他件系数</div>
                  <div class="coefficient-item-tip">配件耗材等材料成本系数</div>
                </div>
                <el-input-number v-model="quotation.coefficients.other" :min="0" :max="10" :precision="2" :step="0.05" style="width: 140px;" />
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- 物料清单 -->
        <el-tab-pane v-if="isEdit" label="物料清单" name="materials">
          <!-- 已归档警告 -->
          <el-alert v-if="isArchived" title="报价单已归档，物料变更需要提交审核" type="warning" :closable="false" show-icon style="margin-bottom: 16px;">
            <template #default>
              您的物料变更申请将发送给报价单负责人审核，审核通过后才会生效。
              <el-button type="warning" size="small" style="margin-left: 16px;" @click="goToPendingReviews" v-if="pendingReviewCount > 0">
                查看待审核 ({{ pendingReviewCount }})
              </el-button>
            </template>
          </el-alert>
          
          <div class="material-actions">
            <el-select v-model="selectedModuleFilter" placeholder="全部模块" clearable style="width: 200px;">
              <el-option
                v-for="mod in modules"
                :key="mod.id"
                :label="mod.name"
                :value="mod.id"
              />
            </el-select>
          </div>

          <!-- 按模块分组显示物料 -->
          <div v-for="mod in filteredModuleGroups" :key="mod.id" class="module-group">
            <div class="module-group-header">
              <span class="module-name">{{ mod.name }}</span>
              <span class="module-material-count">{{ mod.materials.length }} 项物料</span>
              <span class="module-total">小计: {{ mod.total.toFixed(2) }} 元</span>
              <el-button type="primary" size="small" @click="showAddMaterialToModule(mod.id)">+ 添加物料</el-button>
            </div>
            <el-table :data="mod.materials" border style="width: 100%;">
              <el-table-column prop="material_name" label="物料名称" min-width="120">
                <template #default="{ row }">{{ row.material_name || '-' }}</template>
              </el-table-column>
              <el-table-column prop="specification" label="规格" min-width="100">
                <template #default="{ row }">{{ row.specification || '-' }}</template>
              </el-table-column>
              <el-table-column prop="brand" label="品牌" width="80">
                <template #default="{ row }">{{ row.brand || '-' }}</template>
              </el-table-column>
              <el-table-column prop="unit" label="单位" width="60">
                <template #default="{ row }">{{ row.unit || '-' }}</template>
              </el-table-column>
              <el-table-column prop="unit_price" label="单价" width="90">
                <template #default="{ row }">{{ (row.unit_price || 0).toFixed(2) }}</template>
              </el-table-column>
              <el-table-column label="数量" width="130">
                <template #default="{ row }">
                  <el-input-number
                    :model-value="row.quantity"
                    :min="1"
                    size="small"
                    controls-position="right"
                    @change="(val) => updateMaterialQuantity(row.id, val)"
                  />
                </template>
              </el-table-column>
              <el-table-column label="小计" width="100">
                <template #default="{ row }">
                  {{ ((row.unit_price || 0) * row.quantity).toFixed(2) }}
                </template>
              </el-table-column>
              <el-table-column label="添加人" width="80">
                <template #default="{ row }">
                  {{ getUserName(row.selected_by_id) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="80">
                <template #default="{ row }">
                  <el-button size="small" type="danger" @click="deleteModuleMaterial(row.id)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>

          <!-- 全部模块合计 -->
          <div v-if="moduleMaterials.length > 0" class="material-summary total">
            <span>全部物料合计：{{ allMaterialsTotal.toFixed(2) }} 元</span>
          </div>

          <!-- 添加物料弹窗 -->
          <el-dialog v-model="materialDialogVisible" title="添加物料" width="900px">
            <!-- 筛选栏 -->
            <div class="material-filter-bar">
              <el-input v-model="materialFilter.keyword" placeholder="搜索品名" clearable style="width: 150px;" />
              <el-select v-model="materialFilter.category" placeholder="分类" clearable style="width: 120px;">
                <el-option label="大件" value="large" />
                <el-option label="普通件" value="standard" />
                <el-option label="其他件" value="other" />
              </el-select>
              <el-select v-model="materialFilter.brand" placeholder="品牌" clearable style="width: 120px;">
                <el-option v-for="b in availableBrands" :key="b" :label="b" :value="b" />
              </el-select>
            </div>

            <!-- 物料列表 -->
            <el-table
              :data="filteredAvailableMaterials"
              border
              style="width: 100%; margin-top: 12px;"
              max-height="350"
              @selection-change="handleMaterialSelection"
              ref="materialTableRef"
            >
              <el-table-column type="selection" width="45"></el-table-column>
              <el-table-column prop="name" label="品名" min-width="120" />
              <el-table-column prop="spec" label="规格" min-width="100" />
              <el-table-column prop="brand" label="品牌" width="80" />
              <el-table-column prop="unit" label="单位" width="60" />
              <el-table-column prop="unit_price" label="单价" width="80" />
              <el-table-column label="分类" width="80">
                <template #default="{ row }">{{ getCategoryLabel(row.category) }}</template>
              </el-table-column>
              <el-table-column label="数量" width="130">
                <template #default="{ row }">
                  <el-input-number
                    v-model="row._quantity"
                    :min="1"
                    size="small"
                    controls-position="right"
                    :disabled="!selectedMaterials.includes(row)"
                  />
                </template>
              </el-table-column>
            </el-table>
            <template #footer>
              <el-button @click="materialDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="addMaterialsToModule">确定添加</el-button>
            </template>
          </el-dialog>
        </el-tab-pane>

        <!-- 费用 -->
        <el-tab-pane v-if="isEdit" label="费用" name="fees">
          <div class="fee-actions">
            <el-button type="primary" @click="showAddFee">添加费用</el-button>
          </div>

          <el-table :data="fees" border style="width: 100%; margin-top: 16px;">
            <el-table-column prop="fee_type" label="费用类型" />
            <el-table-column prop="location" label="位置">
              <template #default="{ row }">
                {{ getLocationLabel(row.location) }}
              </template>
            </el-table-column>
            <el-table-column prop="amount" label="金额" />
            <el-table-column prop="description" label="描述" />
            <el-table-column label="操作" width="180">
              <template #default="{ row }">
                <el-button size="small" @click="editFee(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteFee(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 添加/编辑费用弹窗 -->
          <el-dialog v-model="feeDialogVisible" :title="feeDialogTitle" width="500px">
            <el-form :model="feeForm" label-width="100px">
              <el-form-item label="费用类型">
                <el-select v-model="feeForm.fee_type" placeholder="请选择费用类型">
                  <el-option v-for="ft in feeTypes" :key="ft.id" :label="ft.name" :value="ft.name" />
                </el-select>
              </el-form-item>
              <el-form-item label="位置">
                <el-select v-model="feeForm.location" placeholder="请选择位置" disabled>
                  <el-option label="厂内" value="internal" />
                  <el-option label="厂外" value="external" />
                </el-select>
                <div class="form-tip">位置由费用类型自动带出</div>
              </el-form-item>
              <el-form-item label="金额">
                <el-input-number v-model="feeForm.amount" :min="0" :precision="2" />
              </el-form-item>
              <el-form-item label="描述">
                <el-input v-model="feeForm.description" type="textarea" rows="3" placeholder="请输入描述" />
              </el-form-item>
            </el-form>
            <template #footer>
              <el-button @click="feeDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="saveFee">确定</el-button>
            </template>
          </el-dialog>
        </el-tab-pane>

        <!-- 人力工时 -->
        <el-tab-pane v-if="isEdit" label="人力工时" name="labor">
          <div class="labor-header">
            <el-button type="primary" @click="showAddLabor">+ 添加工时</el-button>
          </div>

          <el-table :data="laborHours" border style="width: 100%; margin-top: 16px;">
            <el-table-column prop="name" label="名称" min-width="120">
              <template #default="{ row }">
                <el-input v-if="row._editing" v-model="row._name" size="small" placeholder="工时名称" />
                <span v-else>{{ row.name }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="hours" label="工时" width="120">
              <template #default="{ row }">
                <el-input-number v-if="row._editing" v-model="row._hours" :min="0" :precision="1" size="small" controls-position="right" style="width: 100px;" />
                <span v-else>{{ row.hours }} h</span>
              </template>
            </el-table-column>
            <el-table-column prop="unit_price" label="单价 (元/h)" width="140">
              <template #default="{ row }">
                <el-input-number v-if="row._editing" v-model="row._unit_price" :min="0" :precision="2" size="small" controls-position="right" style="width: 110px;" />
                <span v-else>{{ row.unit_price.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="total" label="合计" width="120">
              <template #default="{ row }">{{ (row.hours * row.unit_price).toFixed(2) }}</template>
            </el-table-column>
            <el-table-column label="操作" width="150" align="center">
              <template #default="{ row }">
                <template v-if="row._editing">
                  <el-button size="small" type="primary" @click="saveLaborRow(row)">保存</el-button>
                  <el-button size="small" @click="cancelLaborEdit(row)">取消</el-button>
                </template>
                <template v-else>
                  <el-button size="small" @click="editLaborRow(row)">编辑</el-button>
                  <el-button size="small" type="danger" @click="deleteLabor(row.id)">删除</el-button>
                </template>
              </template>
            </el-table-column>
          </el-table>

          <div v-if="laborHours.length > 0" class="labor-total">
            人力费用合计：<strong>{{ laborTotal.toFixed(2) }} 元</strong>
          </div>

          <!-- 添加工时弹窗 -->
          <el-dialog v-model="laborDialogVisible" title="添加人力工时" width="450px">
            <el-form :model="laborForm" label-width="100px">
              <el-form-item label="名称">
                <el-input v-model="laborForm.name" placeholder="如：电气设计、现场调试" />
              </el-form-item>
              <el-form-item label="工时">
                <el-input-number v-model="laborForm.hours" :min="0" :precision="1" style="width: 100%;" />
              </el-form-item>
              <el-form-item label="单价 (元/h)">
                <el-input-number v-model="laborForm.unit_price" :min="0" :precision="2" style="width: 100%;" />
              </el-form-item>
              <el-form-item label="合计">
                <span>{{ (laborForm.hours * laborForm.unit_price).toFixed(2) }} 元</span>
              </el-form-item>
            </el-form>
            <template #footer>
              <el-button @click="laborDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="addLaborConfirm">确定</el-button>
            </template>
          </el-dialog>
        </el-tab-pane>

        <!-- 汇总 -->
        <el-tab-pane v-if="isEdit" label="汇总" name="summary">
          <div v-loading="summaryLoading">
            <div class="summary-header">
              <div class="summary-currency">
                <span class="currency-label">显示货币：</span>
                <el-select v-model="selectedCurrency" style="width: 120px;">
                  <el-option v-for="rate in exchangeRates" :key="rate.currency" :label="rate.currency" :value="rate.currency" />
                </el-select>
                <span v-if="selectedCurrency !== 'CNY'" class="currency-note">
                  汇率：{{ getExchangeRate(selectedCurrency) }}，已转换
                </span>
              </div>
            </div>
            <div class="summary-grid" v-if="summary">
              <div class="summary-card">
                <div class="summary-label">物料合计</div>
                <div class="summary-value">{{ summary.material_total?.toFixed(2) || '0.00' }}</div>
              </div>
              <div class="summary-card">
                <div class="summary-label">物料合计(含系数)</div>
                <div class="summary-value highlight">{{ summary.material_total_with_rates?.toFixed(2) || '0.00' }}</div>
              </div>
              <div class="summary-card">
                <div class="summary-label">费用合计</div>
                <div class="summary-value">{{ summary.fees_total?.toFixed(2) || '0.00' }}</div>
              </div>
              <div class="summary-card">
                <div class="summary-label">小计</div>
                <div class="summary-value highlight">{{ summary.subtotal?.toFixed(2) || '0.00' }}</div>
              </div>
              <div class="summary-card">
                <div class="summary-label">对外利润率</div>
                <div class="summary-value">{{ ((summary.profit_rate || 0) * 100).toFixed(0) }}%</div>
              </div>
              <div class="summary-card">
                <div class="summary-label">含利润小计</div>
                <div class="summary-value">{{ summary.subtotal_with_profit?.toFixed(2) || '0.00' }}</div>
              </div>
              <div class="summary-card">
                <div class="summary-label">实际利润</div>
                <div class="summary-value highlight">
                  <span>{{ (summary.subtotal_with_profit - summary.material_total - summary.fees_total)?.toFixed(2) || '0.00' }}</span>
                  <span class="profit-pct">({{ (((summary.subtotal_with_profit - summary.material_total - summary.fees_total) / (summary.material_total + summary.fees_total)) * 100)?.toFixed(1) || '0.0' }}%)</span>
                </div>
              </div>
              <div class="summary-card">
                <div class="summary-label">税率</div>
                <div class="summary-value">{{ (summary.tax_rate * 100)?.toFixed(0) || 0 }}%</div>
              </div>
              <div class="summary-card">
                <div class="summary-label">税额</div>
                <div class="summary-value">{{ summary.tax_amount?.toFixed(2) || '0.00' }}</div>
              </div>
              <div class="summary-card total">
                <div class="summary-label">最终报价</div>
                <div class="summary-value highlight large">
                  {{ convertedSummary?.grand_total?.toFixed(2) || '0.00' }} {{ selectedCurrency }}
                </div>
              </div>
            </div>

            <!-- 费用系数详情 -->
            <div v-if="summary?.rate_details?.length > 0" class="rate-details">
              <h4>费用系数明细</h4>
              <el-table :data="summary.rate_details" border size="small">
                <el-table-column label="分类" width="100">
                  <template #default="{ row }">{{ getCategoryLabel(row.category) }}</template>
                </el-table-column>
                <el-table-column prop="rate" label="系数" width="80">
                  <template #default="{ row }">{{ row.rate }}x</template>
                </el-table-column>
                <el-table-column prop="base" label="原价" width="120">
                  <template #default="{ row }">{{ row.base?.toFixed(2) }}</template>
                </el-table-column>
                <el-table-column prop="with_rate" label="系数后">
                  <template #default="{ row }">{{ row.with_rate?.toFixed(2) }}</template>
                </el-table-column>
              </el-table>
            </div>

            <h3 style="margin-top: 24px;">模块汇总</h3>
            <el-table :data="summary?.modules" border style="width: 100%; margin-top: 8px;">
              <el-table-column prop="module_name" label="模块名称" />
              <el-table-column prop="material_count" label="物料数量" width="100" />
              <el-table-column label="物料小计" width="120">
                <template #default="{ row }">
                  {{ row.material_amount?.toFixed(2) || '0.00' }}
                </template>
              </el-table-column>
              <el-table-column label="含系数小计" width="130">
                <template #default="{ row }">
                  {{ row.material_amount_with_rate?.toFixed(2) || row.material_amount?.toFixed(2) || '0.00' }}
                </template>
              </el-table-column>
            </el-table>

            <h3 style="margin-top: 24px;">费用明细</h3>
            <el-table :data="feesIncludingLabor" border style="width: 100%; margin-top: 8px;">
              <el-table-column prop="fee_type" label="费用类型" />
              <el-table-column prop="location" label="位置/工时">
                <template #default="{ row }">
                  <span v-if="row.hours !== undefined">{{ row.hours }}h</span>
                  <span v-else>{{ getLocationLabel(row.location) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="amount" label="金额" />
              <el-table-column prop="description" label="描述" />
            </el-table>
          </div>
        </el-tab-pane>

        <!-- 版本 -->
        <el-tab-pane v-if="isEdit" label="版本" name="versions">
          <el-table :data="versions" border style="width: 100%;">
            <el-table-column prop="version_no" label="版本号" width="80" />
            <el-table-column prop="created_at" label="创建时间" />
            <el-table-column prop="creator_name" label="创建人" />
            <el-table-column prop="operation_type" label="操作类型" />
            <el-table-column prop="remark" label="备注" show-overflow-tooltip />
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="{ row }">
                <el-dropdown trigger="click" @command="(cmd) => exportVersion(row, cmd)">
                  <el-button size="small" type="warning">PDF ▾</el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="pdf_zh">中文 PDF</el-dropdown-item>
                      <el-dropdown-item command="pdf_en">English PDF</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 导出 -->
        <el-tab-pane v-if="isEdit" label="导出" name="export">
          <div class="export-grid">
            <div class="export-item" @click="exportFile('word')">
              <span class="export-icon">📝</span>
              <span class="export-label">导出 Word</span>
            </div>
            <div class="export-item" @click="exportFile('excel')">
              <span class="export-icon">📊</span>
              <span class="export-label">导出 Excel</span>
            </div>
            <el-dropdown @command="(cmd) => exportFile('pdf', cmd)" trigger="click">
              <div class="export-item" style="cursor:pointer">
                <span class="export-icon">📄</span>
                <span class="export-label">导出 PDF ▾</span>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="zh">🇨🇳 中文 PDF</el-dropdown-item>
                  <el-dropdown-item command="en">🇺🇸 English PDF</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../api/request'
import { feesAPI } from '../api'
import changeRequestsAPI from '../api/changeRequests'

const route = useRoute()
const router = useRouter()

console.log('Route params:', route.params)
console.log('Route path:', route.path)

// 判断是新建还是编辑
const isEdit = computed(() => !!route.params.id && route.params.id !== 'new')
const quotationId = ref(route.params.id || null)
console.log('isEdit:', isEdit.value, 'quotationId:', quotationId.value)
const activeTab = ref('basic')
const quotation = ref({ coefficients: { large: 1.0, standard: 1.0, other: 1.0 } })
const isArchived = computed(() => quotation.value.status === 'approved')
const pendingReviewCount = ref(0)
const permissions = ref({
  can_edit_coefficients: true,
  can_edit_participants: true,
  can_edit_materials: true,
  can_edit_modules: true,
  can_edit_fees: true,
  tabs: []
})
const modules = ref([])
const moduleMaterials = ref([])
const fees = ref([])
const summary = ref(null)
const versions = ref([])
const laborHours = ref([])
const users = ref([])
const businessUsers = ref([])
const feeTypes = ref([])
const availableMaterials = ref([])

const selectedModuleId = ref(null)
const summaryLoading = ref(false)

// 货币切换 - 默认使用报价单币种
const selectedCurrency = ref('CNY')
const exchangeRates = ref([])

// 币种选项 - 来自汇率配置
const currencyOptions = computed(() => {
  const options = [{ label: '人民币 (CNY)', value: 'CNY' }]
  // 从汇率配置中添加其他币种
  const extraCurrencies = {
    'USD': '美元 (USD)',
    'EUR': '欧元 (EUR)',
    'HKD': '港元 (HKD)',
    'GBP': '英镑 (GBP)',
    'JPY': '日元 (JPY)',
  }
  exchangeRates.value.forEach(rate => {
    if (rate.currency !== 'CNY' && extraCurrencies[rate.currency]) {
      options.push({ label: extraCurrencies[rate.currency], value: rate.currency })
    }
  })
  return options
})
const currencyCache = ref({})

function getExchangeRate(currency) {
  if (currency === 'CNY') return 1
  const rate = exchangeRates.value.find(r => r.currency === currency)
  return rate ? rate.rate : 1
}

function convertCurrency(amount, fromCurrency = 'CNY') {
  if (fromCurrency === selectedCurrency.value) return amount
  const fromRate = fromCurrency === 'CNY' ? 1 : getExchangeRate(fromCurrency)
  const toRate = selectedCurrency.value === 'CNY' ? 1 : getExchangeRate(selectedCurrency.value)
  return amount / fromRate * toRate
}

const getCategoryLabel = (cat) => {
  const map = { large: '大件', standard: '普通件', other: '其他件' }
  return map[cat] || cat || '-'
}

const getLocationLabel = (loc) => {
  const map = { internal: '厂内', external: '厂外' }
  return map[loc] || loc || '-'
}

// 汇率转换后的汇总计算（只转换最终报价，其他显示CNY原值）
const convertedSummary = computed(() => {
  if (!summary.value) return null
  const rate = getExchangeRate(selectedCurrency.value)
  // rate 是 "1 目标货币 = rate CNY"，所以转换是除以 rate
  // 例如 700 CNY，USD汇率 7（1 USD = 7 CNY），则 700/7 = $100
  const factor = selectedCurrency.value === 'CNY' ? 1 : 1 / rate

  return {
    ...summary.value,
    grand_total: summary.value.grand_total * factor
  }
})

// 费用明细表格：费用 + 人力工时合并展示
const feesIncludingLabor = computed(() => {
  const feeList = summary.value?.fees || []
  const laborRows = (summary.value?.labor_hours || []).map(l => ({
    fee_type: l.name || '人力工时',
    location: null,
    amount: l.total,
    hours: l.hours,
    description: `${l.hours}h × ${l.unit_price}`
  }))
  return [...feeList, ...laborRows]
})

const participantTypes = ref([])

async function loadParticipantTypes() {
  try {
    const res = await request.get('/participant-type-permissions')
    const list = res || []
    // 提取所有不同的 participant_type，返回对象数组
    const typeMap = {}
    for (const p of list) {
      if (!typeMap[p.participant_type]) {
        typeMap[p.participant_type] = {
          type: p.participant_type,
          type_name: p.type_name || p.participant_type
        }
      }
    }
    participantTypes.value = Object.values(typeMap)
  } catch (e) {
    console.error('加载参与类型失败', e)
  }
}

async function loadExchangeRates(skipCurrencyInit = false) {
  try {
    const [ratesRes, baseRes] = await Promise.all([
      api.get('/exchange_rates'),
      api.get('/exchange_rates/base')
    ])
    exchangeRates.value = Array.isArray(ratesRes) ? ratesRes : (ratesRes.items || [])
    // 只有在未跳过货币初始化且当前未设置报价单币种时，才设置默认货币
    if (!skipCurrencyInit && !quotation.value?.currency) {
      selectedCurrency.value = baseRes.currency || 'CNY'
    }
  } catch (error) {
    console.error('加载汇率失败', error)
  }
}

// 表单验证规则
const formRules = {
  name: [{ required: true, message: '请输入报价单名称', trigger: 'blur' }],
  scheme_no: [{ required: true, message: '请输入方案编号', trigger: 'blur' }],
  type: [{ required: true, message: '请选择项目类型', trigger: 'change' }]
}

// 模块弹窗
const moduleDialogVisible = ref(false)
const moduleDialogTitle = ref('添加模块')
const moduleForm = reactive({
  id: null,
  name: '',
  name_en: '',
  description: ''
})

// 物料弹窗
const materialDialogVisible = ref(false)
const addMaterialQuantity = ref(1)
const selectedMaterials = ref([])
const materialTableRef = ref(null)
const materialFilter = reactive({
  keyword: '',
  category: '',
  brand: ''
})

// 计算属性：过滤后的可选物料
const filteredAvailableMaterials = computed(() => {
  let list = availableMaterials.value || []
  if (materialFilter.keyword) {
    list = list.filter(m => m.name && m.name.toLowerCase().includes(materialFilter.keyword.toLowerCase()))
  }
  if (materialFilter.category) {
    list = list.filter(m => m.category === materialFilter.category)
  }
  if (materialFilter.brand) {
    list = list.filter(m => m.brand === materialFilter.brand)
  }
  return list
})

// 计算属性：可选品牌列表
const availableBrands = computed(() => {
  const brands = new Set()
  availableMaterials.value.forEach(m => {
    if (m.brand) brands.add(m.brand)
  })
  return Array.from(brands).sort()
})

// 计算属性：模块物料合计
const moduleMaterialsTotal = computed(() => {
  return moduleMaterials.value.reduce((sum, m) => {
    return sum + (m.unit_price || 0) * m.quantity
  }, 0)
})

// 模块过滤
const selectedModuleFilter = ref(null)

// 计算属性：按模块分组的物料
const filteredModuleGroups = computed(() => {
  let mods = modules.value
  if (selectedModuleFilter.value) {
    mods = mods.filter(m => m.id === selectedModuleFilter.value)
  }
  return mods.map(mod => {
    const matList = moduleMaterials.value.filter(mm => mm.module_id === mod.id)
    return {
      id: mod.id,
      name: mod.name,
      materials: matList,
      total: matList.reduce((sum, m) => sum + (m.unit_price || 0) * m.quantity, 0)
    }
  })
})

// 计算属性：全部物料总计
const allMaterialsTotal = computed(() => {
  return moduleMaterials.value.reduce((sum, m) => {
    return sum + (m.unit_price || 0) * m.quantity
  }, 0)
})

// 获取用户名
const getUserName = (userId) => {
  if (!userId) return '-'
  const user = users.value.find(u => u.id === userId)
  return user ? user.name : userId
}

// 参与人员管理
const participantDialogVisible = ref(false)
const addParticipantDialogVisible = ref(false)
const quotationParticipants = ref([])
const currentParticipants = ref([])
const selectedParticipantUsers = ref([])
const participantSearch = ref('')
const currentModuleId = ref(null)
const participantLoading = ref(false)

// 计算属性：返回已加载的用户（搜索后由后端返回）
const filteredAvailableUsers = computed(() => {
  const currentUserIds = currentParticipants.value.map(p => p.user_id)
  return users.value.filter(u => !currentUserIds.includes(u.id))
})

// 搜索用户（防抖）
let participantSearchTimer = null
watch(participantSearch, (newVal) => {
  if (participantSearchTimer) clearTimeout(participantSearchTimer)
  participantSearchTimer = setTimeout(() => {
    loadUsers()
  }, 300)
})

// 管理参与人员
async function manageParticipants(module) {
  currentModuleId.value = module.id
  participantSearch.value = ''
  selectedParticipantUsers.value = []
  try {
    const data = await api.get(`/modules/${module.id}/participants`)
    currentParticipants.value = data || []
    participantDialogVisible.value = true
  } catch (error) {
    ElMessage.error('加载参与人员失败')
  }
}

// 显示添加人员弹窗
async function showAddParticipantDialog() {
  participantSearch.value = ''
  selectedParticipantUsers.value = []
  // 加载报价单已有参与人
  if (quotationId.value) {
    try {
      const data = await api.get(`/quotations/${quotationId.value}/participants`)
      quotationParticipants.value = data || []
      currentParticipants.value = quotationParticipants.value
    } catch (error) {
      console.error('加载参与人员失败', error)
    }
  }
  await loadUsers()  // 加载用户列表
  addParticipantDialogVisible.value = true
}

// 检查用户是否可选择（已参与不可选）
function checkParticipantSelectable(row) {
  const currentUserIds = currentParticipants.value.map(p => p.user_id)
  return !currentUserIds.includes(row.id)
}

// 处理选择变化
function handleParticipantSelection(selection) {
  selectedParticipantUsers.value = selection
}

// 确认添加人员
async function addParticipantsConfirm() {
  if (!selectedParticipantUsers.value.length) return
  try {
    for (const user of selectedParticipantUsers.value) {
      await api.post(`/quotations/${quotationId.value}/participants`, {
        user_id: user.id,
        participant_type: 'project'
      })
    }
    ElMessage.success('添加成功')
    addParticipantDialogVisible.value = false
    // 重新加载参与人
    const data = await api.get(`/quotations/${quotationId.value}/participants`)
    quotationParticipants.value = data || []
    currentParticipants.value = quotationParticipants.value
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

// 更新参与人类型
async function updateParticipantType(row) {
  try {
    await api.put(`/quotations/${quotationId.value}/participants/${row.user_id}`, {
      participant_type: row.participant_type
    })
    ElMessage.success('类型已更新')
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

// 移除报价单参与人
async function removeQuotationParticipant(participantId) {
  try {
    const participant = quotationParticipants.value.find(p => p.id === participantId)
    if (!participant) return
    await api.delete(`/quotations/${quotationId.value}/participants/${participant.user_id}`)
    ElMessage.success('移除成功')
    quotationParticipants.value = quotationParticipants.value.filter(p => p.id !== participantId)
    currentParticipants.value = quotationParticipants.value
  } catch (error) {
    ElMessage.error('移除失败')
  }
}

// 保存费用系数
async function saveCoefficients() {
  try {
    await api.put(`/quotations/${quotationId.value}`, {
      coefficients: quotation.value.coefficients
    })
    ElMessage.success('费用系数已保存')
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 重置为系统默认系数
async function resetCoefficientsToDefault() {
  try {
    const data = await api.get('/fee_rates')
    const rates = {}
    ;(data || []).forEach(r => { rates[r.category] = r.rate })
    quotation.value.coefficients = {
      large: rates.large ?? 1.0,
      standard: rates.standard ?? 1.0,
      other: rates.other ?? 1.0
    }
    ElMessage.success('已恢复系统默认系数')
  } catch (error) {
    quotation.value.coefficients = { large: 1.0, standard: 1.0, other: 1.0 }
    ElMessage.warning('获取系统系数失败，已重置为1.0')
  }
}

// 人力工时
const laborDialogVisible = ref(false)
const laborForm = reactive({ name: '', hours: 0, unit_price: 0 })

const laborTotal = computed(() => {
  return laborHours.value.reduce((sum, item) => sum + (item.hours || 0) * (item.unit_price || 0), 0)
})

async function loadLaborHours() {
  if (!quotationId.value) return
  try {
    const data = await api.get(`/quotations/${quotationId.value}/labor-hours`)
    laborHours.value = data || []
  } catch (e) { console.error(e) }
}

function showAddLabor() {
  laborForm.name = ''
  laborForm.hours = 0
  laborForm.unit_price = 0
  laborDialogVisible.value = true
}

async function addLaborConfirm() {
  if (!laborForm.name) { ElMessage.warning('请填写名称'); return }
  if (laborForm.hours <= 0) { ElMessage.warning('工时必须大于0'); return }
  try {
    await api.post(`/quotations/${quotationId.value}/labor-hours`, {
      name: laborForm.name,
      hours: laborForm.hours,
      unit_price: laborForm.unit_price
    })
    ElMessage.success('添加成功')
    laborDialogVisible.value = false
    await loadLaborHours()
  } catch (e) { ElMessage.error('添加失败') }
}

function editLaborRow(row) {
  row._editing = true
  row._name = row.name
  row._hours = row.hours
  row._unit_price = row.unit_price
}

function cancelLaborEdit(row) {
  row._editing = false
}

async function saveLaborRow(row) {
  try {
    await api.put(`/quotations/${quotationId.value}/labor-hours/${row.id}`, {
      name: row._name,
      hours: row._hours,
      unit_price: row._unit_price
    })
    ElMessage.success('保存成功')
    await loadLaborHours()
  } catch (e) { ElMessage.error('保存失败') }
}

async function deleteLabor(id) {
  try {
    await api.delete(`/quotations/${quotationId.value}/labor-hours/${id}`)
    ElMessage.success('删除成功')
    await loadLaborHours()
  } catch (e) { ElMessage.error('删除失败') }
}

// 费用弹窗
const feeDialogVisible = ref(false)
const feeDialogTitle = ref('添加费用')
const feeForm = reactive({
  id: null,
  fee_type: '',
  location: 'factory',
  amount: 0,
  description: ''
})

const api = request

// 加载报价单
async function loadQuotation() {
  console.log('loadQuotation called, id:', quotationId.value)
  if (!quotationId.value) {
    console.log('Skipping loadQuotation - no valid id')
    return
  }
  try {
    const data = await api.get(`/quotations/${quotationId.value}`)
    // 已归档的报价单不允许编辑，重定向回列表
    if (data.status === 'approved') {
      ElMessage.warning('已归档的报价单无法编辑，如需修改请先撤销归档')
      router.push('/quotations')
      return
    }
    quotation.value = data
    // 加载用户操作权限
    try {
      const permData = await api.get(`/quotations/${quotationId.value}/permissions`)
      permissions.value = permData
      // 如果当前 tab 不在允许列表中，切换到第一个可用 tab
      if (!permissions.value.tabs.includes(activeTab.value)) {
        activeTab.value = permissions.value.tabs[0] || 'summary'
      }
    } catch (e) {
      console.error('加载权限失败', e)
    }
    // 确保系数有默认值（优先用报价单私有系数，没有则从系统读取）
    if (!quotation.value.coefficients) {
      // 尝试加载系统默认系数
      try {
        const rates = await api.get('/fee_rates')
        const r = {}
        ;(rates || []).forEach(rate => { r[rate.category] = rate.rate })
        quotation.value.coefficients = {
          large: r.large ?? 1.0,
          standard: r.standard ?? 1.0,
          other: r.other ?? 1.0
        }
      } catch {
        quotation.value.coefficients = { large: 1.0, standard: 1.0, other: 1.0 }
      }
    }
    // 设置默认显示货币为报价单币种
    selectedCurrency.value = data.currency || 'CNY'
    // 加载参与人员
    try {
      const participantsData = await api.get(`/quotations/${quotationId.value}/participants`)
      quotationParticipants.value = participantsData || []
      currentParticipants.value = quotationParticipants.value
    } catch (error) {
      console.error('加载参与人员失败', error)
    }
    console.log('Quotation loaded:', data)
  } catch (error) {
    console.error('Load quotation error:', error)
    ElMessage.error('加载报价单失败: ' + (error.message || '未知错误'))
  }
}

// 加载待审核变更申请数量
async function loadPendingReviewCount() {
  try {
    const data = await changeRequestsAPI.getPending()
    pendingReviewCount.value = Array.isArray(data) ? data.length : (data.total || 0)
  } catch (error) {
    console.error('加载待审核数量失败', error)
  }
}

// 跳转到待审核页面
function goToPendingReviews() {
  router.push('/change-requests')
}

// 加载用户列表（支持分页搜索）
async function loadUsers() {
  try {
    participantLoading.value = true
    const params = new URLSearchParams()
    params.append('page_size', '50')  // 一次加载较多用户
    if (participantSearch.value) {
      params.append('keyword', participantSearch.value)
    }
    const data = await api.get(`/users?${params.toString()}`)
    // 处理分页格式 {items: [...], total: n} 或直接是数组
    users.value = Array.isArray(data) ? data : (data.items || [])
  } catch (error) {
    console.error('加载用户失败', error)
  } finally {
    participantLoading.value = false
  }
}

// 加载业务角色用户
async function loadBusinessUsers() {
  try {
    const res = await api.get('/users?role=business')
    businessUsers.value = res.items || res || []
  } catch (error) {
    console.error('加载业务用户失败', error)
  }
}

// 加载费用类型
async function loadFeeTypes() {
  try {
    const res = await feesAPI.getFeeTypes()
    feeTypes.value = Array.isArray(res) ? res : (res.items || [])
  } catch (error) {
    console.error('加载费用类型失败', error)
  }
}

// 保存基本信息
async function saveBasic() {
  // 表单验证
  if (!quotation.value.name) {
    ElMessage.warning('请输入报价单名称')
    return
  }
  if (!quotation.value.scheme_no) {
    ElMessage.warning('请输入方案编号')
    return
  }
  if (!quotation.value.type) {
    ElMessage.warning('请选择项目类型')
    return
  }

  console.log('saveBasic called', { isEdit: isEdit.value, quotation: quotation.value })
  try {
    // 清理 null 值
    const data = { ...quotation.value }
    Object.keys(data).forEach(key => {
      if (data[key] === null || data[key] === undefined || data[key] === '') {
        delete data[key]
      }
    })
    console.log('Data to save:', data)

    let result
    if (isEdit.value) {
      result = await api.put(`/quotations/${quotationId.value}`, data)
      ElMessage.success('保存成功')
    } else {
      result = await api.post('/quotations', data)
      console.log('Create result:', result)
      ElMessage.success('创建成功')
      // 跳转到编辑页面
      router.push(`/quotations/${result.id}`)
    }
  } catch (error) {
    console.error('Save error:', error)
    ElMessage.error('保存失败: ' + (error.message || '未知错误'))
  }
}

// 保存利润率
async function saveProfitRate() {
  try {
    await api.put(`/quotations/${quotationId.value}`, {
      profit_rate: quotation.value.profit_rate
    })
    ElMessage.success('利润率已保存')
  } catch (error) {
    ElMessage.error('保存利润率失败')
  }
}

// 加载模块
async function loadModules() {
  try {
    const data = await api.get(`/quotations/${quotationId.value}/modules`)
    modules.value = data
  } catch (error) {
    ElMessage.error('加载模块失败')
  }
}

// 显示添加模块弹窗
function showAddModule() {
  moduleDialogTitle.value = '添加模块'
  moduleForm.id = null
  moduleForm.name = ''
  moduleForm.name_en = ''
  moduleForm.description = ''
  moduleDialogVisible.value = true
}

// 编辑模块
function editModule(module) {
  moduleDialogTitle.value = '编辑模块'
  moduleForm.id = module.id
  moduleForm.name = module.name
  moduleForm.name_en = module.name_en || ''
  moduleForm.description = module.description || ''
  moduleDialogVisible.value = true
}

// 保存模块
async function saveModule() {
  try {
    if (moduleForm.id) {
      await api.put(`/modules/${moduleForm.id}`, {
        name: moduleForm.name,
        name_en: moduleForm.name_en,
        description: moduleForm.description
      })
      ElMessage.success('更新成功')
    } else {
      await api.post(`/quotations/${quotationId.value}/modules`, {
        name: moduleForm.name,
        name_en: moduleForm.name_en,
        description: moduleForm.description
      })
      ElMessage.success('添加成功')
    }
    moduleDialogVisible.value = false
    loadModules()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 删除模块
async function deleteModule(id) {
  try {
    await ElMessageBox.confirm('确定要删除该模块吗？', '提示', {
      type: 'warning'
    })
    await api.delete(`/modules/${id}`)
    ElMessage.success('删除成功')
    loadModules()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 加载物料列表（所有可选物料）
async function loadAvailableMaterials() {
  try {
    const data = await api.get('/materials')
    availableMaterials.value = data.items || data || []
  } catch (error) {
    ElMessage.error('加载物料列表失败')
  }
}

// 加载模块物料
async function loadModuleMaterials() {
  // 加载所有模块的物料
  try {
    const allMaterials = []
    for (const mod of modules.value) {
      const data = await api.get(`/modules/${mod.id}/materials`)
      const items = data.items || data || []
      if (items.length > 0) {
        allMaterials.push(...items.map(m => ({ ...m, module_id: mod.id })))
      }
    }
    moduleMaterials.value = allMaterials
  } catch (error) {
    ElMessage.error('加载模块物料失败')
  }
}

// 监听选中模块变化
watch(selectedModuleId, () => {
  loadModuleMaterials()
})

// 费用类型选择后自动带出位置
watch(() => feeForm.fee_type, (newFeeType) => {
  if (newFeeType) {
    const selected = feeTypes.value.find(ft => ft.name === newFeeType)
    if (selected) {
      feeForm.location = selected.location
    }
  }
})

// 显示添加物料弹窗（指定模块）
async function showAddMaterialToModule(moduleId) {
  selectedModuleId.value = moduleId
  await loadAvailableMaterials()
  addMaterialQuantity.value = 1
  selectedMaterials.value = []
  materialDialogVisible.value = true
}

// 显示添加物料弹窗（兼容旧调用）
async function showAddMaterial() {
  if (modules.value.length === 0) {
    ElMessage.warning('请先添加模块')
    return
  }
  selectedModuleId.value = modules.value[0].id
  await loadAvailableMaterials()
  addMaterialQuantity.value = 1
  selectedMaterials.value = []
  materialDialogVisible.value = true
}

// 选择物料
function handleMaterialSelection(selection) {
  selectedMaterials.value = selection
}

// 添加物料到模块
async function addMaterialsToModule() {
  if (selectedMaterials.value.length === 0) {
    ElMessage.warning('请选择物料')
    return
  }
  
  // 已归档报价单需要提交变更申请
  if (isArchived.value) {
    try {
      for (const material of selectedMaterials.value) {
        const qty = material._quantity || 1
        await changeRequestsAPI.create({
          quotation_id: quotationId.value,
          module_id: selectedModuleId.value,
          change_type: 'material_add',
          proposed_data: { material_id: material.id, quantity: qty },
          original_data: {}
        })
      }
      ElMessage.warning('报价单已归档，添加物料已提交审核')
      materialDialogVisible.value = false
      selectedMaterials.value.forEach(m => m._quantity = 1)
      selectedMaterials.value = []
    } catch (error) {
      ElMessage.error('提交变更申请失败')
    }
    return
  }
  
  try {
    for (const material of selectedMaterials.value) {
      const qty = material._quantity || 1
      await api.post(`/modules/${selectedModuleId.value}/materials`, {
        material_id: material.id,
        quantity: qty
      })
    }
    ElMessage.success('添加成功')
    materialDialogVisible.value = false
    // 重置选中物料的 _quantity
    selectedMaterials.value.forEach(m => m._quantity = 1)
    loadModuleMaterials()
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

// 更新模块物料数量
async function updateMaterialQuantity(id, quantity) {
  // 已归档报价单需要提交变更申请
  if (isArchived.value) {
    const row = moduleMaterials.value.find(m => m.id === id)
    try {
      await changeRequestsAPI.create({
        quotation_id: quotationId.value,
        module_id: row.module_id,
        change_type: 'material_update',
        proposed_data: { id, quantity },
        original_data: { id, quantity: row.quantity }
      })
      ElMessage.warning('报价单已归档，数量变更已提交审核')
      loadModuleMaterials() // 刷新显示原始数据
    } catch (error) {
      ElMessage.error('提交变更申请失败')
    }
    return
  }
  
  try {
    await api.put(`/module_materials/${id}`, { quantity })
    ElMessage.success('数量已更新')
    loadModuleMaterials()
  } catch (error) {
    ElMessage.error('更新数量失败')
  }
}

// 删除模块物料
async function deleteModuleMaterial(id) {
  // 已归档报价单需要提交变更申请
  if (isArchived.value) {
    const row = moduleMaterials.value.find(m => m.id === id)
    try {
      await changeRequestsAPI.create({
        quotation_id: quotationId.value,
        module_id: row.module_id,
        change_type: 'material_delete',
        proposed_data: {},
        original_data: { id: row.id, quantity: row.quantity }
      })
      ElMessage.warning('报价单已归档，删除物料已提交审核')
      loadModuleMaterials()
    } catch (error) {
      ElMessage.error('提交变更申请失败')
    }
    return
  }
  
  try {
    await ElMessageBox.confirm('确定要删除该物料吗？', '提示', {
      type: 'warning'
    })
    await api.delete(`/module_materials/${id}`)
    ElMessage.success('删除成功')
    loadModuleMaterials()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 加载费用
async function loadFees() {
  try {
    const data = await api.get(`/quotations/${quotationId.value}/fees`)
    fees.value = data
  } catch (error) {
    ElMessage.error('加载费用失败')
  }
}

// 显示添加费用弹窗
function showAddFee() {
  feeDialogTitle.value = '添加费用'
  feeForm.id = null
  feeForm.fee_type = ''
  feeForm.location = 'factory'
  feeForm.amount = 0
  feeForm.description = ''
  feeDialogVisible.value = true
}

// 编辑费用
function editFee(fee) {
  feeDialogTitle.value = '编辑费用'
  feeForm.id = fee.id
  feeForm.fee_type = fee.fee_type
  feeForm.location = fee.location
  feeForm.amount = fee.amount
  feeForm.description = fee.description || ''
  feeDialogVisible.value = true
}

// 保存费用
async function saveFee() {
  try {
    if (feeForm.id) {
      await api.put(`/fees/${feeForm.id}`, feeForm)
      ElMessage.success('更新成功')
    } else {
      await api.post(`/quotations/${quotationId.value}/fees`, feeForm)
      ElMessage.success('添加成功')
    }
    feeDialogVisible.value = false
    loadFees()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 删除费用
async function deleteFee(id) {
  try {
    await ElMessageBox.confirm('确定要删除该费用吗？', '提示', {
      type: 'warning'
    })
    await api.delete(`/fees/${id}`)
    ElMessage.success('删除成功')
    loadFees()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 加载汇总
async function loadSummary() {
  if (!quotationId.value) return
  summaryLoading.value = true
  try {
    const data = await api.get(`/quotations/${quotationId.value}/summary`)
    summary.value = data
  } catch (error) {
    ElMessage.error('加载汇总失败')
  } finally {
    summaryLoading.value = false
  }
}

// 加载版本
async function loadVersions() {
  if (!quotationId.value) return
  try {
    const data = await api.get(`/quotations/${quotationId.value}/versions`)
    versions.value = data
  } catch (error) {
    ElMessage.error('加载版本失败')
  }
}

// 查看版本
function viewVersion(version) {
  ElMessage.info(`查看版本 V${version.version} - ${version.remark || '无备注'}`)
  // TODO: 可以打开版本详情弹窗
}

// 导出特定版本
function exportVersion(version, cmd) {
  // cmd: 'pdf_zh' | 'pdf_en'
  const [fmt, lang] = cmd.split('_')
  window.open(`/api/quotations/${quotationId.value}/versions/${version.version_no}/export/${fmt}?lang=${lang}`, '_blank')
}

// 导出文件
function exportFile(format, lang = 'zh') {
  const langParam = (format === 'pdf' && lang) ? `&lang=${lang}` : ''
  window.open(`/api/quotations/${quotationId.value}/export/${format}?currency=${selectedCurrency.value}${langParam}`, '_blank')
}

// 返回列表
function goBack() {
  router.push('/quotations')
}

// 监听 tab 变化
watch(activeTab, (tab) => {
  if (tab === 'summary') {
    loadSummary()
  } else if (tab === 'versions') {
    loadVersions()
  }
})

// 监听路由参数变化
watch(() => route.params.id, (newId) => {
  quotationId.value = newId || null
  if (newId && newId !== 'new') {
    loadQuotation()
    loadModules()
    loadFees()
  }
}, { immediate: false })

onMounted(async () => {
  await loadUsers()
  await loadBusinessUsers()
  await loadFeeTypes()
  await loadParticipantTypes()
  if (isEdit.value) {
    await loadQuotation()  // 先加载报价单，获取币种
    await loadExchangeRates(true)  // 跳过货币初始化，使用报价单币种
    await loadModules()
    await loadModuleMaterials()
    await loadFees()
    await loadLaborHours()
  } else {
    await loadExchangeRates()  // 新建模式，使用默认币种
  }
})
</script>

<style scoped>
.quotation-edit {
  padding: var(--spacing-lg);
}

/* 页面标题栏 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.page-header-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.back-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.back-btn:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.page-title-sub {
  font-size: 14px;
  color: var(--color-text-muted);
  margin-left: var(--spacing-sm);
}

/* 卡片容器 */
.edit-card {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  overflow: hidden;
}

/* Tabs 样式 */
.edit-card :deep(.el-tabs__header) {
  margin: 0;
  padding: 0 var(--spacing-lg);
  background: var(--color-bg-hover);
  border-bottom: 1px solid var(--color-border-light);
}

.edit-card :deep(.el-tabs__nav-wrap::after) {
  display: none;
}

.edit-card :deep(.el-tabs__item) {
  height: 48px;
  line-height: 48px;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  padding: 0 var(--spacing-lg);
}

.edit-card :deep(.el-tabs__item.is-active) {
  color: var(--color-primary);
}

.edit-card :deep(.el-tabs__active-bar) {
  height: 3px;
  background: var(--color-primary);
}

.edit-card :deep(.el-tabs__content) {
  padding: var(--spacing-lg);
}

/* 表单样式 */
.form-section {
  max-width: 600px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
}

.form-actions {
  display: flex;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--color-border-light);
}

.save-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-xl);
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.save-btn:hover {
  background: var(--color-primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

/* 表格容器 */
.table-section {
  margin-top: var(--spacing-md);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.table-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.table-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-md);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  border: none;
}

.action-btn.primary {
  background: var(--color-primary);
  color: white;
}

.action-btn.primary:hover {
  background: var(--color-primary-hover);
}

.action-btn.secondary {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

.action-btn.secondary:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

/* 数据表格 */
.data-table {
  border-radius: var(--radius-md);
  overflow: hidden;
}

.data-table :deep(.el-table__header-wrapper th) {
  background: var(--color-bg-hover) !important;
  color: var(--color-text-primary);
  font-weight: 600;
  font-size: 13px;
  padding: 12px 0;
}

.data-table :deep(.el-table__body-wrapper tr) {
  transition: background var(--transition-fast);
}

.data-table :deep(.el-table__body-wrapper tr:hover) {
  background: var(--color-bg-hover);
}

/* 单元格操作按钮 */
.cell-btn {
  padding: 4px 12px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  border: none;
  background: none;
}

.cell-btn.edit {
  color: var(--color-primary);
  background: var(--color-primary-light);
}

.cell-btn.edit:hover {
  background: var(--color-primary);
  color: white;
}

.cell-btn.delete {
  color: var(--color-danger);
  background: var(--color-danger-bg);
}

.cell-btn.delete:hover {
  background: var(--color-danger);
  color: white;
}

/* 弹窗样式 */
.dialog-header {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.dialog-form {
  padding: var(--spacing-md) 0;
}

.dialog-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--color-text-primary);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--color-border-light);
}

.cancel-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--radius-md);
  font-size: 14px;
  background: var(--color-bg-card);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.cancel-btn:hover {
  background: var(--color-bg-hover);
}

.confirm-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--radius-md);
  font-size: 14px;
  background: var(--color-primary);
  color: white;
  border: none;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.confirm-btn:hover {
  background: var(--color-primary-hover);
}

.summary-header {
  margin-bottom: var(--spacing-md);
}

.summary-currency {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.currency-label {
  font-weight: 500;
  color: var(--color-text-secondary);
}

.currency-note {
  font-size: 12px;
  color: var(--color-primary);
}

/* 汇总卡片 */
.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.summary-card {
  background: var(--color-bg-hover);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  text-align: center;
}

.summary-card.total {
  grid-column: 1 / -1;
  background: var(--color-primary);
  color: white;
}

.summary-card.total .summary-label {
  color: rgba(255,255,255,0.8);
}

.summary-label {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-xs);
}

.summary-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.summary-value.highlight {
  color: var(--color-primary);
}

.summary-value.large {
  font-size: 32px;
  color: #FFFFFF;
}

.rate-details {
  margin-top: var(--spacing-lg);
  padding: var(--spacing-md);
  background: var(--color-bg-hover);
  border-radius: var(--radius-md);
}

.rate-details h4 {
  margin: 0 0 var(--spacing-sm) 0;
  color: var(--color-text-primary);
}

/* 导出按钮组 */
.export-grid {
  display: flex;
  gap: var(--spacing-md);
}

.export-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xl);
  background: var(--color-bg-hover);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  border: 1px solid transparent;
}

.export-item:hover {
  border-color: var(--color-primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.export-icon {
  font-size: 32px;
}

.export-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: var(--spacing-2xl);
  color: var(--color-text-muted);
}

.empty-icon {
  font-size: 48px;
  opacity: 0.5;
  margin-bottom: var(--spacing-md);
  display: block;
}

.module-actions,
.material-actions,
.fee-actions,
.export-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.material-filter-bar {
  display: flex;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.participant-manager {
  padding: 8px 0;
}

.participant-section {
  margin-bottom: 8px;
}

.participant-section h4 {
  margin: 0 0 12px 0;
  color: var(--color-text-primary);
  font-size: 14px;
}

.participant-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.user-list {
  max-height: 250px;
  overflow-y: auto;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.user-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-bottom: 1px solid var(--color-border);
}

.user-item:last-child {
  border-bottom: none;
}

.user-item:hover {
  background: var(--color-bg-hover);
}

.empty-text {
  color: var(--color-text-secondary);
  text-align: center;
  padding: 20px;
}

.material-summary {
  margin-top: 16px;
  padding: 12px 16px;
  background: var(--color-primary-light);
  border-radius: var(--radius-md);
  text-align: right;
  font-weight: 600;
  color: var(--color-primary);
}

.material-summary.total {
  background: var(--color-primary);
  color: white;
}

.module-group {
  margin-bottom: 24px;
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.module-group-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  background: var(--color-bg-hover);
  border-bottom: 1px solid var(--color-border-light);
}

.module-name {
  font-weight: 600;
  color: var(--color-text-primary);
}

.module-material-count {
  color: var(--color-text-secondary);
  font-size: 13px;
}

.module-total {
  margin-left: auto;
  font-weight: 600;
  color: var(--color-primary);
}

/* 响应式 */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .summary-grid {
    grid-template-columns: 1fr;
  }
}

/* 费用系数卡片 */
.coefficient-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 24px;
  max-width: 560px;
}

.coefficient-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.coefficient-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.coefficient-actions {
  display: flex;
  gap: 8px;
}

.coefficient-desc {
  color: #6b7280;
  font-size: 13px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f3f4f6;
}

.coefficient-items {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.coefficient-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 14px;
  background: #f9fafb;
  border-radius: 8px;
}

.coefficient-item-label {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.coefficient-item-tip {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 2px;
}

.coefficient-item-icon {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
  background: #d1d5db;
}

.coefficient-item-icon.large { background: linear-gradient(135deg, #f97316, #ea580c); }
.coefficient-item-icon.standard { background: linear-gradient(135deg, #0D9488, #0f766e); }
.coefficient-item-icon.other { background: linear-gradient(135deg, #6366f1, #4f46e5); }

.labor-header {
  display: flex;
  gap: 8px;
}

.labor-total {
  margin-top: 16px;
  padding: 12px 16px;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
  color: #166534;
  font-size: 14px;
}
</style>
