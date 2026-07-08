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
    <div class="edit-card" v-loading="pageLoading" element-loading-text="页面加载中...">
      <el-tabs v-model="activeTab">
        <!-- 基本信息 -->
        <el-tab-pane label="基本信息" name="basic">
          <QuotationEditBasicTab
            :quotation="quotation"
            :form-rules="formRules"
            :is-edit="isEdit"
            :parent-id="parentId"
            :saving-basic="savingBasic"
            :business-users="businessUsers"
            :currency-options="currencyOptions"
            :scheme-hint="schemeHint"
            :scheme-hint-type="schemeHintType"
            :scheme-suggestions="schemeSuggestions"
            @save-basic="saveBasic"
            @save-profit-rate="saveProfitRate"
            @select-scheme="handleSelectScheme"
            @scheme-input="onSchemeInput"
            @validate-scheme="validateSchemeLocally"
          />
        </el-tab-pane>

        <!-- 模块管理 -->
        <el-tab-pane v-if="isEdit" label="模块管理" name="modules">
          <QuotationEditModulesTab
            :modules="modules"
            :module-types="MODULE_TYPES"
            :module-form="moduleForm"
            :module-dialog-visible="moduleDialogVisible"
            :module-dialog-title="moduleDialogTitle"
            :participants-count="currentParticipants.length"
            @add-module="showAddModule"
            @edit-module="editModule"
            @delete-module="deleteModule"
            @save-module="saveModule"
            @infer-type="inferModuleType"
            @cancel-dialog="moduleDialogVisible = false"
            @update:dialog-visible="moduleDialogVisible = $event"
          />
        </el-tab-pane>

        <!-- 参与人员 -->
        <el-tab-pane v-if="isEdit" label="参与人员" name="participants">
          <QuotationEditParticipantsTab
            :participants="quotationParticipants"
            :participant-types="participantTypes"
            :dialog-visible="addParticipantDialogVisible"
            :loading="participantLoading"
            :available-users="users"
            :participant-search="participantSearch"
            :selected-participant-type="selectedParticipantType"
            :selected-count="selectedParticipantUsers.length"
            :check-selectable="checkParticipantSelectable"
            @add-participant="showAddParticipantDialog"
            @remove-participant="removeQuotationParticipant"
            @confirm-add="addParticipantsConfirm"
            @cancel-dialog="addParticipantDialogVisible = false"
            @type-change="updateParticipantType"
            @update:visible="addParticipantDialogVisible = $event"
            @update:search="participantSearch = $event"
            @update:type="selectedParticipantType = $event"
            @update:selected="selectedParticipantUsers = $event"
          />
        </el-tab-pane>

        <!-- 费用系数 -->
        <el-tab-pane v-if="isEdit" label="费用系数" name="coefficients">
          <QuotationEditCoefficientsTab
            :coefficients="quotation.coefficients"
            :saving="savingCoeff"
            @save="saveCoefficients"
            @reset="resetCoefficientsToDefault"
          />
        </el-tab-pane>

        <!-- 物料清单 -->
        <el-tab-pane v-if="isEdit" label="物料清单" name="materials">
          <QuotationEditMaterials
            :is-edit="isEdit"
            :module-materials="moduleMaterials"
            :grouped-materials="groupedModulesByType"
            :all-materials-total="allMaterialsTotal"
            :selected-currency="selectedCurrency"
            :exchange-rates="exchangeRates"
            :module-types="MODULE_TYPES"
            :dispatch-group-info="dispatchGroupInfo"
            :is-archived="isArchived"
            :modules="modules"
            :available-materials="availableMaterials"
            :material-total="materialTotal"
            :has-key-fields="hasKeyFields"
            :material-has-key-params="materialHasKeyParams"
            :selected-module-filter="selectedModuleFilter"
            @update:selected-module-filter="selectedModuleFilter = $event"
            @update-quantity="updateMaterialQuantity"
            @delete-material="deleteModuleMaterial"
            @add-materials="handleAddMaterials"
            @save-other-price="handleSaveOtherPrice"
            @load-materials="handleLoadMaterials"
          />
        </el-tab-pane>

        <!-- 费用 -->
        <el-tab-pane v-if="isEdit" label="费用" name="fees">
          <QuotationEditFeesTab
            :fees="fees"
            :fee-types="feeTypes"
            :fee-form="feeForm"
            :dialog-visible="feeDialogVisible"
            :dialog-title="feeDialogTitle"
            @add-fee="showAddFee"
            @edit-fee="editFee"
            @delete-fee="deleteFee"
            @save-fee="saveFee"
            @cancel-dialog="feeDialogVisible = false"
            @update:visible="feeDialogVisible = $event"
          />
        </el-tab-pane>

        <!-- 人力工时 -->
        <el-tab-pane v-if="isEdit" label="人力工时" name="labor">
          <QuotationEditLaborTab
            :labor-hours="laborHours"
            :labor-total="laborTotal"
            :labor-form="laborForm"
            :labor-type-choices="LABOR_TYPE_CHOICES"
            :labor-name-choices="LABOR_NAME_CHOICES"
            :hours-per-day="HOURS_PER_DAY"
            :dialog-visible="laborDialogVisible"
            @add-labor="showAddLabor"
            @edit-row="editLaborRow"
            @save-row="saveLaborRow"
            @cancel-edit="cancelLaborEdit"
            @delete-row="deleteLabor"
            @confirm-add="addLaborConfirm"
            @cancel-dialog="laborDialogVisible = false"
            @update:visible="laborDialogVisible = $event"
            @row-name-change="onRowNameChange"
            @row-hours-change="onRowHoursChange"
            @row-person-days-change="onRowPersonDaysChange"
            @row-unit-price-change="onRowUnitPriceChange"
            @name-change="onLaborNameChange"
            @hours-change="onHoursChange"
            @person-days-change="onPersonDaysChange"
            @unit-price-change="onLaborUnitPriceChange"
          />
        </el-tab-pane>

        <!-- 运输包装 -->
        <el-tab-pane v-if="isEdit" label="运输包装" name="packing">
          <QuotationEditPackingTab
            :entries="packingEntries"
            :total="packingTotal"
            :packing-types="packingTypes"
            :form="packingForm"
            :dialog-visible="packingDialogVisible"
            @add-entry="showAddPackingEntry"
            @edit-row="editPackingRow"
            @save-row="savePackingRow"
            @cancel-edit="cancelPackingEdit"
            @delete-entry="deletePackingEntry"
            @confirm-add="addPackingConfirm"
            @cancel-dialog="packingDialogVisible = false"
            @update:visible="packingDialogVisible = $event"
            @type-change="onPackingTypeChange"
            @quantity-change="(v) => packingForm.quantity = v"
            @remark-change="(v) => packingForm.remark = v"
            @row-unit-price-change="onRowUnitPriceChange"
            @row-quantity-change="onRowQuantityChange"
          />
        </el-tab-pane>

        <!-- 差旅人天 -->
        <el-tab-pane v-if="isEdit" label="差旅人天" name="travel-days">
          <QuotationEditTravelDaysTab
            :entries="travelPersonDays"
            :total="travelDaysTotal"
            :categories="travelCategories"
            :form="travelDaysForm"
            :dialog-visible="travelDaysDialogVisible"
            @add-entry="showAddTravelDaysEntry"
            @edit-row="editTravelDaysRow"
            @save-row="saveTravelDaysRow"
            @cancel-edit="cancelTravelDaysEdit"
            @delete-entry="deleteTravelDaysEntry"
            @confirm-add="addTravelDaysConfirm"
            @cancel-dialog="travelDaysDialogVisible = false"
            @update:visible="travelDaysDialogVisible = $event"
            @category-change="onTravelCategoryChange"
            @person-days-change="(v) => travelDaysForm.person_days = v"
            @remark-change="(v) => travelDaysForm.remark = v"
            @row-unit-price-change="onRowUnitPriceChange"
            @row-person-days-change="onRowPersonDaysChange"
          />
        </el-tab-pane>

        <!-- 差旅人次 -->
        <el-tab-pane v-if="isEdit" label="差旅人次" name="travel-trips">
          <QuotationEditTravelTripsTab
            :entries="travelPersonTrips"
            :total="travelTripsTotal"
            :categories="travelCategories"
            :modes="travelModes"
            :form="travelTripForm"
            :dialog-visible="travelTripDialogVisible"
            @add-entry="showAddTravelTripEntry"
            @edit-row="editTravelTripRow"
            @save-row="saveTravelTripRow"
            @cancel-edit="cancelTravelTripEdit"
            @delete-entry="deleteTravelTripEntry"
            @confirm-add="addTravelTripConfirm"
            @cancel-dialog="travelTripDialogVisible = false"
            @update:visible="travelTripDialogVisible = $event"
            @category-change="onTripCategoryChange"
            @mode-change="onTripModeChange"
            @person-count-change="(v) => travelTripForm.person_count = v"
            @remark-change="(v) => travelTripForm.remark = v"
            @row-unit-price-change="onRowUnitPriceChange"
            @row-visa-fee-change="onRowVisaFeeChange"
            @row-person-count-change="onRowPersonCountChange"
          />
        </el-tab-pane>

        <!-- 汇总 -->
        <el-tab-pane v-if="isEdit" label="汇总" name="summary">
          <QuotationEditSummary
            :summary="summary"
            :summary-loading="summaryLoading"
            ref="summaryCompRef"
            :selected-currency="selectedCurrency"
            :exchange-rates="exchangeRates"
            :exchange-rate-symbol="''"
            :grouped-summary-modules-by-type="groupedSummaryModulesByType"
            :all-modules-count="allModulesCount || 0"
            @update:selectedCurrency="selectedCurrency = $event"
          />
        </el-tab-pane>

        <!-- 版本 -->
        <el-tab-pane v-if="isEdit" label="版本" name="versions">
          <QuotationEditVersionsTab :versions="versions" @export-version="exportVersion" />
        </el-tab-pane>

        <!-- 导出 -->
        <el-tab-pane v-if="isEdit" label="导出" name="export">
          <QuotationEditExportTab @export-file="exportFile" @export-summary-pdf="exportSummaryAsPDF" />
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../api/request'
import { openDownload } from '../utils/download'
import { feesAPI, packingTypeAPI, travelCategoryAPI, travelModeAPI, travelPersonTripFeeAPI, quotationsAPI } from '../api'
import { packingEntryAPI, travelPersonDaysAPI, travelPersonTripAPI } from '../api/travel_entries'
import QuotationEditSaveBar from '@/components/QuotationEditSaveBar.vue'
import QuotationEditBasicTab from '@/components/QuotationEditBasicTab.vue'
import QuotationEditModulesTab from '@/components/QuotationEditModulesTab.vue'
import QuotationEditParticipantsTab from '@/components/QuotationEditParticipantsTab.vue'
import QuotationEditCoefficientsTab from '@/components/QuotationEditCoefficientsTab.vue'
import QuotationEditFeesTab from '@/components/QuotationEditFeesTab.vue'
import QuotationEditLaborTab from '@/components/QuotationEditLaborTab.vue'
import QuotationEditPackingTab from '@/components/QuotationEditPackingTab.vue'
import QuotationEditTravelDaysTab from '@/components/QuotationEditTravelDaysTab.vue'
import QuotationEditTravelTripsTab from '@/components/QuotationEditTravelTripsTab.vue'
import QuotationEditVersionsTab from '@/components/QuotationEditVersionsTab.vue'
import QuotationEditExportTab from '@/components/QuotationEditExportTab.vue'
import QuotationEditMaterials from '@/components/QuotationEditMaterials.vue'
import QuotationEditSummary from '@/components/QuotationEditSummary.vue'
import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'

const route = useRoute()
const router = useRouter()

console.log('Route params:', route.params)
console.log('Route path:', route.path)

// 判断是新建还是编辑
const isEdit = computed(() => !!route.params.id && route.params.id !== 'new')
const quotationId = ref(route.params.id || null)
const savingBasic = ref(false)
const savingCoeff = ref(false)
const parentId = ref(route.query.parent_id ? parseInt(route.query.parent_id) : null)
console.log('isEdit:', isEdit.value, 'quotationId:', quotationId.value, 'parentId:', parentId.value)
const activeTab = ref('basic')
const quotation = ref({ coefficients: { large: 1.0, standard: 1.0, other: 1.0 } })
const isArchived = computed(() => quotation.value.status === 'approved')

// 方案号联动查询 - 状态
const schemeSuggestions = ref([])
const schemeHint = ref('')
const schemeHintType = ref('info')  // info/success/warning/danger
let schemeSearchController = null  // 用于取消正在飞行的请求
let schemeSearchReqId = 0  // 请求序号，最新的胜出
const SCHEME_MIN_LEN = 2
// 记录从方案库自动填了哪些字段（手动改方案号时一并清空）
const autoFilledFields = ref([])

// 方案号输入：立刻发请求（取消上一次在飞的请求）
// 不需要 debounce：axios + AbortController 保证只有最新请求的响应被采纳
// 后端响应 200ms 内，立刻查比 debounce 500ms 体验更好
function onSchemeInput(value) {
  schemeHint.value = ''
  // 用户改方案号 → 清掉上次自动填的字段
  if (autoFilledFields.value.length) {
    for (const f of autoFilledFields.value) {
      if (f === 'name') quotation.value.name = ''
      if (f === 'business_owner_id') quotation.value.business_owner_id = null
    }
    autoFilledFields.value = []
  }
  if (!value || value.length < SCHEME_MIN_LEN) {
    schemeSuggestions.value = []
    return
  }
  fetchSchemeSuggestions(value)
}

// 真正发请求的函数：先取消上一次未完成的请求，再发新请求
async function fetchSchemeSuggestions(prefix) {
  if (!prefix || prefix.length < SCHEME_MIN_LEN) {
    schemeSuggestions.value = []
    return
  }
  // 1) 取消上一次还在飞的请求（避免响应顺序错乱、节省后端和外部接口的查询）
  if (schemeSearchController) {
    schemeSearchController.abort()
  }
  // 2) 用新的 controller 发本次请求
  const controller = new AbortController()
  schemeSearchController = controller
  // 3) 请求序号自增，本次调用结束前若序号变了，说明已被新请求取代
  const myReqId = ++schemeSearchReqId
  try {
    const data = await api.get('/quotations/scheme-search', {
      params: { prefix },
      signal: controller.signal
    })
    // 已被新请求取代 → 丢弃结果
    if (myReqId !== schemeSearchReqId) return
    schemeSuggestions.value = data.items || []
  } catch (error) {
    // 主动取消的请求不算错误（axios 抛 CanceledError，code=ERR_CANCELED）
    const isCanceled = error?.name === 'CanceledError' || error?.code === 'ERR_CANCELED'
    if (isCanceled) return
    if (myReqId !== schemeSearchReqId) return
    console.warn('方案号查询失败:', error)
    schemeSuggestions.value = []
  }
}

// el-autocomplete 的 fetch-suggestions 入口：返回当前缓存
// 真正的查询由 onSchemeInput 触发，结果写入 schemeSuggestions
function querySchemeSuggestions(queryString, callback) {
  callback(schemeSuggestions.value)
}

// 子组件透传：autocomplete 的 (cb, prefix) → 父级 querySchemeSuggestions
function handleQuerySchemeSuggestions(cb, prefix) {
  querySchemeSuggestions(prefix, cb)
}

// 选中下拉项：自动填名称 + 业务负责人（如果方案库提供了）
function handleSelectScheme(item) {
  schemeHint.value = ''
  if (item.is_used_locally) {
    schemeHint.value = `⚠ 方案号 "${item.schemeNo}" 已被本系统使用，保存会被拒绝`
    schemeHintType.value = 'danger'
    return  // 不自动填任何字段，避免覆盖用户已输入
  }
  // 1) 自动填报价单名称（名称为空时填，避免覆盖用户已输入）
  if (item.schemeName && !quotation.value.name) {
    quotation.value.name = item.schemeName
    autoFilledFields.value.push('name')
  }
  // 2) 自动选业务负责人（如果方案库提供了，且本系统里有该工号对应的用户）
  if (item.businessManager) {
    // RS8139 是方案库的「业务经理工号」，本系统的 User.username/RS 号是同一个值
    // User 表没有 employee_no 字段（employee_id 是 FK，但 RS 号就是 username）
    const matchedUser = businessUsers.value.find(u =>
      String(u.username) === item.businessManager ||
      String(u.employee_no) === item.businessManager
    )
    if (matchedUser && !quotation.value.business_owner_id) {
      quotation.value.business_owner_id = matchedUser.id
      autoFilledFields.value.push('business_owner_id')
    }
  }
  // 3) 提示
  const parts = [`已选中：${item.schemeNo} - ${item.schemeName || '(无名称)'}`]
  if (quotation.value.name === item.schemeName) parts.push('名称已自动填入')
  if (quotation.value.business_owner_id) parts.push('业务负责人已自动填入')
  schemeHint.value = parts.join('；')
  schemeHintType.value = 'success'
}

// 失焦时本地预校验（节省一次后端往返；后端 400 仍兜底）
async function validateSchemeLocally() {
  const sn = quotation.value.scheme_no
  if (!sn || parentId.value) {
    schemeHint.value = ''
    return
  }
  // 用本地下拉结果判断（如果下拉为空 → 外部库没这个号；下拉有且 is_used_locally → 被占用）
  const hit = schemeSuggestions.value.find(s => s.schemeNo === sn)
  if (hit && hit.is_used_locally) {
    schemeHint.value = `⚠ 方案号 "${sn}" 已被本系统使用，保存会被拒绝`
    schemeHintType.value = 'danger'
  } else if (hit) {
    schemeHint.value = `✓ 方案号可用（来自方案库：${hit.schemeName || '无名称'}）`
    schemeHintType.value = 'success'
  } else {
    schemeHint.value = ''
  }
}
const hasKeyFields = computed(() => {
  return modules.value.some(mod =>
    mod.materials && mod.materials.some(m => m.param1 || m.param2 || m.param3)
  )
})
const materialHasKeyParams = computed(() => {
  return availableMaterials.value.some(m => m.param1 || m.param2 || m.param3)
})
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
// 汇总 tab 组件引用 (用于刷新汇总数据 + 导出 PDF)
const summaryCompRef = ref(null)
// 分页状态 (服务端分页)
const materialPage = ref(1)
const materialPageSize = ref(50)
const materialTotal = ref(0)

// 三大新费用数据
const packingEntries = ref([])
const travelPersonDays = ref([])
const travelPersonTrips = ref([])
const packingTypes = ref([])
const travelCategories = ref([])
const travelModes = ref([])
// 全部差旅人次单价配置 (category × mode → unit_price + visa_fee), 前端本地查
const travelPersonTripFees = ref([])

const selectedModuleId = ref(null)
const pageLoading = ref(true)
const summaryLoading = ref(false)
const summaryRef = ref(null)

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
  const map = { large: '大件', standard: '核心部件', other: '其他件' }
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

// 运输+差旅合计（运输包装 + 差旅人天 + 差旅人次）
const totalTravelAmount = computed(() => {
  if (!summary.value) return 0
  const packing = summary.value.packing_total || 0
  const days = summary.value.travel_person_days_total || 0
  const trips = summary.value.travel_person_trips_total || 0
  return packing + days + trips
})

// 占比计算：含利润小计为分母 (精确到小数点后两位)
function getRatio(amount) {
  if (!summary.value || !amount) return '0.00'
  const denom = summary.value.subtotal_with_profit || 0
  if (denom === 0) return '0.00'
  return ((amount / denom) * 100).toFixed(2)
}

// 硬件分类占比：material_total_with_rates 为分母 (精确到小数点后两位)
function getMaterialCategoryRatio(amount) {
  if (!summary.value || !amount) return '0.00'
  const denom = summary.value.material_total_with_rates || 0
  if (denom === 0) return '0.00'
  return ((amount / denom) * 100).toFixed(2)
}

// ====== 目标调价 (联动目标硬件占比) ======
const targetHardwareRatio = ref(null)
const targetHardwareManuallySet = ref(false)

const actualHardwareRatioPercent = computed(() => {
  if (!summary.value) return 0
  const hw = summary.value.material_total_with_rates || 0
  const denom = (summary.value.subtotal || 0)
  if (denom === 0) return 0
  return (hw / denom) * 100
})

const largeHardwareAmount = computed(() => {
  if (!summary.value) return 0
  const rows = summary.value.rate_details || []
  const r = rows.find(x => x.category === 'large')
  return r ? (r.with_rate || 0) : 0
})

const largeHardwareRatioPercent = computed(() => {
  if (!summary.value) return 0
  const denom = summary.value.material_total_with_rates || 0
  if (denom === 0) return 0
  return (largeHardwareAmount.value / denom) * 100
})

const moduleTypeRatio = computed(() => {
  if (!summary.value) return { mech: 0, elec: 0, label: '0 : 0' }
  let mech = 0, elec = 0
  for (const sm of (summary.value.modules || [])) {
    const amt = sm.material_amount_with_rate || sm.material_amount || 0
    if (sm.module_type === 'mechanical') mech += amt
    else if (sm.module_type === 'electrical') elec += amt
  }
  return { mech, elec, label: elec > 0 ? `${mech.toFixed(0)} : ${elec.toFixed(0)} ≈ ${(mech / elec).toFixed(2)}` : (mech > 0 ? `机械 ${mech.toFixed(0)} / 无电控模块` : '暂无模块') }
})

const noTaxPrice = computed(() => {
  if (!summary.value) return 0
  return summary.value.subtotal || 0
})

const finalPriceWithTax = computed(() => {
  if (!summary.value) return 0
  return summary.value.final_price_with_tax || summary.value.subtotal_with_profit_with_tax || 0
})

watch(actualHardwareRatioPercent, (newVal) => {
  if (newVal > 0 && !targetHardwareManuallySet.value) {
    targetHardwareRatio.value = Number(newVal.toFixed(2))
  }
}, { immediate: true })

const targetPrice = computed(() => {
  // 调整目标硬件占比后, 目标含税报价 (基于不含税小计反推):
  // 假设: 人力 + 运输 + 差旅 (其他成本) 保持不变, 通过调整物料系数使硬件占比达到目标值。
  // 设 other = 当前 subtotal - 当前物料含系数 (其他成本, 固定)
  // 则: target_subtotal - other = target_subtotal × targetRatio
  // 即: target_subtotal = other / (1 - targetRatio)
  // 调高占比 → target_subtotal 增大 → targetPrice 升 ✅
  const ratio = Number(targetHardwareRatio.value || 0)
  if (ratio <= 0 || !summary.value) return 0
  if (ratio >= 100) return 0
  const hw = summary.value.material_total_with_rates || 0
  const sub = noTaxPrice.value || 0
  if (sub <= 0) return 0
  const other = sub - hw
  return other / (1 - ratio / 100)
})

const targetHardwareAtTarget = computed(() => {
  const tp = targetPrice.value
  const ratio = Number(targetHardwareRatio.value || 0)
  return (tp * ratio / 100) || 0
})

const targetHardwareUplift = computed(() => {
  if (!summary.value) return 0
  const cur = summary.value.material_total_with_rates || 0
  return targetHardwareAtTarget.value - cur
})

// 各分类 (大件/核心部件/其他件) 的建议系数 - 按现有 base 占比分配调整量
const categoryCoefficients = computed(() => {
  if (!summary.value) return []
  const rows = summary.value.rate_details || []
  const totalBase = rows.reduce((sum, r) => sum + (r.base || 0), 0)
  const totalCurrentWithRate = rows.reduce((sum, r) => sum + (r.with_rate || 0), 0)
  if (totalBase <= 0) return []

  const targetHW = targetHardwareAtTarget.value
  const adjustment = targetHW - totalCurrentWithRate

  const out = []
  for (const r of rows) {
    const cur_base = r.base || 0
    const cur_with_rate = r.with_rate || 0
    const cur_rate = r.rate || 1
    const weight = cur_base / totalBase
    const uplift = adjustment * weight
    const new_with_rate = Math.max(0, cur_with_rate + uplift)
    const new_rate = cur_base > 0 ? new_with_rate / cur_base : cur_rate
    out.push({
      category: r.category,
      label: r.category === 'large' ? '大件' : r.category === 'standard' ? '核心部件' : '其他件',
      cat_class: 'cat-' + r.category,
      base: cur_base,
      current_with_rate: cur_with_rate,
      current_rate: cur_rate,
      new_with_rate,
      new_rate,
      uplift,
    })
  }
  return out
})

// ====== 汇总头部双行 10 卡片汇总数据 ======
// 设计人力成本: 各类设计工时 total 之和
const designLaborCost = computed(() => {
  if (!summary.value) return 0
  return (summary.value.labor_details || [])
    .filter((d) => d.labor_type === 'design')
    .reduce((s, d) => s + (Number(d.total) || 0), 0)
})

// 调试人力成本: 各类调试工时 total 之和
const debugLaborCost = computed(() => {
  if (!summary.value) return 0
  return (summary.value.labor_details || [])
    .filter((d) => d.labor_type === 'debug')
    .reduce((s, d) => s + (Number(d.total) || 0), 0)
})

// 按费用类型关键词过滤金额合计
function sumFeesByKeyword(keyword) {
  if (!summary.value || !Array.isArray(summary.value.fees)) return 0
  return summary.value.fees
    .filter((f) => String(f.fee_type || '').includes(keyword))
    .reduce((s, f) => s + (Number(f.amount) || 0), 0)
}

// 认证费用成本: fee_type 包含"认证"
const certificationFeeCost = computed(() => sumFeesByKeyword('认证'))

// 项目管理费用: fee_type 包含"管理"
const projectManagementFee = computed(() => sumFeesByKeyword('管理'))

// 项目利润 (对外利润 = subtotal * profit_rate)
const profitAmount = computed(() => {
  if (!summary.value) return 0
  const swp = Number(summary.value.subtotal_with_profit) || 0
  const s = Number(summary.value.subtotal) || 0
  return swp - s
})

// 第一行 / 第二行卡片通用辅助
const fmtMoney = (v) => `¥${(Number(v) || 0).toFixed(2)}`

const targetPriceDelta = computed(() => {
  return targetPrice.value - noTaxPrice.value
})

function onTargetHardwareRatioInput(val) {
  targetHardwareManuallySet.value = true
  targetHardwareRatio.value = Number(val) || 0
}

function resetTargetHardwareRatio() {
  targetHardwareManuallySet.value = false
  targetHardwareRatio.value = Number(actualHardwareRatioPercent.value.toFixed(2))
}

// 费用明细参数 (2 卡片) - 数据源 - 与 QuotationView 同步
const LABOR_TYPE_LABELS = {
  design: '设计',
  debug: '调试',
  assembly: '装配',
}

// 卡片 1: 单价 + 系数
const detailPriceRows = computed(() => {
  const rows = []
  const s = summary.value
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

  // 6) 各类差旅人次交通 + 签证费用
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

// 卡片 2: 数量
const detailQuantityRows = computed(() => {
  const rows = []
  const s = summary.value
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
const MODULE_TYPES = [
  { value: 'mechanical', label: '机构', color: '#3b82f6' },
  { value: 'electrical', label: '电气', color: '#f59e0b' },
  { value: 'other', label: '其他', color: '#94a3b8' },
]
const moduleForm = reactive({
  id: null,
  name: '',
  name_en: '',
  description: '',
  module_type: 'other',
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

// 修改其他物料单价弹窗
const otherPriceDialogVisible = ref(false)
const otherPriceForm = reactive({
  id: null,
  material_name: '其他',
  unit_price_override: 0
})

// 动态获取"其他"物料ID（按名称查，避免硬编码）
const otherMaterial = computed(() => {
  return availableMaterials.value.find(m => m.name === '其他')
})

// 服务端分页 + 筛选, 前端不再做客户端过滤 (filteredAvailableMaterials 已废弃)

// 计算属性：可选品牌列表 (从当前页物料中提取, 主要用于 UI 显示)
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
      module_type: mod.module_type,
      module_type_label: mod.module_type_label,
      materials: matList,
      total: matList.reduce((sum, m) => sum + (m.unit_price || 0) * m.quantity, 0)
    }
  })
})

// 按模块类型分组的卡片 (机构/电气/其他) - 用于物料清单 tab
const groupedModulesByType = computed(() => {
  const groups = {}
  for (const t of MODULE_TYPES) {
    groups[t.value] = []
  }
  for (const modGroup of filteredModuleGroups.value) {
    // modGroup.id 实际是 module id; module_type 需要查 modules
    const mod = modules.value.find(m => m.id === modGroup.id)
    const t = (mod?.module_type) || 'other'
    if (!groups[t]) groups[t] = []
    groups[t].push(modGroup)
  }
  // 永远返回 3 个类型 (机构/电气/其他), 没有数据的也显示, 数值默认为 0, 表格为空
  return MODULE_TYPES.map(t => ({
    ...t,
    module_list: groups[t.value] || [],
    group_total: (groups[t.value] || []).reduce((sum, m) => sum + m.total, 0),
    group_materials_count: (groups[t.value] || []).reduce((sum, m) => sum + m.materials.length, 0),
    group_module_count: (groups[t.value] || []).length
  }))
})

// 汇总模块按类型分组 - 用于汇总 tab
const groupedSummaryModulesByType = computed(() => {
  const groups = {}
  for (const t of MODULE_TYPES) {
    groups[t.value] = []
  }
  for (const sm of (summary.value?.modules || [])) {
    const t = sm.module_type || 'other'
    if (!groups[t]) groups[t] = []
    groups[t].push(sm)
  }
  // 永远返回 3 个类型 (机构/电气/其他), 没有数据的也显示, 数值默认为 0, 表格为空
  return MODULE_TYPES.map(t => ({
    ...t,
    module_list: groups[t.value] || [],
    group_total: (groups[t.value] || []).reduce((sum, m) => sum + (m.material_amount || 0), 0),
    group_total_with_rate: (groups[t.value] || []).reduce((sum, m) => sum + (m.material_amount_with_rate || m.material_amount || 0), 0),
    group_materials_count: (groups[t.value] || []).reduce((sum, m) => sum + (m.material_count || 0), 0),
    group_module_count: (groups[t.value] || []).length
  }))
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
const selectedParticipantType = ref('')

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
  selectedParticipantType.value = ''
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
  if (!selectedParticipantUsers.value.length || !selectedParticipantType.value) return
  try {
    for (const user of selectedParticipantUsers.value) {
      await api.post(`/quotations/${quotationId.value}/participants`, {
        user_id: user.id,
        participant_type: selectedParticipantType.value
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
  savingCoeff.value = true
  try {
    await api.put(`/quotations/${quotationId.value}`, {
      coefficients: quotation.value.coefficients
    })
    ElMessage.success('费用系数已保存')
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    savingCoeff.value = false
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
// 8 工时 = 1 人天 (标准 1 天 8 小时)
const HOURS_PER_DAY = 8
// 7 个固定工时名称 (选择后自动匹配工时类型)
const LABOR_NAME_CHOICES = [
  { name: '机械设计',                     labor_type: 'design' },
  { name: '电控编程设计（PLC&HMI）',         labor_type: 'design' },
  { name: '软件编程设计（C#&Vision&robot）', labor_type: 'design' },
  { name: '生产装配',                     labor_type: 'assembly' },
  { name: '机械厂外调试',                 labor_type: 'debug' },
  { name: '电控编程厂外调试（PLC&HMI）',      labor_type: 'debug' },
  { name: '软件编程厂外调试（C#&Vision&robot）', labor_type: 'debug' },
]

const LABOR_TYPE_CHOICES = [
  { value: 'design', label: '设计', color: '#3b82f6' },
  { value: 'debug', label: '调试', color: '#f59e0b' },
  { value: 'assembly', label: '装配', color: '#10b981' },
]
const laborForm = reactive({
  name: '',
  hours: 0,          // 工时 (实际存储)
  person_days: 0,    // 人天 (前端展示,双向换算)
  unit_price: 0,
  labor_type: 'design',  // 默认设计
})

// 工时名称变化 → 自动设置 labor_type
function onLaborNameChange(name) {
  laborForm.name = name
  const choice = LABOR_NAME_CHOICES.find(n => n.name === name)
  if (choice) {
    laborForm.labor_type = choice.labor_type
  }
}

const laborTotal = computed(() => {
  return laborHours.value.reduce((sum, item) => sum + (item.hours || 0) * (item.unit_price || 0), 0)
})

// 人天 ↔ 工时 双向换算
function formatPersonDays(hours) {
  if (!hours) return '0.00'
  return (hours / HOURS_PER_DAY).toFixed(2)
}
function onHoursChange(val) {
  if (val == null) val = 0
  laborForm.person_days = +(val / HOURS_PER_DAY).toFixed(2)
}
function onPersonDaysChange(val) {
  if (val == null) val = 0
  laborForm.hours = +(val * HOURS_PER_DAY).toFixed(1)
}
// 表格行级别换算
function onRowHoursChange(row, val) {
  if (val != null) row._hours = val
  if (row._hours == null) row._hours = 0
  row._person_days = +(row._hours / HOURS_PER_DAY).toFixed(2)
}
function onRowPersonDaysChange(row, val) {
  if (val != null) row._person_days = val
  if (row._person_days == null) row._person_days = 0
  row._hours = +(row._person_days * HOURS_PER_DAY).toFixed(1)
}
function onRowNameChange(row, val) {
  if (val != null) row._name = val
}
function onRowUnitPriceChange(row, val) {
  if (val != null) row._unit_price = val
}
function onRowQuantityChange(row, val) {
  if (val != null) row._quantity = val
}
function onRowVisaFeeChange(row, val) {
  if (val != null) row._visa_fee = val
}
function onRowPersonCountChange(row, val) {
  if (val != null) row._person_count = val
}
function onLaborUnitPriceChange(val) {
  laborForm.unit_price = val
}

// ===== 运输包装 =====
const packingDialogVisible = ref(false)
const packingForm = reactive({ packing_type_id: null, unit_price: 0, quantity: 0, remark: '' })

const packingTotal = computed(() =>
  packingEntries.value.reduce((sum, e) => sum + (e.subtotal || 0), 0)
)

async function loadPackingTypes() {
  try {
    const res = await packingTypeAPI.getList()
    packingTypes.value = Array.isArray(res) ? res : (res.items || [])
  } catch (e) { console.error(e) }
}

async function loadPackingEntries() {
  if (!quotationId.value) return
  try {
    const data = await packingEntryAPI.getList({ quotation_id: quotationId.value })
    packingEntries.value = (data || []).map(e => ({ ...e, _editing: false, _quantity: e.quantity }))
  } catch (e) { console.error(e) }
}

function onPackingTypeChange(id) {
  packingForm.packing_type_id = id
  const pt = packingTypes.value.find(p => p.id === id)
  packingForm.unit_price = pt ? (pt.unit_price || 0) : 0
}

function showAddPackingEntry() {
  packingForm.packing_type_id = null; packingForm.unit_price = 0; packingForm.quantity = 0; packingForm.remark = ''
  packingDialogVisible.value = true
}

async function addPackingConfirm() {
  if (!packingForm.packing_type_id) { ElMessage.warning('请选择运输包装类型'); return }
  try {
    await packingEntryAPI.upsert({ quotation_id: quotationId.value, packing_type_id: packingForm.packing_type_id, quantity: packingForm.quantity, remark: packingForm.remark })
    ElMessage.success('添加成功')
    packingDialogVisible.value = false
    loadPackingEntries()
  } catch (e) { ElMessage.error('添加失败') }
}

function editPackingRow(row) { row._editing = true; row._quantity = row.quantity; row._unit_price = row.unit_price }
function cancelPackingEdit(row) { row._editing = false }
async function savePackingRow(row) {
  try {
    if (row.id) {
      await packingEntryAPI.update(row.id, {
        packing_type_id: row.packing_type_id,
        quantity: Number(row._quantity || row.quantity || 0),
        unit_price: Number(row._unit_price || row.unit_price || 0),
        remark: row.remark || '',
      })
    } else {
      await packingEntryAPI.create(quotationId.value, {
        packing_type_id: row.packing_type_id,
        quantity: Number(row._quantity || row.quantity || 0),
        unit_price: Number(row._unit_price || row.unit_price || 0),
        remark: row.remark || '',
      })
    }
    row._editing = false
    ElMessage.success('保存成功')
    await loadPackingEntries()
  } catch (e) {
    ElMessage.error('保存失败: ' + (e?.response?.data?.detail || e?.message || '未知错误'))
  }
}
async function deletePackingEntry(id) {
  try { await packingEntryAPI.delete(id); ElMessage.success('删除成功'); loadPackingEntries() } catch (e) { ElMessage.error('删除失败') }
}

// ===== 差旅人天 =====
const travelDaysDialogVisible = ref(false)
const travelDaysForm = reactive({ travel_category_id: null, unit_price: 0, person_days: 0, remark: '' })

const travelDaysTotal = computed(() =>
  travelPersonDays.value.reduce((sum, e) => sum + (e.subtotal || 0), 0)
)

async function loadTravelCategories() {
  try {
    const res = await travelCategoryAPI.getList()
    travelCategories.value = Array.isArray(res) ? res : (res.items || [])
  } catch (e) { console.error(e) }
}

async function loadTravelDayRates() {
  // 单价由后端根据分类自动查，这里只加载分类
}

function onTravelCategoryChange(id) {
  travelDaysForm.category_id = id
  // 从已加载的人天单价列表中找对应分类的单价
  travelDaysForm.unit_price = 0
}

async function loadTravelPersonDays() {
  if (!quotationId.value) return
  try {
    const data = await travelPersonDaysAPI.getList({ quotation_id: quotationId.value })
    travelPersonDays.value = (data || []).map(e => ({ ...e, _editing: false, _person_days: e.person_days }))
  } catch (e) { console.error(e) }
}

function showAddTravelDaysEntry() {
  travelDaysForm.travel_category_id = null; travelDaysForm.unit_price = 0; travelDaysForm.person_days = 0; travelDaysForm.remark = ''
  travelDaysDialogVisible.value = true
}

async function addTravelDaysConfirm() {
  if (!travelDaysForm.travel_category_id) { ElMessage.warning('请选择差旅分类'); return }
  try {
    await travelPersonDaysAPI.upsert({ quotation_id: quotationId.value, travel_category_id: travelDaysForm.travel_category_id, person_days: travelDaysForm.person_days, remark: travelDaysForm.remark })
    ElMessage.success('添加成功')
    travelDaysDialogVisible.value = false
    loadTravelPersonDays()
  } catch (e) { ElMessage.error('添加失败') }
}

function editTravelDaysRow(row) { row._editing = true; row._person_days = row.person_days; row._unit_price = row.unit_price }
function cancelTravelDaysEdit(row) { row._editing = false }
async function saveTravelDaysRow(row) {
  try {
    if (row.id) {
      await travelPersonDaysAPI.update(row.id, {
        travel_category_id: row.travel_category_id,
        person_days: Number(row._person_days || row.person_days || 0),
        unit_price: Number(row._unit_price || row.unit_price || 0),
        remark: row.remark || '',
      })
    } else {
      await travelPersonDaysAPI.create(quotationId.value, {
        travel_category_id: row.travel_category_id,
        person_days: Number(row._person_days || row.person_days || 0),
        unit_price: Number(row._unit_price || row.unit_price || 0),
        remark: row.remark || '',
      })
    }
    row._editing = false
    ElMessage.success('保存成功')
    await loadTravelPersonDays()
  } catch (e) {
    ElMessage.error('保存失败: ' + (e?.response?.data?.detail || e?.message || '未知错误'))
  }
}
async function deleteTravelDaysEntry(id) {
  try { await travelPersonDaysAPI.delete(id); ElMessage.success('删除成功'); loadTravelPersonDays() } catch (e) { ElMessage.error('删除失败') }
}

// ===== 差旅人次 =====
const travelTripDialogVisible = ref(false)
const travelTripForm = reactive({ travel_category_id: null, travel_mode_id: null, unit_price: 0, visa_fee: 0, person_count: 0, remark: '' })

const travelTripsTotal = computed(() =>
  travelPersonTrips.value.reduce((sum, e) => sum + (e.subtotal || 0), 0)
)

async function loadTravelModes() {
  try {
    const res = await travelModeAPI.getList()
    const all = Array.isArray(res) ? res : (res.items || [])
    // 去掉"轮船" (DB 有但实际无对应单价配置)
    travelModes.value = all.filter(m => m.code !== 'ship')
  } catch (e) { console.error(e) }
}

async function loadTravelPersonTripFees() {
  try {
    const res = await travelPersonTripFeeAPI.getList()
    travelPersonTripFees.value = Array.isArray(res) ? res : (res.items || [])
  } catch (e) { console.error(e) }
}

// 本地查 (cat, mode) → fee 配置 (返回所有, 含已停用, 便于历史回填)
function findTripFee(categoryId, modeId) {
  if (!categoryId || !modeId) return null
  return travelPersonTripFees.value.find(f =>
    f.travel_category_id === categoryId && f.travel_mode_id === modeId
  ) || null
}

// 推荐默认出行方式: 优先 airplane > train > car > other (按 fee 表里的实际配置挑)
function getDefaultModeId(categoryId) {
  if (!categoryId) return null
  const priority = ['airplane', 'flight', 'train', 'car', 'other']
  for (const code of priority) {
    const mode = travelModes.value.find(m => m.code === code)
    if (!mode) continue
    if (findTripFee(categoryId, mode.id)) return mode.id
  }
  return travelModes.value[0]?.id || null
}

function onTripCategoryChange(id) {
  travelTripForm.travel_category_id = id
  // 选分类后: 自动推荐默认出行方式, 并按 (cat, mode) 填单价
  travelTripForm.travel_mode_id = getDefaultModeId(travelTripForm.travel_category_id)
  applyTripDefaultsFromFee()
}

function onTripModeChange(id) {
  travelTripForm.travel_mode_id = id
  applyTripDefaultsFromFee()
}

function applyTripDefaultsFromFee() {
  const fee = findTripFee(travelTripForm.travel_category_id, travelTripForm.travel_mode_id)
  travelTripForm.unit_price = fee ? Number(fee.unit_price || 0) : 0
  travelTripForm.visa_fee = fee ? Number(fee.visa_fee || 0) : 0
}

function computeTripSubtotal() {
  const count = travelTripForm.person_count || 0
  const unit = travelTripForm.unit_price || 0
  const visa = travelTripForm.visa_fee || 0
  const cat = travelCategories.value.find(c => c.id === travelTripForm.travel_category_id)
  const isDomestic = cat && cat.code === 'domestic'
  return count * (unit + (isDomestic ? 0 : visa))
}

Object.defineProperty(travelTripForm, 'subtotal', { get: computeTripSubtotal, enumerable: true })

async function loadTravelPersonTrips() {
  if (!quotationId.value) return
  try {
    const data = await travelPersonTripAPI.getList({ quotation_id: quotationId.value })
    travelPersonTrips.value = (data || []).map(e => ({ ...e, _editing: false, _person_count: e.person_count }))
  } catch (e) { console.error(e) }
}

function showAddTravelTripEntry() {
  Object.assign(travelTripForm, { travel_category_id: null, travel_mode_id: null, unit_price: 0, visa_fee: 0, person_count: 0, remark: '' })
  travelTripDialogVisible.value = true
  loadTravelCategories()
  loadTravelModes()
  loadTravelPersonTripFees()
}

async function addTravelTripConfirm() {
  if (!travelTripForm.travel_category_id || !travelTripForm.travel_mode_id) { ElMessage.warning('请选择差旅分类和出行方式'); return }
  try {
    await travelPersonTripAPI.upsert({
      quotation_id: quotationId.value,
      travel_category_id: travelTripForm.travel_category_id,
      travel_mode_id: travelTripForm.travel_mode_id,
      person_count: travelTripForm.person_count,
      remark: travelTripForm.remark
    })
    ElMessage.success('添加成功')
    travelTripDialogVisible.value = false
    loadTravelPersonTrips()
  } catch (e) { ElMessage.error('添加失败') }
}

function editTravelTripRow(row) { row._editing = true; row._person_count = row.person_count; row._unit_price = row.unit_price; row._visa_fee = row.visa_fee }
function cancelTravelTripEdit(row) { row._editing = false }
async function saveTravelTripRow(row) {
  try {
    if (row.id) {
      // 更新已有记录
      await travelPersonTripAPI.update(row.id, {
        travel_category_id: row.travel_category_id,
        travel_mode_id: row.travel_mode_id,
        person_count: Number(row._person_count || row.person_count || 0),
        unit_price: Number(row._unit_price || row.unit_price || 0),
        visa_fee: Number(row._visa_fee || row.visa_fee || 0),
        remark: row.remark || '',
      })
    } else {
      // 新增 (从弹窗确认后不会走到这里, 走 addTravelTripConfirm)
      await travelPersonTripAPI.create(quotationId.value, {
        travel_category_id: row.travel_category_id,
        travel_mode_id: row.travel_mode_id,
        person_count: Number(row._person_count || row.person_count || 0),
        unit_price: Number(row._unit_price || row.unit_price || 0),
        visa_fee: Number(row._visa_fee || row.visa_fee || 0),
        remark: row.remark || '',
      })
    }
    row._editing = false
    ElMessage.success('保存成功')
    await loadTravelPersonTrips()
  } catch (e) {
    ElMessage.error('保存失败: ' + (e?.response?.data?.detail || e?.message || '未知错误'))
  }
}
async function deleteTravelTripEntry(id) {
  try { await travelPersonTripAPI.delete(id); ElMessage.success('删除成功'); loadTravelPersonTrips() } catch (e) { ElMessage.error('删除失败') }
}

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
  laborForm.person_days = 0
  laborForm.unit_price = 0
  laborForm.labor_type = 'design'  // 默认设计
  laborDialogVisible.value = true
}

async function addLaborConfirm() {
  if (!laborForm.name) { ElMessage.warning('请填写名称'); return }
  // 验证名称必须在 7 个固定选项里
  const validChoice = LABOR_NAME_CHOICES.find(n => n.name === laborForm.name)
  if (!validChoice) {
    ElMessage.warning('请选择 7 个固定工时名称之一')
    return
  }
  // 同步 labor_type (防止用户绕过 onLaborNameChange)
  laborForm.labor_type = validChoice.labor_type
  if (laborForm.hours <= 0) { ElMessage.warning('工时必须大于0'); return }
  if (!laborForm.labor_type) { ElMessage.warning('请选择工时类型'); return }
  try {
    await api.post(`/quotations/${quotationId.value}/labor-hours`, {
      name: laborForm.name,
      hours: laborForm.hours,
      unit_price: laborForm.unit_price,
      labor_type: laborForm.labor_type,
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
  row._person_days = +(row.hours / HOURS_PER_DAY).toFixed(2)
  row._unit_price = row.unit_price
  row._labor_type = row.labor_type || 'design'
}

function cancelLaborEdit(row) {
  row._editing = false
}

async function saveLaborRow(row) {
  try {
    await api.put(`/quotations/${quotationId.value}/labor-hours/${row.id}`, {
      name: row._name,
      hours: row._hours,
      unit_price: row._unit_price,
      labor_type: row._labor_type,
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

// 加载父报价单信息
async function loadParentQuotation() {
  try {
    const parent = await quotationsAPI.getById(parentId.value)
    // 预填字段（除名称和方案编号外的继承字段）
    quotation.value.currency = parent.currency
    quotation.value.tax_rate = parent.tax_rate
    quotation.value.profit_rate = parent.profit_rate
    quotation.value.business_owner_id = parent.business_owner_id
    quotation.value.coefficients = parent.coefficients || { large: 1.0, standard: 1.0, other: 1.0 }
    quotation.value.type = 'single'  // 强制锁定单机

    // 生成子报价单方案编号：父方案编号-01, -02, ...
    const parentSchemeNo = parent.scheme_no || `Q${parent.id}`
    // 查询父报价单已有子报价单数量
    const siblings = await quotationsAPI.getChildren(parentId.value)
    const nextSeq = (siblings.length || 0) + 1
    quotation.value.scheme_no = `${parentSchemeNo}-${String(nextSeq).padStart(2, '0')}`
    quotation.value.parent_id = parentId.value
    console.log('子报价单方案编号:', quotation.value.scheme_no)
  } catch (error) {
    console.error('加载父报价单失败:', error)
    ElMessage.error('加载父报价单信息失败')
  }
}

// 加载报价单
async function loadQuotation() {
  console.log('loadQuotation called, id:', quotationId.value)
  if (!quotationId.value) {
    console.log('Skipping loadQuotation - no valid id')
    pageLoading.value = false
    return
  }
  try {
    const data = await api.get(`/quotations/${quotationId.value}`)
    quotation.value = data
    // 已归档的报价单不允许编辑，重定向回列表
    if (data.status === 'approved') {
      ElMessage.warning('已归档的报价单无法编辑，如需修改请先撤销归档')
      router.push('/quotations')
      return
    }
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
  } finally {
    pageLoading.value = false
  }
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
    // 一次拉所有业务用户（默认 page_size=20 太少），匹配方案库工号时需要全量
    const res = await api.get('/users', { params: { role: 'business', page_size: 200 } })
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
  savingBasic.value = true
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
    // 优先用后端返回的 detail 字段（FastAPI HTTPException）
    const msg = error?.response?.data?.detail || error.message || '未知错误'
    ElMessage.error('保存失败: ' + msg)
  } finally {
    savingBasic.value = false
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
    let data
    if (quotation.value.type === 'line' && isEdit.value) {
      // 线体报价单：聚合所有子报价单的模块
      data = await api.get(`/quotations/${quotationId.value}/all-modules`)
    } else {
      data = await api.get(`/quotations/${quotationId.value}/modules`)
    }
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
  moduleForm.module_type = 'other'  // 先默认值, inferModuleType 异步覆盖
  moduleDialogVisible.value = true
  // 打开弹窗自动静默推断 (无需用户点按钮)
  nextTick(() => {
    inferModuleType(true)  // silent=true, 不弹 ElMessage
  })
}

// 编辑模块
function editModule(module) {
  moduleDialogTitle.value = '编辑模块'
  moduleForm.id = module.id
  moduleForm.name = module.name || ''
  moduleForm.name_en = module.name_en || ''
  moduleForm.description = module.description || ''
  moduleForm.module_type = module.module_type || 'other'
  // 先关闭再打开, 强制 el-input 重新渲染 (避免 reactive 属性赋值后 input.value 不更新)
  moduleDialogVisible.value = false
  nextTick(() => {
    moduleDialogVisible.value = true
  })
}

// 自动推断模块类型 (根据当前登录用户对该报价单的参与类型 participant_type)
// 规则 (与后端 infer_module_type_from_participant_types 一致):
//   - agency → mechanical (机构)
//   - electrical → electrical (电气)
//   - project / 无参与记录 → other (其他)
// 自动模式: 弹窗打开时静默调用, 不弹 ElMessage (避免噪音)
// 手动模式: 用户点 ✨ 按钮时调用, 弹成功提示
async function inferModuleType(silent = false) {
  // 推断依据: 当前登录用户 (=模块创建人) 对该报价单的参与类型
  // 走后端 /api/modules/infer-type quotation_id 模式, 后端从 token 取 user_id 查 participant_type
  try {
    const res = await request.post('/modules/infer-type', { quotation_id: quotation.value?.id })
    const myType = res.participant_type
    if (!myType || res.user_count === 0) {
      // 静默时不弹提示 (避免每次开弹窗都弹"无参与类型"提示)
      if (!silent) {
        ElMessage.info(res.message || '当前用户在此报价单无参与类型记录, 默认为"其他"')
      }
      moduleForm.module_type = 'other'
      return
    }
    const map = {
      agency: 'mechanical',
      electrical: 'electrical',
      project: 'other',
    }
    moduleForm.module_type = map[myType] || 'other'
    if (!silent) {
      const label = MODULE_TYPES.find(t => t.value === moduleForm.module_type)?.label || '其他'
      ElMessage.success(`已根据您的参与类型 [${myType}] 推断为: ${label}`)
    }
  } catch (e) {
    console.error('推断失败', e)
    if (!silent) {
      ElMessage.error('推断失败: ' + (e.message || e))
    }
  }
}

// 保存模块
async function saveModule() {
  try {
    const payload = {
      name: moduleForm.name,
      name_en: moduleForm.name_en,
      description: moduleForm.description,
      module_type: moduleForm.module_type,
    }
    if (moduleForm.id) {
      await api.put(`/modules/${moduleForm.id}`, payload)
      ElMessage.success('更新成功')
    } else {
      await api.post(`/quotations/${quotationId.value}/modules`, payload)
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

// 加载物料列表（按筛选条件 + 分页查询）
async function loadAvailableMaterials() {
  try {
    const params = {
      page: materialPage.value,
      page_size: materialPageSize.value,
      status: 'active',
    }
    if (materialFilter.keyword) params.keyword = materialFilter.keyword
    if (materialFilter.category) params.category = materialFilter.category
    if (materialFilter.brand) params.brand = materialFilter.brand
    const data = await api.get('/materials', { params })
    availableMaterials.value = data.items || []
    materialTotal.value = data.total || 0
  } catch (error) {
    ElMessage.error('加载物料列表失败')
  }
}

// QuotationEditMaterials 子组件事件处理
async function handleLoadMaterials({ page, pageSize, keyword, category, brand }) {
  if (page) materialPage.value = page
  if (pageSize) materialPageSize.value = pageSize
  materialFilter.keyword = keyword || ''
  materialFilter.category = category || ''
  materialFilter.brand = brand || ''
  await loadAvailableMaterials()
}

async function handleAddMaterials(moduleId, materials) {
  if (!moduleId) return
  try {
    // 后端接口是单条添加 /modules/{id}/materials, 循环调
    for (const m of materials) {
      await api.post(`/modules/${moduleId}/materials`, {
        material_id: m.material_id,
        quantity: m.quantity || 1,
      })
    }
    ElMessage.success('已添加物料')
    await loadModuleMaterials()
    await summaryCompRef.value?.refresh?.()
  } catch (error) {
    ElMessage.error('添加物料失败: ' + (error?.response?.data?.detail || error?.message || '未知错误'))
  }
}

async function handleSaveOtherPrice(form) {
  try {
    // 后端 PUT /module_materials/{id} 接口接受 unit_price_override
    await api.put(`/module_materials/${form.id}`, {
      unit_price_override: form.unit_price_override,
    })
    ElMessage.success('已更新其他物料单价')
    otherPriceDialogVisible.value = false
    await loadModuleMaterials()
    await summaryCompRef.value?.refresh?.()
  } catch (error) {
    ElMessage.error('更新失败: ' + (error?.response?.data?.detail || error?.message || '未知错误'))
  }
}

// 分页改变
async function onMaterialPageChange(page) {
  materialPage.value = page
  await loadAvailableMaterials()
}

// 筛选条件变化 - 重置页码并重新查询 (keyword 单独防抖)
async function onMaterialFilterChange() {
  materialPage.value = 1
  await loadAvailableMaterials()
}

let _keywordDebounceTimer = null
async function onKeywordChange() {
  if (_keywordDebounceTimer) clearTimeout(_keywordDebounceTimer)
  _keywordDebounceTimer = setTimeout(async () => {
    materialPage.value = 1
    await loadAvailableMaterials()
  }, 400)
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
  // 重置筛选条件 + 分页
  materialFilter.keyword = ''
  materialFilter.category = ''
  materialFilter.brand = ''
  materialPage.value = 1
  materialPageSize.value = 50
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

// 修改其他物料单价
function editOtherMaterial(row) {
  otherPriceForm.id = row.id
  otherPriceForm.material_name = row.material_name
  otherPriceForm.unit_price_override = row.unit_price_override || row.unit_price || 0
  otherPriceDialogVisible.value = true
}

// 保存其他物料单价
async function saveOtherMaterialPrice() {
  if (!otherPriceForm.unit_price_override || otherPriceForm.unit_price_override <= 0) {
    ElMessage.warning('请输入有效的单价')
    return
  }
  try {
    await api.put(`/module_materials/${otherPriceForm.id}`, {
      unit_price_override: otherPriceForm.unit_price_override
    })
    ElMessage.success('修改成功')
    otherPriceDialogVisible.value = false
    await loadModuleMaterials()
  } catch (error) {
    ElMessage.error('修改失败')
  }
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
  if (isArchived.value) {
    ElMessage.error('已归档报价单不可编辑')
    return
  }
  
  try {
    // 检查是否重复物料
    const existingMaterialIds = moduleMaterials.value
      .filter(mm => mm.module_id === selectedModuleId.value)
      .map(mm => mm.material_id || mm.id)
    const duplicate = selectedMaterials.value.find(m => existingMaterialIds.includes(m.id))
    if (duplicate) {
      ElMessage.warning(`"${duplicate.name}" 已在该模块中，请修改数量`)
      return
    }

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
  if (isArchived.value) {
    ElMessage.error('已归档报价单不可编辑')
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
  if (isArchived.value) {
    ElMessage.error('已归档报价单不可编辑')
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
  openDownload(`/api/quotations/${quotationId.value}/versions/${version.version_no}/export/${fmt}?lang=${lang}`)
}

// 导出文件
function exportFile(format, lang = 'zh') {
  const langParam = (format === 'pdf' && lang) ? `&lang=${lang}` : ''
  openDownload(`/api/quotations/${quotationId.value}/export/${format}?currency=${selectedCurrency.value}${langParam}`)
}

// 导出汇总 tab 内容为 PDF（按网页显示样式截图）
async function exportSummaryAsPDF() {
  if (!summaryCompRef.value?.summaryRef) {
    ElMessage.error('汇总内容未加载，请先切换到汇总 tab')
    return
  }
  if (!summary.value) {
    ElMessage.warning('汇总数据为空，请先加载汇总')
    return
  }

  // 切换到汇总 tab 确保内容渲染
  if (activeTab.value !== 'summary') {
    activeTab.value = 'summary'
    await nextTick()
    await new Promise(resolve => setTimeout(resolve, 300))
  }

  const loading = ElMessage({
    message: '正在生成 PDF...',
    type: 'info',
    duration: 0
  })

  try {
    // 截图前临时隐藏不需要导出的元素（如货币切换器）
    const hideElements = summaryRef.value.querySelectorAll('.no-export')
    const prevDisplays = []
    hideElements.forEach((el) => {
      prevDisplays.push(el.style.display)
      el.style.display = 'none'
    })

    // 截图：使用完整 DOM 高度（包含滚动不可见部分）
    const canvas = await html2canvas(summaryRef.value, {
      scale: 2,
      useCORS: true,
      backgroundColor: '#ffffff',
      logging: false,
      windowWidth: summaryRef.value.scrollWidth,
      windowHeight: summaryRef.value.scrollHeight
    })

    // 恢复隐藏元素
    hideElements.forEach((el, i) => {
      el.style.display = prevDisplays[i]
    })

    // A4 尺寸（毫米），左右上下各留 5mm 边距
    const pdfWidth = 210
    const pdfHeight = 297
    const margin = 5
    const contentWidth = pdfWidth - margin * 2
    const contentHeight = pdfHeight - margin * 2

    // 高度按比例缩放到内容区宽度
    const imgWidth = contentWidth
    const imgHeight = (canvas.height * imgWidth) / canvas.width

    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    })

    // 如果内容总高度 <= A4 内容区，单页
    if (imgHeight <= contentHeight) {
      const imgData = canvas.toDataURL('image/png')
      pdf.addImage(imgData, 'PNG', margin, margin, imgWidth, imgHeight)
    } else {
      // 多页：按 A4 内容区高度切片
      const pageHeightInPx = (contentHeight * canvas.width) / imgWidth
      let position = 0
      let pageIndex = 0
      const totalPages = Math.ceil(canvas.height / pageHeightInPx)

      while (position < canvas.height) {
        const pageCanvas = document.createElement('canvas')
        pageCanvas.width = canvas.width
        const remainingHeight = canvas.height - position
        const currentPageHeight = Math.min(pageHeightInPx, remainingHeight)
        pageCanvas.height = currentPageHeight

        const ctx = pageCanvas.getContext('2d')
        ctx.fillStyle = '#ffffff'
        ctx.fillRect(0, 0, pageCanvas.width, pageCanvas.height)
        ctx.drawImage(
          canvas,
          0, position, canvas.width, currentPageHeight,
          0, 0, canvas.width, currentPageHeight
        )

        const pageImgData = pageCanvas.toDataURL('image/png')
        const pageImgHeight = (pageCanvas.height * imgWidth) / pageCanvas.width
        if (pageIndex > 0) pdf.addPage()
        pdf.addImage(pageImgData, 'PNG', margin, margin, imgWidth, pageImgHeight)

        position += currentPageHeight
        pageIndex += 1
      }
    }

    const fileName = `${quotation.value?.name || '报价单'}_汇总_${new Date().toISOString().slice(0, 10)}.pdf`
    pdf.save(fileName)
    ElMessage.success(`PDF 已生成：${fileName}`)
  } catch (err) {
    console.error('导出汇总 PDF 失败：', err)
    ElMessage.error('导出失败：' + (err.message || '未知错误'))
  } finally {
    loading.close()
  }
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
  } else if (tab === 'packing') {
    loadPackingTypes()
    loadPackingEntries()
  } else if (tab === 'travel-days') {
    loadTravelCategories()
    loadTravelPersonDays()
  } else if (tab === 'travel-trips') {
    loadTravelCategories()
    loadTravelModes()
    loadTravelPersonTripFees()
    loadTravelPersonTrips()
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
    // 如果是创建子报价单，预填父报价单信息
    if (parentId.value) {
      await loadParentQuotation()
    }
    pageLoading.value = false
  }
})
</script>

<style scoped>
.quotation-edit {
  padding: var(--spacing-lg);
}

/* 方案号下拉建议 */
.scheme-suggestion {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}
.scheme-suggestion .scheme-no {
  font-weight: 600;
  color: #409eff;
  min-width: 80px;
}
.scheme-suggestion .scheme-name {
  color: #606266;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.scheme-suggestion.is-used {
  background: #fef0f0;
}
.scheme-suggestion.is-used .scheme-no {
  color: #f56c6c;
}
.scheme-hint {
  display: inline-block;
  margin-left: 8px;
  font-size: 12px;
}
.scheme-hint.info { color: #909399; }
.scheme-hint.success { color: #67c23a; }
.scheme-hint.warning { color: #e6a23c; }
.scheme-hint.danger { color: #f56c6c; font-weight: 600; }

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
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: calc(100vh - 140px);
}

.edit-card :deep(.el-tabs) {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.edit-card :deep(.el-tabs__content) {
  flex: 1;
  overflow: auto;
}

.edit-card :deep(.el-tab-pane) {
  height: 100%;
  overflow: auto;
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

/* 汇总布局 */
.summary-layout {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.summary-left {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-md);
  align-items: stretch;
}

.summary-right {
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.summary-card {
  background: var(--color-bg-hover);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  text-align: center;
}

.summary-card.compact {
  padding: var(--spacing-md);
  min-height: 90px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.summary-card.total {
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

.summary-card.total .summary-label {
  color: rgba(255,255,255,0.75);
}

.summary-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.summary-value.highlight {
  color: var(--color-primary);
}

.summary-card.total .summary-value {
  color: white;
}

.summary-value.large {
  font-size: 32px;
  color: #FFFFFF;
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

/* 占比卡片组（5个：硬件/人力/差旅/利润/税） */
.ratio-cards {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.ratio-card {
  background: var(--color-bg-hover);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  text-align: left;
  border-left: 4px solid var(--color-primary);
}

.ratio-card .ratio-label {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-bottom: 6px;
}

.ratio-card .ratio-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1.2;
}

.ratio-card .ratio-percent {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-primary);
  margin-top: 4px;
}

.ratio-bar {
  margin-top: 8px;
  height: 6px;
  background: rgba(0,0,0,0.06);
  border-radius: 3px;
  overflow: hidden;
}

.ratio-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.4s ease;
}

.ratio-bar-fill.material { background: linear-gradient(90deg, #0D9488, #14B8A6); }
.ratio-bar-fill.labor { background: linear-gradient(90deg, #6366F1, #818CF8); }
.ratio-bar-fill.travel { background: linear-gradient(90deg, #F59E0B, #FBBF24); }
.ratio-bar-fill.profit { background: linear-gradient(90deg, #10B981, #34D399); }
.ratio-bar-fill.tax { background: linear-gradient(90deg, #EF4444, #F87171); }

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

/* 堆叠条 */
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

/* 费用卡片 */
.fees-card {
  background: var(--color-bg-hover);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  text-align: left;
  flex: 1;
}

.fees-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid rgba(0,0,0,0.08);
}

.fees-total {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-primary);
}

.fees-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.fees-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  padding: 3px 0;
  color: var(--color-text-secondary);
}

.fees-row span:last-child {
  font-weight: 500;
  color: var(--color-text-primary);
}

.profit-pct {
  font-size: 12px;
  margin-left: 4px;
  color: var(--color-primary);
}

@media (max-width: 900px) {
  .summary-layout {
    flex-direction: column;
  }
  .summary-left {
    grid-template-columns: repeat(3, 1fr);
  }
  .summary-right {
    width: 100%;
  }
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
  align-items: center;
}

.material-pagination {
  display: flex;
  justify-content: flex-end;
  margin-top: var(--spacing-md);
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

.module-quotation-tag {
  padding: 2px 8px;
  background: #E0E7FF;
  color: #4F46E5;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
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

/* 模块类型分组卡片 (按机构/电气/其他 分类) */
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

.module-type-stat {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 13px;
  color: var(--color-text-secondary);
}

.module-type-total {
  font-weight: 700;
  font-size: 16px;
  color: var(--color-primary);
}

.module-type-body {
  padding: 0;
}

.module-type-empty {
  padding: 32px;
  text-align: center;
  color: var(--color-text-secondary);
  font-size: 13px;
  font-style: italic;
}

.module-type-body .module-group {
  margin-bottom: 0;
  border: none;
  border-radius: 0;
  border-bottom: 1px solid var(--color-border-light);
}
.module-type-body .module-group:last-child {
  border-bottom: none;
}

/* 汇总模块卡片横向 grid 排列 - 强制 1 行 3 列 (自适应: <3 类时每列等宽) */
.summary-modules-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
  margin-top: 12px;
}

/* viewport < 760px 时降为 1 列 */
@media (max-width: 760px) {
  .summary-modules-grid {
    grid-template-columns: 1fr;
  }
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
.labor-total-days {
  margin-left: 8px;
  color: #15803d;
  font-weight: 500;
}
.form-hint {
  margin-left: 12px;
  color: #94a3b8;
  font-size: 12px;
}

.packing-header {
  display: flex;
  gap: 8px;
}

.money {
  font-weight: 600;
  color: var(--color-primary);
}

/* 汇总费用系数明细 - 2 卡片布局 (与 QuotationView 同步) */
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

/* ====== 目标调价 (5 张卡片) ====== */
.target-price-cards {
  display: grid;
  /* 5 个 1fr + 1 个跨 2 列 (分类建议表) → 实际占 7 个 grid 列 */
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
</style>
