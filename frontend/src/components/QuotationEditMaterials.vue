<template>
  <!-- 已归档警告 -->
  <el-alert
    v-if="isArchived"
    title="报价单已归档，物料变更需要提交审核"
    type="warning"
    :closable="false"
    show-icon
    style="margin-bottom: 16px;"
  >
    <template #default>
      您的物料变更申请将发送给报价单负责人审核，审核通过后才会生效。
      <el-button
        v-if="pendingReviewCount > 0"
        type="warning"
        size="small"
        style="margin-left: 16px;"
        @click="$emit('go-to-pending-reviews')"
      >
        查看待审核 ({{ pendingReviewCount }})
      </el-button>
    </template>
  </el-alert>

  <div class="material-actions">
    <el-select
      v-model="selectedModuleFilter"
      placeholder="全部模块"
      clearable
      style="width: 200px;"
      @change="onModuleFilterChange"
    >
      <el-option
        v-for="mod in modules"
        :key="mod.id"
        :label="mod.name"
        :value="mod.id"
      />
    </el-select>
  </div>

  <!-- 按模块类型分组卡片展示 -->
  <div v-for="group in groupedMaterials" :key="group.value" class="module-type-group">
    <div class="module-type-header" :class="'type-' + group.value">
      <div class="module-type-icon" :class="'type-' + group.value">
        <span v-if="group.value === 'mechanical'">🔧</span>
        <span v-else-if="group.value === 'electrical'">⚡</span>
        <span v-else>📦</span>
      </div>
      <span class="module-type-title">{{ group.label }}模块</span>
      <span class="module-type-count">{{ group.group_module_count }} 个模块</span>
      <div class="module-type-stat">
        <span>{{ group.group_materials_count }} 项物料</span>
        <span class="module-type-total">¥{{ group.group_total.toFixed(2) }}</span>
      </div>
    </div>
    <div class="module-type-body">
      <div v-if="group.module_list.length === 0" class="module-type-empty">
        该类型暂无模块
      </div>
      <div v-for="mod in group.module_list" :key="mod.id" class="module-group">
        <div class="module-group-header">
          <span class="module-name">{{ mod.name }}</span>
          <el-tag
            size="small"
            :type="mod.module_type === 'mechanical' ? 'primary' : mod.module_type === 'electrical' ? 'warning' : 'info'"
            effect="plain"
          >
            {{ mod.module_type_label || '其他' }}
          </el-tag>
          <span class="module-material-count">{{ mod.materials.length }} 项物料</span>
          <span class="module-total">小计: {{ mod.total.toFixed(2) }} 元</span>
          <el-button type="primary" size="small" @click="openAddMaterialDialog(mod.id)">+ 添加物料</el-button>
        </div>
        <el-table :data="mod.materials" border style="width: 100%;" show-overflow-tooltip>
          <el-table-column prop="material_name" label="物料名称" min-width="100">
            <template #default="{ row }">{{ row.material_name || '-' }}</template>
          </el-table-column>
          <el-table-column prop="item_no" label="品号" min-width="110">
            <template #default="{ row }">
              <span v-if="row.item_no" style="font-family: monospace;">{{ row.item_no }}</span>
              <span v-else style="color: #c0c4cc;">-</span>
            </template>
          </el-table-column>
          <el-table-column prop="specification" label="规格" min-width="80">
            <template #default="{ row }">{{ row.specification || '-' }}</template>
          </el-table-column>
          <el-table-column prop="brand" label="品牌" width="70">
            <template #default="{ row }">{{ row.brand || '-' }}</template>
          </el-table-column>
          <el-table-column v-if="hasKeyFields" prop="param1" label="关键参数01" width="130">
            <template #default="{ row }"><span v-if="row.param1">{{ row.param1 }}</span></template>
          </el-table-column>
          <el-table-column v-if="hasKeyFields" prop="param2" label="关键参数02" width="130">
            <template #default="{ row }"><span v-if="row.param2">{{ row.param2 }}</span></template>
          </el-table-column>
          <el-table-column v-if="hasKeyFields" prop="param3" label="关键参数03" width="130">
            <template #default="{ row }"><span v-if="row.param3">{{ row.param3 }}</span></template>
          </el-table-column>
          <el-table-column prop="unit" label="单位" width="60">
            <template #default="{ row }">{{ row.unit || '-' }}</template>
          </el-table-column>
          <el-table-column prop="unit_price" label="单价" width="90">
            <template #default="{ row }">{{ (row.unit_price || 0).toFixed(2) }}</template>
          </el-table-column>
          <el-table-column label="数量" width="130">
            <template #default="{ row }">
              <span v-if="row.is_other === true">{{ row.quantity }} {{ row.unit }} <span style="color:#999;font-size:12px">(不可改)</span></span>
              <el-input-number
                v-else
                :model-value="row.quantity"
                :min="1"
                size="small"
                controls-position="right"
                @change="(val) => $emit('update-quantity', row.id, val)"
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
              {{ row.selected_by_name || '-' }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" align="center">
            <template #default="{ row }">
              <template v-if="row.is_other === true">
                <el-button size="small" @click="editOtherMaterial(row)">改单价</el-button>
                <el-button size="small" type="danger" @click="$emit('delete-material', row.id)">删除</el-button>
              </template>
              <el-button v-else size="small" type="danger" @click="$emit('delete-material', row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>

  <!-- 全部模块合计 -->
  <div v-if="moduleMaterials.length > 0" class="material-summary total">
    <span>全部物料合计：{{ allMaterialsTotal.toFixed(2) }} 元</span>
  </div>

  <!-- 添加物料弹窗 -->
  <el-dialog v-model="materialDialogVisible" title="添加物料" width="1300px">
    <div class="material-filter-bar">
      <el-input
        v-model="localFilter.keyword"
        placeholder="搜索品名/规格/品牌"
        clearable
        style="width: 200px;"
        @input="onKeywordInput"
        @clear="emitFilterChange"
      />
      <el-select
        v-model="localFilter.category"
        placeholder="分类"
        clearable
        style="width: 110px;"
        @change="emitFilterChange"
      >
        <el-option label="大件" value="large" />
        <el-option label="核心部件" value="standard" />
        <el-option label="其他件" value="other" />
      </el-select>
      <el-select
        v-model="localFilter.brand"
        placeholder="品牌"
        clearable
        style="width: 110px;"
        @change="emitFilterChange"
      >
        <el-option v-for="b in availableBrands" :key="b" :label="b" :value="b" />
      </el-select>
      <span style="margin-left:auto;color:#909399;font-size:13px;">共 {{ materialTotal }} 条</span>
    </div>
    <el-table
      ref="materialTableRef"
      :data="availableMaterials"
      border
      style="width: 100%; margin-top: 12px;"
      max-height="450"
      show-overflow-tooltip
      @selection-change="handleMaterialSelection"
    >
      <el-table-column type="selection" width="45" />
      <el-table-column prop="name" label="品名" min-width="120" />
      <el-table-column prop="item_no" label="品号" min-width="110">
        <template #default="{ row }">
          <span v-if="row.item_no" style="font-family: monospace;">{{ row.item_no }}</span>
          <span v-else style="color: #c0c4cc;">-</span>
        </template>
      </el-table-column>
      <el-table-column prop="spec" label="规格" min-width="100" />
      <el-table-column prop="brand" label="品牌" width="70" />
      <el-table-column v-if="materialHasKeyParams" prop="param1" label="关键参数01" width="140">
        <template #default="{ row }"><span v-if="row.param1" class="key-param">{{ row.param1 }}</span></template>
      </el-table-column>
      <el-table-column v-if="materialHasKeyParams" prop="param2" label="关键参数02" width="140">
        <template #default="{ row }"><span v-if="row.param2" class="key-param">{{ row.param2 }}</span></template>
      </el-table-column>
      <el-table-column v-if="materialHasKeyParams" prop="param3" label="关键参数03" width="140">
        <template #default="{ row }"><span v-if="row.param3" class="key-param">{{ row.param3 }}</span></template>
      </el-table-column>
      <el-table-column prop="unit" label="单位" width="60" />
      <el-table-column prop="unit_price" label="单价" width="70" />
      <el-table-column label="分类" width="70">
        <template #default="{ row }">{{ getCategoryLabel(row.category) }}</template>
      </el-table-column>
      <el-table-column label="数量" width="120">
        <template #default="{ row }">
          <span v-if="row.name === '其他'">1 <span style="color:#999;font-size:12px">(不可改)</span></span>
          <el-input-number
            v-else
            v-model="row._quantity"
            :min="1"
            size="small"
            controls-position="right"
            :disabled="!selectedMaterials.includes(row)"
          />
        </template>
      </el-table-column>
    </el-table>
    <div class="material-pagination">
      <el-pagination
        v-model:current-page="localPage"
        v-model:page-size="localPageSize"
        :total="materialTotal"
        :page-sizes="[20, 50, 100, 200]"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="emitPageChange"
        @size-change="emitPageChange"
      />
    </div>
    <template #footer>
      <el-button @click="closeAddMaterialDialog">取消</el-button>
      <el-button type="primary" @click="confirmAddMaterials">确定添加</el-button>
    </template>
  </el-dialog>

  <!-- 修改其他物料单价弹窗 -->
  <el-dialog v-model="otherPriceDialogVisible" title="修改其他物料单价" width="400px">
    <el-form :model="otherPriceForm" label-width="100px">
      <el-form-item label="物料名称">
        <el-input v-model="otherPriceForm.material_name" disabled />
      </el-form-item>
      <el-form-item label="单价">
        <el-input-number v-model="otherPriceForm.unit_price_override" :min="0" :precision="2" style="width: 100%;" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="otherPriceDialogVisible = false">取消</el-button>
      <el-button type="primary" @click="confirmSaveOtherPrice">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'

const props = defineProps({
  isEdit: Boolean,
  moduleMaterials: { type: Array, default: () => [] },
  groupedMaterials: { type: Array, default: () => [] },
  allMaterialsTotal: { type: Number, default: 0 },
  selectedCurrency: { type: String, default: '' },
  exchangeRates: { type: Object, default: () => ({}) },
  moduleTypes: { type: Array, default: () => [] },
  dispatchGroupInfo: { type: Object, default: () => ({}) },
  isArchived: Boolean,
  modules: { type: Array, default: () => [] },
  pendingReviewCount: { type: Number, default: 0 },
  availableMaterials: { type: Array, default: () => [] },
  materialTotal: { type: Number, default: 0 },
  hasKeyFields: { type: Boolean, default: false },
  materialHasKeyParams: { type: Boolean, default: false },
  selectedModuleFilter: { type: [Number, String], default: null },
})

const emit = defineEmits([
  'update:selectedModuleFilter',
  'update-quantity',
  'delete-material',
  'add-materials',
  'save-other-price',
  'load-materials',
  'go-to-pending-reviews',
])

// ---------------------------------------------------------------------------
// Module filter (v-model pattern)
// ---------------------------------------------------------------------------
const selectedModuleFilter = ref(props.selectedModuleFilter)

watch(() => props.selectedModuleFilter, (val) => {
  selectedModuleFilter.value = val
})

function onModuleFilterChange(val) {
  emit('update:selectedModuleFilter', val)
}

// ---------------------------------------------------------------------------
// Add material dialog
// ---------------------------------------------------------------------------
const materialDialogVisible = ref(false)
const materialDialogModuleId = ref(null)
const selectedMaterials = ref([])
const materialTableRef = ref(null)
const localFilter = reactive({
  keyword: '',
  category: '',
  brand: '',
})
const localPage = ref(1)
const localPageSize = ref(50)

function onKeywordInput() {
  if (window._keywordDebounceTimer) clearTimeout(window._keywordDebounceTimer)
  window._keywordDebounceTimer = setTimeout(() => {
    emitFilterChange()
  }, 400)
}

function emitFilterChange() {
  localPage.value = 1
  emitLoadMaterials()
}

function emitPageChange() {
  emitLoadMaterials()
}

function emitLoadMaterials() {
  emit('load-materials', {
    page: localPage.value,
    pageSize: localPageSize.value,
    keyword: localFilter.keyword,
    category: localFilter.category,
    brand: localFilter.brand,
  })
}

function openAddMaterialDialog(moduleId) {
  materialDialogModuleId.value = moduleId
  localFilter.keyword = ''
  localFilter.category = ''
  localFilter.brand = ''
  localPage.value = 1
  localPageSize.value = 50
  selectedMaterials.value = []
  materialDialogVisible.value = true
  emitLoadMaterials()
}

function closeAddMaterialDialog() {
  materialDialogVisible.value = false
  selectedMaterials.value.forEach(m => { m._quantity = 1 })
  selectedMaterials.value = []
}

function handleMaterialSelection(selection) {
  selectedMaterials.value = selection
}

function confirmAddMaterials() {
  if (selectedMaterials.value.length === 0) {
    return
  }
  const materials = selectedMaterials.value.map(m => ({
    material_id: m.id,
    quantity: m._quantity || 1,
  }))
  emit('add-materials', materialDialogModuleId.value, materials)
  materialDialogVisible.value = false
  selectedMaterials.value.forEach(m => { m._quantity = 1 })
  selectedMaterials.value = []
}

// ---------------------------------------------------------------------------
// Other material price dialog
// ---------------------------------------------------------------------------
const otherPriceDialogVisible = ref(false)
const otherPriceForm = reactive({
  id: null,
  material_name: '其他',
  unit_price_override: 0,
})

function editOtherMaterial(row) {
  otherPriceForm.id = row.id
  otherPriceForm.material_name = row.material_name
  otherPriceForm.unit_price_override = row.unit_price_override || row.unit_price || 0
  otherPriceDialogVisible.value = true
}

function confirmSaveOtherPrice() {
  if (!otherPriceForm.unit_price_override || otherPriceForm.unit_price_override <= 0) {
    return
  }
  emit('save-other-price', { ...otherPriceForm })
  otherPriceDialogVisible.value = false
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
const availableBrands = computed(() => {
  const brands = new Set()
  props.availableMaterials.forEach(m => {
    if (m.brand) brands.add(m.brand)
  })
  return Array.from(brands).sort()
})

function getCategoryLabel(cat) {
  const map = { large: '大件', standard: '核心部件', other: '其他件' }
  return map[cat] || cat || '-'
}
</script>
