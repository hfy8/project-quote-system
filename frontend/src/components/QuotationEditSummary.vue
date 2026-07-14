<template>
  <div v-loading="summaryLoading" ref="summaryRef">
    <div class="summary-header no-export">
      <div class="summary-currency">
        <span class="currency-label">显示货币：</span>
        <el-select :model-value="selectedCurrency" @update:model-value="$emit('update:selectedCurrency', $event)" style="width: 120px;">
          <el-option v-for="rate in exchangeRates" :key="rate.currency" :label="rate.currency" :value="rate.currency" />
        </el-select>
        <span v-if="selectedCurrency !== 'CNY'" class="currency-note">
          汇率：{{ getExchangeRate(selectedCurrency) }}，已转换
        </span>
      </div>
    </div>
    <div v-if="summary" class="summary-top-cards">
      <!-- 第一行: 硬件 / 设计 / 调试 / 差旅(人天) / 认证 -->
      <div class="summary-row-cards">
        <div class="summary-mini-card card-hardware">
          <div class="summary-mini-icon">🔧</div>
          <div class="summary-mini-label">硬件成本</div>
          <div class="summary-mini-value highlight">{{ fmtMoney(summary.material_total_with_rates) }}</div>
        </div>
        <div class="summary-mini-card card-design">
          <div class="summary-mini-icon">🎨</div>
          <div class="summary-mini-label">设计人力成本</div>
          <div class="summary-mini-value">{{ fmtMoney(designLaborCost) }}</div>
        </div>
        <div class="summary-mini-card card-debug">
          <div class="summary-mini-icon">🔨</div>
          <div class="summary-mini-label">调试人力成本</div>
          <div class="summary-mini-value">{{ fmtMoney(debugLaborCost) }}</div>
        </div>
        <div class="summary-mini-card card-travel-days">
          <div class="summary-mini-icon">🧳</div>
          <div class="summary-mini-label">差旅成本（出差人天）</div>
          <div class="summary-mini-value">{{ fmtMoney(summary.travel_person_days_total) }}</div>
        </div>
        <div class="summary-mini-card card-cert">
          <div class="summary-mini-icon">📜</div>
          <div class="summary-mini-label">认证费用成本</div>
          <div class="summary-mini-value">{{ fmtMoney(certificationFeeCost) }}</div>
        </div>
      </div>

      <!-- 第二行: 机票签证 / 项目管理 / 项目利润 / 包装运输 / 最终报价 -->
      <div class="summary-row-cards">
        <div class="summary-mini-card card-travel-trips">
          <div class="summary-mini-icon">✈️</div>
          <div class="summary-mini-label">差旅机票签证</div>
          <div class="summary-mini-value">{{ fmtMoney(summary.travel_person_trips_total) }}</div>
        </div>
        <div class="summary-mini-card card-mgmt">
          <div class="summary-mini-icon">📊</div>
          <div class="summary-mini-label">项目管理费用</div>
          <div class="summary-mini-value">{{ fmtMoney(projectManagementFee) }}</div>
        </div>
        <div class="summary-mini-card card-profit">
          <div class="summary-mini-icon">💰</div>
          <div class="summary-mini-label">项目利润（对外利润）</div>
          <div class="summary-mini-value">{{ fmtMoney(profitAmount) }}</div>
          <div class="summary-mini-sub">利润率 {{ ((summary.profit_rate || 0) * 100).toFixed(2) }}%</div>
        </div>
        <div class="summary-mini-card card-packing">
          <div class="summary-mini-icon">📦</div>
          <div class="summary-mini-label">包装运输费用</div>
          <div class="summary-mini-value">{{ fmtMoney(summary.packing_total) }}</div>
        </div>
        <div class="summary-mini-card card-grand-total">
          <div class="summary-mini-icon">💵</div>
          <div class="summary-mini-label">最终报价</div>
          <div class="summary-mini-value huge">{{ fmtMoney(summary.grand_total) }}</div>
          <div class="summary-mini-sub">含税 ¥{{ summary.tax_amount?.toFixed(2) || '0.00' }}</div>
        </div>
      </div>
    </div>

    <!-- 占比分析 -->
    <div v-if="summary" class="breakdown-section">
      <h3 class="section-title">📊 占比分析（基于含利润小计）</h3>

      <!-- 目标调价: 5 张卡片 -->
      <h4 class="section-subtitle" style="margin-top: 24px;">🎯 目标调价</h4>
      <div class="target-price-cards">
        <!-- 1. 硬件 (实际) -->
        <div class="target-card">
          <div class="target-label">🔧 硬件（含系数）</div>
          <div class="target-value highlight">¥{{ summary.material_total_with_rates?.toFixed(2) || '0.00' }}</div>
          <div class="target-meta">占最终含税报价 <strong>{{ actualHardwareRatioPercent.toFixed(2) }}%</strong></div>
          <div class="target-bar">
            <div class="target-bar-fill" :style="{ width: actualHardwareRatioPercent + '%' }"></div>
          </div>
          <div class="target-sub-meta">最终含税报价 ¥{{ finalPriceWithTax?.toFixed(2) || '0.00' }}</div>
        </div>

        <!-- 2. 大件 (占硬件) -->
        <div class="target-card">
          <div class="target-label">📦 大件占硬件</div>
          <div class="target-value highlight">¥{{ largeHardwareAmount?.toFixed(2) || '0.00' }}</div>
          <div class="target-meta">占硬件 <strong>{{ largeHardwareRatioPercent.toFixed(2) }}%</strong></div>
          <div class="target-bar">
            <div class="target-bar-fill cat-large" :style="{ width: largeHardwareRatioPercent + '%' }"></div>
          </div>
          <div class="target-sub-meta">硬件合计 ¥{{ summary.material_total_with_rates?.toFixed(2) || '0.00' }}</div>
        </div>

        <!-- 3. 机械/电控比 -->
        <div class="target-card">
          <div class="target-label">⚖️ 机械/电控比</div>
          <div class="target-value target-ratio-text">{{ moduleTypeRatio.label }}</div>
          <div class="target-meta">
            机械 ¥{{ moduleTypeRatio.mech.toFixed(0) }} : 电控 ¥{{ moduleTypeRatio.elec.toFixed(0) }}
          </div>
          <div class="target-bar">
            <div class="target-bar-fill cat-mechanical" :style="{ width: ((moduleTypeRatio.mech / Math.max(moduleTypeRatio.mech + moduleTypeRatio.elec, 1)) * 100) + '%' }"></div>
            <div class="target-bar-fill cat-electrical" :style="{ width: ((moduleTypeRatio.elec / Math.max(moduleTypeRatio.mech + moduleTypeRatio.elec, 1)) * 100) + '%', left: ((moduleTypeRatio.mech / Math.max(moduleTypeRatio.mech + moduleTypeRatio.elec, 1)) * 100) + '%' }"></div>
          </div>
          <div class="target-sub-meta">基于模块硬件成本（含系数）</div>
        </div>

        <!-- 4. 目标硬件占比 (可编辑) -->
        <div class="target-card target-card-editable">
          <div class="target-label">🎯 目标硬件占比 <span class="editable-tag">可调</span></div>
          <div class="target-input-wrap">
            <el-input-number
              :model-value="targetHardwareRatio"
              @update:modelValue="onTargetHardwareRatioInput"
              :min="0.01" :max="99" :step="0.5" :precision="2"
              size="large"
              style="width: 100%;"
            >
              <template #append>%</template>
            </el-input-number>
          </div>
          <el-slider
            :model-value="targetHardwareRatio"
            @update:modelValue="onTargetHardwareRatioInput"
            :min="0.01" :max="99" :step="0.5"
            show-input
            :show-input-controls="false"
            style="margin-top: 8px;"
          />
          <div class="target-sub-meta">
            初始 {{ actualHardwareRatioPercent.toFixed(2) }}%
            <el-button link size="small" type="info" @click="resetTargetHardwareRatio" style="margin-left: 8px;">重置</el-button>
          </div>
        </div>

        <!-- 5. 目标报价 (联动: 硬件不变反推最终含税报价) -->
        <div class="target-card target-card-highlight">
          <div class="target-label">💰 目标最终含税报价（硬件不变·反推）</div>
          <div class="target-value huge">
            <template v-if="Number.isFinite(targetFinalPrice)">
              ¥{{ targetFinalPrice?.toFixed(2) || '0.00' }}
            </template>
            <template v-else>
              ∞
            </template>
          </div>
          <div class="target-meta">
            当前最终含税 ¥{{ finalPriceWithTax?.toFixed(2) || '0.00' }}
            <span :class="['delta', targetPriceDelta >= 0 ? 'delta-pos' : 'delta-neg']">
              {{ targetPriceDelta >= 0 ? '+' : '' }}{{ targetPriceDelta.toFixed(2) }}
            </span>
          </div>
          <div class="target-bar">
            <div class="target-bar-fill" :style="{ width: (Number.isFinite(targetFinalPrice) ? targetHardwareRatio : 100) + '%' }"></div>
          </div>
          <div class="target-sub-meta">
            硬件不变 ¥{{ summary.material_total_with_rates?.toFixed(2) || '0.00' }} · 其他部分 ¥{{ targetOtherPartsTotal?.toFixed(2) || '0.00' }}
          </div>
        </div>

        <!-- 6. 其他成本建议 (7 金额项按权重分配 + 利润/税额按比例联动) -->
        <div class="target-card target-card-editable target-card-wide">
          <div class="target-label">
            💡 其他成本建议
            <span class="editable-tag">硬件不变·按权重分配</span>
          </div>

          <!-- 6a. 5 个金额项 (subtotal 中的非硬件部分) -->
          <el-table :data="otherPartsSuggestions.amountItems" border size="small" style="margin-top: 6px;">
            <el-table-column label="项目" width="130">
              <template #default="{ row }">
                <span style="font-size: 16px;">{{ row.icon }}</span>
                <span style="margin-left: 6px;">{{ row.label }}</span>
              </template>
            </el-table-column>
            <el-table-column label="权重" width="70" align="center">
              <template #default="{ row }">
                <span :class="row.weight === 0 ? 'muted' : ''">{{ (row.weight * 100).toFixed(1) }}%</span>
              </template>
            </el-table-column>
            <el-table-column label="建议金额" width="110" align="right">
              <template #default="{ row }">
                <strong :class="row.current === 0 ? 'muted' : ''">¥{{ row.target.toFixed(2) }}</strong>
              </template>
            </el-table-column>
            <el-table-column label="调整金额" width="100" align="right" :resizable="false">
              <template #default="{ row }">
                <span :class="['uplift-amt', row.delta >= 0 ? 'uplift-pos' : 'uplift-neg', row.current === 0 ? 'muted' : '']">
                  {{ row.delta >= 0 ? '+' : '' }}{{ row.delta.toFixed(2) }}
                </span>
              </template>
            </el-table-column>
          </el-table>

          <!-- 6a-小计: 6 项金额项合计 (合并到一行) -->
          <div class="target-sub-meta">
            小计 ¥{{ otherPartsSuggestions.subCurrent.toFixed(2) }}
            <span style="margin: 0 6px;">→</span>
            ¥{{ otherPartsSuggestions.subTarget.toFixed(2) }}
            <span :class="['delta', (otherPartsSuggestions.subTarget - otherPartsSuggestions.subCurrent) >= 0 ? 'delta-pos' : 'delta-neg']" style="margin-left: 6px;">
              ({{ (otherPartsSuggestions.subTarget - otherPartsSuggestions.subCurrent) >= 0 ? '+' : '' }}{{ (otherPartsSuggestions.subTarget - otherPartsSuggestions.subCurrent).toFixed(2) }})
            </span>
          </div>
        </div>
      </div>
    </div>

    <h3 style="margin-top: 24px;">模块汇总</h3>

    <!-- 按模块类型分组卡片展示 -->
    <div class="summary-modules-grid">
      <div v-for="group in groupedSummaryModulesByType" :key="group.value" class="module-type-group summary-module-card">
        <div class="module-type-header" :class="'type-' + group.value">
          <div class="module-type-icon" :class="'type-' + group.value">
            <span v-if="group.value === 'mechanical'">🔧</span>
            <span v-else-if="group.value === 'electrical'">⚡</span>
            <span v-else>📦</span>
          </div>
          <span class="module-type-title">{{ group.label }}模块</span>
          <span class="module-type-count">{{ group.group_module_count }} 个</span>
        </div>
        <div class="module-type-stats">
          <div class="module-type-stat-row">
            <span class="stat-label">模块数</span>
            <span class="stat-value">{{ group.group_module_count }}</span>
          </div>
          <div class="module-type-stat-row">
            <span class="stat-label">物料数</span>
            <span class="stat-value">{{ group.group_materials_count }}</span>
          </div>
          <div class="module-type-stat-row">
            <span class="stat-label">物料小计</span>
            <span class="stat-value">¥{{ group.group_total.toFixed(2) }}</span>
          </div>
          <div class="module-type-stat-row highlight">
            <span class="stat-label">含系数小计</span>
            <span class="stat-value module-type-total">¥{{ group.group_total_with_rate.toFixed(2) }}</span>
          </div>
        </div>
        <div class="module-type-table-wrapper">
          <el-table :data="group.module_list" border height="400" empty-text="暂无模块" style="width: 100%;">
            <el-table-column prop="module_name" label="模块名称" min-width="60" flex="1">
              <template #default="{ row }">
                <div class="cell-name-wrap">
                  <span class="cell-module-name" :title="row.module_name">{{ row.module_name }}</span>
                  <el-tag size="mini" :type="row.module_type === 'mechanical' ? 'primary' : row.module_type === 'electrical' ? 'warning' : 'info'" effect="plain">
                    {{ row.module_type_label || '其他' }}
                  </el-tag>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="material_count" label="物料" min-width="50" align="center" />
            <el-table-column label="物料小计" min-width="80" align="right">
              <template #default="{ row }">
                <span class="cell-amount">¥{{ (row.material_amount || 0).toFixed(0) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="含系数" width="90" align="right">
              <template #default="{ row }">
                <span class="cell-amount highlight">¥{{ (row.material_amount_with_rate || row.material_amount || 0).toFixed(0) }}</span>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </div>

    <!-- 兼容旧数据 -->
    <el-table v-if="groupedSummaryModulesByType.length === 0 && summary?.modules?.length > 0" :data="summary.modules" border style="width: 100%; margin-top: 8px;">
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

    <!-- 报价单系数明细 -->
    <h3 style="margin-top: 32px;">📋 报价单系数明细</h3>
    <div v-if="summary" class="coefficient-detail-section">
      <!-- 卡片 1: 单价 + 系数 (销售) -->
      <div class="detail-card">
        <div class="detail-card-header">
          <h4>📋 单价/系数（销售）</h4>
        </div>
        <el-table :data="detailPriceRows" border size="small">
          <el-table-column prop="group" label="类别" width="140" />
          <el-table-column prop="label" label="项目" />
          <el-table-column prop="value" label="数值" width="140" align="right">
            <template #default="{ row }">
              <span :class="{ 'value-strong': row.strong }">{{ row.value }}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 卡片 2: 数量 (项目) -->
      <div class="detail-card">
        <div class="detail-card-header">
          <h4>📊 数量（项目）</h4>
        </div>
        <el-table :data="detailQuantityRows" border size="small">
          <el-table-column prop="group" label="类别" width="140" />
          <el-table-column prop="label" label="项目" />
          <el-table-column prop="value" label="数量" width="140" align="right">
            <template #default="{ row }">
              <span :class="{ 'value-strong': row.strong }">{{ row.value }}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  summary: { type: Object, default: null },
  summaryLoading: { type: Boolean, default: false },
  selectedCurrency: { type: String, default: 'CNY' },
  exchangeRates: { type: Array, default: () => [] },
  exchangeRateSymbol: { type: String, default: '' },
  groupedSummaryModulesByType: { type: Array, default: () => [] },
  allModulesCount: { type: Number, default: 0 },
})

const emit = defineEmits([
  'update:selectedCurrency',
  'goQuotation',
  'toggleModuleReadiness',
])

// Template ref for PDF export
const summaryRef = ref(null)
defineExpose({ summaryRef })

// ====== Helper functions ======

const fmtMoney = (v) => `¥${(Number(v) || 0).toFixed(2)}`

function getExchangeRate(currency) {
  if (currency === 'CNY') return 1
  const rate = props.exchangeRates.find(r => r.currency === currency)
  return rate ? rate.rate : 1
}

const getCategoryLabel = (cat) => {
  const map = { large: '大件', standard: '核心部件', other: '其他件' }
  return map[cat] || cat || '-'
}

// 硬件分类占比
function getMaterialCategoryRatio(amount) {
  if (!props.summary || !amount) return '0.00'
  const denom = props.summary.material_total_with_rates || 0
  if (denom === 0) return '0.00'
  return ((amount / denom) * 100).toFixed(2)
}

// ====== 目标调价 ======

const targetHardwareRatio = ref(null)
const targetHardwareManuallySet = ref(false)

const actualHardwareRatioPercent = computed(() => {
  if (!props.summary) return 0
  const hw = props.summary.material_total_with_rates || 0
  // 硬件占最终含税报价 (用户要求：硬件占比 = 硬件 / 最终含税报价)
  const denom = (finalPriceWithTax.value || 0)
  if (denom === 0) return 0
  return (hw / denom) * 100
})

watch(actualHardwareRatioPercent, (newVal) => {
  if (newVal > 0 && !targetHardwareManuallySet.value) {
    targetHardwareRatio.value = Number(newVal.toFixed(2))
  }
}, { immediate: true })

function onTargetHardwareRatioInput(val) {
  targetHardwareManuallySet.value = true
  let v = Number(val) || 0
  // 边界保护: 占比应在 [0.01, 99] 区间, 否则反推公式会发散
  if (v < 0.01) v = 0.01
  if (v > 99) v = 99
  targetHardwareRatio.value = v
}

function resetTargetHardwareRatio() {
  targetHardwareManuallySet.value = false
  targetHardwareRatio.value = Number(actualHardwareRatioPercent.value.toFixed(2))
}

const largeHardwareAmount = computed(() => {
  if (!props.summary) return 0
  const rows = props.summary.rate_details || []
  const r = rows.find(x => x.category === 'large')
  return r ? (r.with_rate || 0) : 0
})

const largeHardwareRatioPercent = computed(() => {
  if (!props.summary) return 0
  const denom = props.summary.material_total_with_rates || 0
  if (denom === 0) return 0
  return (largeHardwareAmount.value / denom) * 100
})

const moduleTypeRatio = computed(() => {
  if (!props.summary) return { mech: 0, elec: 0, label: '0 : 0' }
  let mech = 0, elec = 0
  for (const sm of (props.summary.modules || [])) {
    const amt = sm.material_amount_with_rate || sm.material_amount || 0
    if (sm.module_type === 'mechanical') mech += amt
    else if (sm.module_type === 'electrical') elec += amt
  }
  return {
    mech,
    elec,
    label: elec > 0
      ? `${mech.toFixed(0)} : ${elec.toFixed(0)} ≈ ${(mech / elec).toFixed(2)}`
      : (mech > 0 ? `机械 ${mech.toFixed(0)} / 无电控模块` : '暂无模块')
  }
})

const noTaxPrice = computed(() => {
  if (!props.summary) return 0
  return props.summary.subtotal || 0
})
const finalPriceWithTax = computed(() => {
  // 最终含税报价 = grand_total (subtotal_with_profit + tax_amount)
  if (!props.summary) return 0
  return props.summary.grand_total || 0
})

const targetFinalPrice = computed(() => {
  // 目标最终含税报价 (用户要求：保持硬件不变，按目标硬件占比反推)
  // 公式: targetFinalPrice = hw / targetRatio
  // 含义: 硬件 hw 固定, 调整"其他部分"(人力/运输/差旅/签证) 使最终含税报价刚好让硬件占比 = 目标占比
  const ratio = Number(targetHardwareRatio.value || 0)
  if (ratio <= 0 || !props.summary) return 0
  if (ratio >= 100) return Infinity  // 占比 >= 100% 时无解
  const hw = props.summary.material_total_with_rates || 0
  return hw / (ratio / 100)
})

// "其他部分"在目标最终含税报价下的总金额 (= 目标最终含税报价 - 硬件)
const targetOtherPartsTotal = computed(() => {
  const tp = targetFinalPrice.value
  if (!isFinite(tp) || !props.summary) return 0
  const hw = props.summary.material_total_with_rates || 0
  return Math.max(0, tp - hw)
})

// "其他部分"在当前最终含税报价下的总金额 (= 当前最终含税报价 - 硬件)
const currentOtherPartsTotal = computed(() => {
  if (!props.summary) return 0
  const fp = finalPriceWithTax.value || 0
  const hw = props.summary.material_total_with_rates || 0
  return Math.max(0, fp - hw)
})

// 其他部分调整金额 (目标 - 当前)
const otherPartsDelta = computed(() => {
  return targetOtherPartsTotal.value - currentOtherPartsTotal.value
})

const targetHardwareAtTarget = computed(() => {
  // 硬件金额 (保持不变) = summary.material_total_with_rates
  const hw = props.summary?.material_total_with_rates || 0
  return hw
})

const otherPartsSuggestions = computed(() => {
  // 其他成本建议: 5 个金额项按权重分配 (设计+调试+装配合并为人力工时, 认证/管理合并为"管理认证其他")
  if (!props.summary) return { amountItems: [], subCurrent: 0, subTarget: 0 }

  // ===== 5 个金额项 (subtotal 中的非硬件部分) =====
  // 1. 人力工时 (设计 + 调试 + 装配)
  const labor = (props.summary.labor_details || [])
    .reduce((s, d) => s + (Number(d.total) || 0), 0)
  // 2. 差旅人天
  const travelDays = Number(props.summary.travel_person_days_total || 0)
  // 3. 机票签证 (含签证)
  const travelTrips = Number(props.summary.travel_person_trips_total || 0)
  // 4. 包装运输
  const packing = Number(props.summary.packing_total || 0)
  // 5. 管理认证其他 = 费用 tab 中所有项的合计 (认证费+项目管理费+其他费用类型)
  const mgmtCertOther = (props.summary.fees || [])
    .reduce((s, f) => s + (Number(f.amount) || 0), 0)

  const amountItems = [
    { key: 'labor',         label: '人力工时',     icon: '👷', current: labor },
    { key: 'travelDays',    label: '差旅人天',     icon: '🧳', current: travelDays },
    { key: 'travelTrips',   label: '机票签证',     icon: '✈️', current: travelTrips },
    { key: 'packing',       label: '包装运输',     icon: '📦', current: packing },
    { key: 'mgmtCertOther', label: '管理认证其他', icon: '📋', current: mgmtCertOther },
  ]

  const subCurrent = amountItems.reduce((s, it) => s + it.current, 0)

  // ===== 目标金额推导 (保持 R=profit×tax 比例不变) =====
  const profitRate = Number(props.summary.profit_rate || 0)
  const taxRate    = Number(props.summary.tax_rate || 0)
  const R = (1 + profitRate) * (1 + taxRate)

  const hw = props.summary.material_total_with_rates || 0
  const T  = targetFinalPrice.value   // 目标最终含税报价
  const targetSubtotal = (Number.isFinite(T) && R > 0) ? (T / R) : 0
  const subTarget = Math.max(0, targetSubtotal - hw)

  // ===== 6 项按权重分配 subTarget =====
  const out = amountItems.map(it => {
    const weight = subCurrent > 0 ? it.current / subCurrent : 0
    const target = subCurrent > 0 ? subTarget * weight : 0
    return { ...it, weight, target, delta: target - it.current }
  })

  return {
    amountItems: out,
    subCurrent,
    subTarget,
  }
})

// ====== 卡片汇总数据 ======

const designLaborCost = computed(() => {
  if (!props.summary) return 0
  return (props.summary.labor_details || [])
    .filter((d) => d.labor_type === 'design')
    .reduce((s, d) => s + (Number(d.total) || 0), 0)
})

const debugLaborCost = computed(() => {
  if (!props.summary) return 0
  return (props.summary.labor_details || [])
    .filter((d) => d.labor_type === 'debug')
    .reduce((s, d) => s + (Number(d.total) || 0), 0)
})

function sumFeesByKeyword(keyword) {
  if (!props.summary || !Array.isArray(props.summary.fees)) return 0
  return props.summary.fees
    .filter((f) => String(f.fee_type || '').includes(keyword))
    .reduce((s, f) => s + (Number(f.amount) || 0), 0)
}

const certificationFeeCost = computed(() => sumFeesByKeyword('认证'))
const projectManagementFee = computed(() => sumFeesByKeyword('管理'))

const profitAmount = computed(() => {
  if (!props.summary) return 0
  const swp = Number(props.summary.subtotal_with_profit) || 0
  const s = Number(props.summary.subtotal) || 0
  return swp - s
})

const targetPriceDelta = computed(() => {
  // 改为基于最终含税报价对比 (原来基于不含税)
  const tp = targetFinalPrice.value
  if (!isFinite(tp)) return 0
  return tp - finalPriceWithTax.value
})

// ====== 费用明细参数 ======

const LABOR_TYPE_LABELS = {
  design: '设计',
  debug: '调试',
  assembly: '装配',
}

const detailPriceRows = computed(() => {
  const rows = []
  const s = props.summary
  if (!s) return rows

  // 1) 物料系数
  const rates = s.fee_rates || { large: 1, standard: 1, other: 1 }
  rows.push({ group: '物料系数', label: '大件系数',        value: `${rates.large || 1}x` })
  rows.push({ group: '物料系数', label: '核心部件系数',    value: `${rates.standard || 1}x` })
  rows.push({ group: '物料系数', label: '其他件系数',      value: `${rates.other || 1}x`, strong: true })

  // 2) 各类工时单价
  const laborDetails = s.labor_details || []
  const seenLabor = new Set()
  for (const l of laborDetails) {
    const key = `${l.name}|${l.labor_type}`
    if (seenLabor.has(key)) continue
    seenLabor.add(key)
    const typeLabel = LABOR_TYPE_LABELS[l.labor_type] || l.labor_type
    rows.push({
      group: '工时单价',
      label: `${l.name} (${typeLabel})`,
      value: `${(l.unit_price || 0).toFixed(2)} 元/h`,
    })
  }
  if (laborDetails.length === 0) {
    rows.push({ group: '工时单价', label: '尚未添加工时', value: '-' })
  }

  // 3) 对外利润率
  rows.push({
    group: '对外利润率',
    label: '对外利润率',
    value: `${((s.profit_rate || 0) * 100).toFixed(2)}%`,
    strong: true,
  })

  // 4) 各类运输单价
  const packingDetails = s.packing_details || []
  if (packingDetails.length === 0) {
    rows.push({ group: '运输单价', label: '尚未添加运输', value: '-' })
  } else {
    for (const p of packingDetails) {
      rows.push({
        group: '运输单价',
        label: p.packing_type_name || '运输',
        value: `${(p.unit_price || 0).toFixed(2)} 元/单位`,
      })
    }
  }

  // 5) 各类差旅人天单价
  const daysDetails = s.person_days_details || []
  if (daysDetails.length === 0) {
    rows.push({ group: '差旅人天单价', label: '尚未添加差旅人天', value: '-' })
  } else {
    for (const d of daysDetails) {
      rows.push({
        group: '差旅人天单价',
        label: d.travel_category_name || '差旅',
        value: `${(d.unit_price || 0).toFixed(2)} 元/人天`,
      })
    }
  }

  // 6) 各类差旅人次交通 + 签证
  const tripDetails = s.person_trip_details || []
  if (tripDetails.length === 0) {
    rows.push({ group: '差旅人次费用', label: '尚未添加差旅人次', value: '-' })
  } else {
    for (const t of tripDetails) {
      rows.push({
        group: '差旅人次费用',
        label: `${t.travel_category_name || '差旅'} 交通`,
        value: `${(t.unit_price || 0).toFixed(2)} 元/人次`,
      })
      if (t.visa_fee && t.visa_fee > 0) {
        rows.push({
          group: '差旅人次费用',
          label: `${t.travel_category_name || '差旅'} 签证`,
          value: `${(t.visa_fee || 0).toFixed(2)} 元/人次`,
        })
      }
    }
  }

  return rows
})

const detailQuantityRows = computed(() => {
  const rows = []
  const s = props.summary
  if (!s) return rows

  // 1) 各类工时人天
  const laborDetails = s.labor_details || []
  const laborByType = {}
  for (const l of laborDetails) {
    const t = l.labor_type || 'design'
    laborByType[t] = (laborByType[t] || 0) + (l.person_days || 0)
  }
  const allLaborTypes = ['design', 'debug', 'assembly']
  for (const t of allLaborTypes) {
    const days = laborByType[t] || 0
    rows.push({
      group: '工时人天',
      label: LABOR_TYPE_LABELS[t] || t,
      value: days > 0 ? `${days.toFixed(2)} 人天` : '-',
    })
  }

  // 2) 各类运输数量
  const packingDetails = s.packing_details || []
  if (packingDetails.length === 0) {
    rows.push({ group: '运输数量', label: '尚未添加运输', value: '-' })
  } else {
    for (const p of packingDetails) {
      rows.push({
        group: '运输数量',
        label: p.packing_type_name || '运输',
        value: `${p.quantity || 0} 单位`,
      })
    }
  }

  // 3) 各类差旅人天
  const daysDetails = s.person_days_details || []
  if (daysDetails.length === 0) {
    rows.push({ group: '差旅人天', label: '尚未添加差旅人天', value: '-' })
  } else {
    for (const d of daysDetails) {
      rows.push({
        group: '差旅人天',
        label: d.travel_category_name || '差旅',
        value: `${(d.person_days || 0).toFixed(2)} 人天`,
      })
    }
  }

  // 4) 各类差旅人次
  const tripDetails = s.person_trip_details || []
  if (tripDetails.length === 0) {
    rows.push({ group: '差旅人次', label: '尚未添加差旅人次', value: '-' })
  } else {
    for (const t of tripDetails) {
      rows.push({
        group: '差旅人次',
        label: t.travel_category_name || '差旅',
        value: `${(t.person_count || 0).toFixed(0)} 人次`,
        strong: true,
      })
    }
  }

  return rows
})
</script>

<style scoped>
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

/* ===== 汇总头部双行 10 卡片 ===== */
.summary-top-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: var(--spacing-xl);
}

.summary-row-cards {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
}

.summary-mini-card {
  background: var(--color-bg-hover);
  border: 1px solid var(--color-border-light);
  border-radius: 10px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  position: relative;
  border-left: 4px solid var(--color-primary);
  min-height: 100px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.summary-mini-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.summary-mini-icon {
  font-size: 22px;
  margin-bottom: 2px;
}

.summary-mini-label {
  font-size: 13px;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.summary-mini-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-primary);
  font-family: monospace;
  line-height: 1.2;
}

.summary-mini-value.huge {
  font-size: 28px;
  color: #1d4ed8;
  letter-spacing: -0.5px;
}

.summary-mini-value.highlight {
  color: #0f766e;
}

.summary-mini-sub {
  font-size: 12px;
  color: var(--color-text-muted);
  margin-top: 2px;
}

.summary-mini-card.card-hardware { border-left-color: #0d9488; }
.summary-mini-card.card-design { border-left-color: #6366f1; }
.summary-mini-card.card-debug { border-left-color: #ec4899; }
.summary-mini-card.card-travel-days { border-left-color: #f59e0b; }
.summary-mini-card.card-cert { border-left-color: #14b8a6; }
.summary-mini-card.card-travel-trips { border-left-color: #3b82f6; }
.summary-mini-card.card-mgmt { border-left-color: #8b5cf6; }
.summary-mini-card.card-profit { border-left-color: #10b981; }
.summary-mini-card.card-packing { border-left-color: #f97316; }

.summary-mini-card.card-grand-total {
  background: linear-gradient(135deg, #eff6ff, #dbeafe);
  border: 2px solid #3b82f6;
  border-left: 6px solid #1d4ed8;
  box-shadow: 0 2px 8px rgba(29, 78, 216, 0.12);
}

.summary-mini-card.card-grand-total .summary-mini-label {
  color: #1d4ed8;
  font-weight: 600;
}

/* 占比分析区块 */
.breakdown-section {
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-lg);
  border-top: 1px dashed rgba(0,0,0,0.08);
}

.breakdown-section .section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-md) 0;
}

.breakdown-section .section-subtitle {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin: var(--spacing-lg) 0 var(--spacing-sm) 0;
}

/* 硬件成本结构 */
.hardware-structure {
  margin-top: var(--spacing-lg);
}

.hardware-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.hardware-card {
  background: var(--color-bg-hover);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  position: relative;
}

.hardware-card .hardware-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-bottom: 6px;
}

.hardware-card .dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}

.hardware-card.cat-large .dot { background: #0D9488; }
.hardware-card.cat-standard .dot { background: #6366F1; }
.hardware-card.cat-other .dot { background: #F59E0B; }
.hardware-card.cat-large { border-left: 3px solid #0D9488; }
.hardware-card.cat-standard { border-left: 3px solid #6366F1; }
.hardware-card.cat-other { border-left: 3px solid #F59E0B; }

.hardware-amount {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1.2;
}

.hardware-percent {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-primary);
  margin-top: 4px;
}

.hardware-percent .ratio-of {
  font-size: 11px;
  color: var(--color-text-secondary);
  font-weight: 400;
  margin-left: 2px;
}

.hardware-bar {
  margin-top: 8px;
  height: 5px;
  background: rgba(0,0,0,0.06);
  border-radius: 3px;
  overflow: hidden;
}

.hardware-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.4s ease;
}

.hardware-card.cat-large .hardware-bar-fill { background: #0D9488; }
.hardware-card.cat-standard .hardware-bar-fill { background: #6366F1; }
.hardware-card.cat-other .hardware-bar-fill { background: #F59E0B; }

.hardware-meta {
  font-size: 11px;
  color: var(--color-text-secondary);
  margin-top: 6px;
}

.hardware-stacked-bar {
  display: flex;
  height: 14px;
  border-radius: 7px;
  overflow: hidden;
  background: rgba(0,0,0,0.04);
}

.stacked-segment {
  height: 100%;
  transition: width 0.4s ease;
}

.stacked-segment.cat-large { background: #0D9488; }
.stacked-segment.cat-standard { background: #6366F1; }
.stacked-segment.cat-other { background: #F59E0B; }

/* ====== 目标调价 ====== */
.target-price-cards {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 12px;
  margin-top: 12px;
}

.target-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-height: 160px;
  position: relative;
}

.target-card-editable {
  background: linear-gradient(135deg, #fffbeb, #fef3c7);
  border-color: #fbbf24;
}

.target-card-wide {
  grid-column: span 2;
  min-height: auto;
}

.target-card-highlight {
  background: linear-gradient(135deg, #eff6ff, #dbeafe);
  border-color: #3b82f6;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
}

.target-label {
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.editable-tag {
  background: #fbbf24;
  color: #78350f;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 4px;
}

.target-value {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.2;
}

.target-value.huge {
  font-size: 26px;
  color: #1d4ed8;
}

.target-value.highlight {
  color: #0f766e;
}

.target-ratio-text {
  font-size: 16px;
  font-weight: 600;
  color: #475569;
}

.target-meta {
  font-size: 13px;
  color: #475569;
}

.target-meta strong {
  color: #1e293b;
  font-weight: 700;
  font-size: 14px;
}

.target-bar {
  position: relative;
  width: 100%;
  height: 8px;
  background: #f1f5f9;
  border-radius: 4px;
  overflow: hidden;
  margin-top: 4px;
}

.target-bar-fill {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  background: linear-gradient(90deg, #0d9488, #14b8a6);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.target-bar-fill.cat-large { background: linear-gradient(90deg, #0d9488, #14b8a6); }
.target-bar-fill.cat-standard { background: linear-gradient(90deg, #6366f1, #818cf8); }
.target-bar-fill.cat-other { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.target-bar-fill.cat-mechanical { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
.target-bar-fill.cat-electrical { background: linear-gradient(90deg, #f97316, #fb923c); }
.target-bar-fill.target-bar-blue { background: linear-gradient(90deg, #3b82f6, #2563eb); }

.target-sub-meta {
  font-size: 12px;
  color: #94a3b8;
  border-top: 1px dashed #e2e8f0;
  padding-top: 6px;
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.delta {
  font-weight: 600;
  font-family: monospace;
  margin-left: 6px;
}
.delta-pos { color: #16a34a; }
.delta-neg { color: #dc2626; }

.coef-new {
  font-weight: 700;
  font-family: monospace;
}
.coef-new.cat-large { color: #0d9488; }
.coef-new.cat-standard { color: #6366f1; }
.coef-new.cat-other { color: #f59e0b; }

.uplift-amt {
  font-weight: 600;
  font-family: monospace;
}
.uplift-pos { color: #16a34a; }
.uplift-neg { color: #dc2626; }

.target-input-wrap {
  margin: 4px 0;
}

@media (max-width: 1440px) {
  .target-price-cards { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 900px) {
  .target-price-cards { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 600px) {
  .target-price-cards { grid-template-columns: 1fr; }
}

/* 模块汇总 */
.summary-modules-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-top: 12px;
}

@media (max-width: 760px) {
  .summary-modules-grid {
    grid-template-columns: 1fr;
  }
}

.module-type-group {
  margin-bottom: 24px;
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--color-bg-card);
}

.module-type-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  background: var(--color-bg-hover);
  border-bottom: 2px solid var(--color-border-light);
}
.module-type-header.type-mechanical { border-bottom-color: #3b82f6; }
.module-type-header.type-electrical { border-bottom-color: #f59e0b; }
.module-type-header.type-other { border-bottom-color: #94a3b8; }

.module-type-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #fff;
}
.module-type-icon.type-mechanical { background: #3b82f6; }
.module-type-icon.type-electrical { background: #f59e0b; }
.module-type-icon.type-other { background: #94a3b8; }

.module-type-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.module-type-count {
  padding: 2px 10px;
  border-radius: 12px;
  background: var(--color-bg-hover);
  color: var(--color-text-secondary);
  font-size: 12px;
  font-weight: 500;
}

.summary-module-card {
  display: flex;
  flex-direction: column;
  margin-bottom: 0;
}

.summary-module-card .module-type-header {
  flex-shrink: 0;
}

.summary-module-card .module-type-stats {
  display: flex;
  flex-direction: column;
  padding: 14px 18px;
  background: var(--color-bg-card);
  border-bottom: 1px solid var(--color-border-light);
  flex-shrink: 0;
}

.module-type-stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px 0;
  font-size: 13px;
}
.module-type-stat-row .stat-label {
  color: var(--color-text-secondary);
}
.module-type-stat-row .stat-value {
  font-weight: 600;
  color: var(--color-text-primary);
  font-family: monospace;
}
.module-type-stat-row.highlight {
  margin-top: 4px;
  padding-top: 8px;
  border-top: 1px dashed var(--color-border-light);
}

.module-type-table-wrapper {
  flex: 1;
  padding: 12px;
  background: var(--color-bg-card);
  overflow: hidden;
}

.module-type-table-wrapper .el-table {
  border-radius: 6px;
}

.module-type-table-wrapper .el-table .cell {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cell-name-wrap {
  display: flex;
  align-items: center;
  gap: 3px;
  min-width: 0;
  max-width: 100%;
  overflow: hidden;
}

.cell-module-name {
  font-weight: 600;
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
  min-width: 0;
}

.cell-amount {
  font-family: monospace;
  font-weight: 500;
  color: var(--color-text-primary);
}
.cell-amount.highlight {
  color: var(--color-primary);
  font-weight: 700;
}

/* 费用明细参数 2 卡片 */
.coefficient-detail-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-top: 12px;
}

.coefficient-detail-section .detail-card {
  background: var(--color-bg-card, #ffffff);
  border: 1px solid var(--color-border, #e2e8f0);
  border-radius: 8px;
  overflow: hidden;
}

.coefficient-detail-section .detail-card-header {
  background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
  padding: 12px 16px;
  border-bottom: 1px solid var(--color-border, #e2e8f0);
}

.coefficient-detail-section .detail-card-header h4 {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text-primary, #1e293b);
}

.coefficient-detail-section .value-strong {
  font-weight: 600;
  color: var(--color-primary, #3b82f6);
}

@media (max-width: 900px) {
  .coefficient-detail-section { grid-template-columns: 1fr; }
}
</style>
