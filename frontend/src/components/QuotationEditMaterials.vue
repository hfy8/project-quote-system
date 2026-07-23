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
    <el-button
      type="success"
      :icon="Download"
      :disabled="noItemNoMaterialsCount === 0"
      style="margin-left: 12px;"
      @click="exportNoItemNoMaterials"
    >
      导出无品号物料 ({{ noItemNoMaterialsCount }})
    </el-button>
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
        <el-table :data="getSortedMaterials(mod)" border style="width: 100%;" show-overflow-tooltip
          @sort-change="(sort) => onSortChange(mod.id, sort)">
          <el-table-column prop="material_name" label="物料名称" min-width="100" sortable="custom">
            <template #default="{ row }">
              <span>{{ row.material_name || '-' }}</span>
              <!-- migration 020: 自制件徽章 -->
              <span v-if="row.is_custom" class="custom-tag" title="自制件 (不参与导出无品号物料)">自制件</span>
            </template>
          </el-table-column>
          <el-table-column prop="item_no" label="品号" min-width="110" sortable="custom">
            <template #default="{ row }">
              <span v-if="row.item_no" style="font-family: monospace;">{{ row.item_no }}</span>
              <span v-else style="color: #c0c4cc;">-</span>
            </template>
          </el-table-column>
          <el-table-column prop="specification" label="规格" min-width="80" sortable="custom">
            <template #default="{ row }">{{ row.specification || '-' }}</template>
          </el-table-column>
          <el-table-column prop="brand" label="品牌" width="70">
            <template #default="{ row }">{{ row.brand || '-' }}</template>
          </el-table-column>
          <el-table-column prop="material_type" label="类型" width="80">
            <template #default="{ row }">
              <span :class="['material-type-tag', row.material_type || 'other']">
                {{ getMaterialTypeLabel(row.material_type) }}
              </span>
            </template>
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
          <el-table-column prop="unit_price" label="单价" width="90" sortable="custom">
            <template #default="{ row }">{{ (row.unit_price || 0).toFixed(2) }}</template>
          </el-table-column>
          <el-table-column prop="quantity" label="数量" width="130" sortable="custom">
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
          <el-table-column prop="subtotal" label="小计" width="100" sortable="custom">
            <template #default="{ row }">
              {{ ((row.unit_price || 0) * row.quantity).toFixed(2) }}
            </template>
          </el-table-column>
          <el-table-column label="添加人" width="80">
            <template #default="{ row }">
              {{ row.selected_by_name || '-' }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="220" align="center">
            <template #default="{ row }">
              <template v-if="row.is_custom === true">
                <!-- migration 020: 自制件编辑 -->
                <el-button size="small" @click="openCustomEditDialog(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="$emit('delete-material', row.id)">删除</el-button>
              </template>
              <template v-else-if="row.is_other === true">
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
    <!-- 顶部 tab 切换: 选择原材料 / 添加自制件 — migration 020 -->
    <el-tabs v-model="addDialogTab" class="add-dialog-tabs">
      <el-tab-pane label="选择原材料" name="raw">
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
          <el-table-column label="类型" width="80">
            <template #default="{ row }">
              <span class="material-type-tag" :class="row.material_type || 'other'">
                {{ getMaterialTypeLabel(row.material_type) }}
              </span>
            </template>
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
      </el-tab-pane>

      <!-- 自制件 tab — migration 020 -->
      <el-tab-pane label="添加自制件" name="custom">
        <div class="custom-form-tip">
          <el-alert type="info" :closable="false" show-icon>
            <template #title>
              自制件：物料库没有的物料, 由报价员手动填写完整信息 (品名/规格/单位/单价/类型等)
              <br />添加后仅本次报价单使用, 不进入物料库, 不参与"导出无品号物料"
            </template>
          </el-alert>
        </div>
        <el-form :model="customForm" :rules="customFormRules" ref="customFormRef" label-width="100px" class="custom-form">
          <el-form-item label="品名" prop="name">
            <el-input v-model="customForm.name" placeholder="例: 外购电机支架" maxlength="100" show-word-limit />
          </el-form-item>
          <el-form-item label="规格" prop="spec">
            <el-input v-model="customForm.spec" placeholder="例: 50×30×2mm" maxlength="200" />
          </el-form-item>
          <el-form-item label="单位" prop="unit">
            <el-input v-model="customForm.unit" placeholder="个/件/套" maxlength="20" style="width: 120px;" />
          </el-form-item>
          <el-form-item label="单价" prop="unit_price">
            <el-input-number v-model="customForm.unit_price" :min="0" :precision="2" :step="10" style="width: 180px;" />
          </el-form-item>
          <el-form-item label="数量" prop="quantity">
            <el-input-number v-model="customForm.quantity" :min="1" :step="1" style="width: 180px;" />
          </el-form-item>
          <el-form-item label="类型" prop="material_type">
            <el-select v-model="customForm.material_type" placeholder="请选择" style="width: 180px;">
              <el-option label="机械类" value="mechanical" />
              <el-option label="非机械类" value="electrical" />
              <el-option label="其他" value="other" />
            </el-select>
          </el-form-item>
          <el-form-item label="部件分类" prop="category">
            <el-select v-model="customForm.category" placeholder="请选择" style="width: 180px;">
              <el-option label="大件" value="large" />
              <el-option label="核心部件" value="standard" />
              <el-option label="其他件" value="other" />
            </el-select>
          </el-form-item>
          <el-form-item label="产品名称">
            <el-input v-model="customForm.product_name" placeholder="产品线 (可空)" maxlength="100" />
          </el-form-item>
          <el-form-item label="品牌">
            <el-input v-model="customForm.brand" placeholder="可空" maxlength="50" style="width: 200px;" />
          </el-form-item>
          <el-form-item label="关键参数1">
            <el-input v-model="customForm.param1" placeholder="可空" maxlength="100" />
          </el-form-item>
          <el-form-item label="关键参数2">
            <el-input v-model="customForm.param2" placeholder="可空" maxlength="100" />
          </el-form-item>
          <el-form-item label="关键参数3">
            <el-input v-model="customForm.param3" placeholder="可空" maxlength="100" />
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
    <template #footer>
      <el-button @click="closeAddMaterialDialog">取消</el-button>
      <!-- 不同 tab 不同按钮 -->
      <el-button v-if="addDialogTab === 'raw'" type="primary" @click="confirmAddMaterials">确定添加 ({{ selectedMaterials.length }})</el-button>
      <el-button v-else type="primary" @click="confirmAddCustomMaterial">确定添加自制件</el-button>
    </template>
  </el-dialog>

  <!-- 自制件编辑弹窗 — migration 020 -->
  <el-dialog v-model="customEditDialogVisible" title="编辑自制件" width="600px">
    <el-form :model="customEditForm" label-width="100px">
      <el-form-item label="品名">
        <el-input v-model="customEditForm.name" maxlength="100" />
      </el-form-item>
      <el-form-item label="规格">
        <el-input v-model="customEditForm.spec" maxlength="200" />
      </el-form-item>
      <el-form-item label="单位">
        <el-input v-model="customEditForm.unit" maxlength="20" style="width: 120px;" />
      </el-form-item>
      <el-form-item label="单价">
        <el-input-number v-model="customEditForm.unit_price" :min="0" :precision="2" :step="10" style="width: 180px;" />
      </el-form-item>
      <el-form-item label="类型">
        <el-select v-model="customEditForm.material_type" style="width: 180px;">
          <el-option label="机械类" value="mechanical" />
          <el-option label="非机械类" value="electrical" />
          <el-option label="其他" value="other" />
        </el-select>
      </el-form-item>
      <el-form-item label="部件分类">
        <el-select v-model="customEditForm.category" style="width: 180px;">
          <el-option label="大件" value="large" />
          <el-option label="核心部件" value="standard" />
          <el-option label="其他件" value="other" />
        </el-select>
      </el-form-item>
      <el-form-item label="产品名称">
        <el-input v-model="customEditForm.product_name" maxlength="100" />
      </el-form-item>
      <el-form-item label="品牌">
        <el-input v-model="customEditForm.brand" maxlength="50" style="width: 200px;" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="customEditDialogVisible = false">取消</el-button>
      <el-button type="primary" @click="confirmSaveCustomEdit">保存</el-button>
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
import { Download } from '@element-plus/icons-vue'
import * as XLSX from 'xlsx-js-style'
import JSZip from 'jszip'
import { ElMessage } from 'element-plus'

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
  'add-custom-material',  // migration 020
  'update-custom-material',  // migration 020
])

// ---------------------------------------------------------------------------
// 自制件 — migration 020
// ---------------------------------------------------------------------------
const addDialogTab = ref('raw')
const customFormRef = ref(null)
const customForm = reactive({
  name: '',
  spec: '',
  unit: '',
  unit_price: 0,
  quantity: 1,
  material_type: 'other',
  category: 'standard',
  product_name: '',
  brand: 'RS',
  param1: '',
  param2: '',
  param3: '',
})
const customFormRules = {
  name: [{ required: true, message: '请输入品名', trigger: 'blur' }],
  unit: [{ required: true, message: '请输入单位', trigger: 'blur' }],
  unit_price: [{ required: true, message: '请输入单价', trigger: 'blur' }],
  quantity: [{ required: true, message: '请输入数量', trigger: 'blur' }],
  material_type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  category: [{ required: true, message: '请选择部件分类', trigger: 'change' }],
}

// 自制件编辑
const customEditDialogVisible = ref(false)
const customEditForm = reactive({
  mmId: null,
  name: '',
  spec: '',
  unit: '',
  unit_price: 0,
  material_type: 'other',
  category: 'standard',
  product_name: '',
  brand: '',
})
const customEditTarget = ref(null)  // 当前编辑的 mm 对象

function openCustomEditDialog(mm) {
  customEditTarget.value = mm
  customEditForm.mmId = mm.id
  customEditForm.name = mm.material_name || ''
  customEditForm.spec = mm.specification || ''
  customEditForm.unit = mm.unit || ''
  customEditForm.unit_price = mm.unit_price || 0
  customEditForm.material_type = mm.material_type || 'other'
  customEditForm.category = mm.category || 'standard'
  customEditForm.product_name = mm.product_name || ''
  customEditForm.brand = mm.brand || ''
  customEditDialogVisible.value = true
}

function confirmSaveCustomEdit() {
  if (!customEditForm.name || !customEditForm.unit) {
    ElMessage.warning('品名和单位必填')
    return
  }
  emit('update-custom-material', {
    mmId: customEditForm.mmId,
    custom_data: {
      name: customEditForm.name,
      spec: customEditForm.spec,
      unit: customEditForm.unit,
      brand: customEditForm.brand,
      unit_price: customEditForm.unit_price,
      // 保留原 param1/2/3 (不在编辑弹窗里改)
      param1: customEditTarget.value?.param1 || '',
      param2: customEditTarget.value?.param2 || '',
      param3: customEditTarget.value?.param3 || '',
    },
    material_type: customEditForm.material_type,
    category: customEditForm.category,
    product_name: customEditForm.product_name,
  })
  customEditDialogVisible.value = false
}

function confirmAddCustomMaterial() {
  customFormRef.value?.validate((valid) => {
    if (!valid) return
    emit('add-custom-material', {
      is_custom: true,
      quantity: customForm.quantity,
      custom_data: {
        name: customForm.name,
        spec: customForm.spec,
        unit: customForm.unit,
        brand: customForm.brand,
        unit_price: customForm.unit_price,
        param1: customForm.param1,
        param2: customForm.param2,
        param3: customForm.param3,
      },
      material_type: customForm.material_type,
      category: customForm.category,
      product_name: customForm.product_name,
    })
    // 重置表单
    customForm.name = ''
    customForm.spec = ''
    customForm.unit = ''
    customForm.unit_price = 0
    customForm.quantity = 1
    customForm.material_type = 'other'
    customForm.category = 'standard'
    customForm.product_name = ''
    customForm.brand = 'RS'
    customForm.param1 = ''
    customForm.param2 = ''
    customForm.param3 = ''
    addDialogTab.value = 'raw'  // 切回 raw tab
    closeAddMaterialDialog()
  })
}

// 打开添加物料 dialog — migration 020 加了 tab 重置
function openAddMaterialDialog(moduleId) {
  addDialogTab.value = 'raw'  // 默认回到原材料 tab
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
// 物料表格排序 (per-module 状态, 默认按物料名+规格升序)
// ---------------------------------------------------------------------------
// 每模块独立维护: { moduleId: { prop, order } }
// 默认无前端排序, 用后端默认 ORDER BY (物料名 + 规格 + id)
const moduleSortState = ref({})

function onSortChange(modId, sort) {
  // sort = { prop, order } 其中 order 为 ascending/descending
  if (!sort.order) {
    // element-ui 循环 asc → desc → asc, 这里 null 不会出现, 兜底清除
    delete moduleSortState.value[modId]
  } else {
    moduleSortState.value[modId] = { prop: sort.prop, order: sort.order }
  }
}

function getSortedMaterials(mod) {
  const st = moduleSortState.value[mod.id]
  const list = [...mod.materials]
  if (!st || !st.order) return list  // 用 backend default
  const dir = st.order === 'descending' ? -1 : 1
  list.sort((a, b) => {
    let va, vb
    if (st.prop === 'subtotal') {
      va = (a.unit_price || 0) * a.quantity
      vb = (b.unit_price || 0) * b.quantity
    } else {
      va = a[st.prop]
      vb = b[st.prop]
    }
    // 字符串 vs 数字比较
    if (typeof va === 'string' || typeof vb === 'string') {
      const sa = (va || '').toString()
      const sb = (vb || '').toString()
      return dir * sa.localeCompare(sb, 'zh-CN')
    }
    return dir * ((va || 0) - (vb || 0))
  })
  return list
}

// 当 props.moduleMaterials 变化时清除该模块的 sort 状态 (避免引用过期)
watch(() => props.moduleMaterials, () => {
  moduleSortState.value = {}
})

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
  // migration 017/019: 携带 material_type + product_name + category 快照, 后端 add_material_to_module 接收
  const materials = selectedMaterials.value.map(m => ({
    material_id: m.id,
    quantity: m._quantity || 1,
    material_type: m.material_type || 'other',
    product_name: m.product_name || null,  // migration 019
    category: m.category || null,  // migration 019
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

// 物料类型 (机械类/非机械类) — migration 017
function getMaterialTypeLabel(t) {
  const map = { mechanical: '机械类', electrical: '非机械类', other: '其他' }
  return map[t] || t || '其他'
}

// ---------------------------------------------------------------------------
// 导出无品号物料 (优选清单汇总表格式)
// ---------------------------------------------------------------------------
// 模块类型 -> 模板"类型"列
const MODULE_TYPE_TO_TEMPLATE = {
  mechanical: '机械类',
  electrical: '非机械类',
  other: '非机械类',
}

// 遍历所有模块分组, 找出无品号物料 (item_no 为空/纯空白/null)
const noItemNoMaterialsCount = computed(() => {
  let count = 0
  for (const group of props.groupedMaterials || []) {
    for (const mod of group.module_list || []) {
      for (const m of mod.materials || []) {
        // migration 020: 自制件不进"无品号导出" (用户明确需求)
        if (m.is_custom) continue
        if (!m.item_no || String(m.item_no).trim() === '') {
          count++
        }
      }
    }
  }
  return count
})

function exportNoItemNoMaterials() {
  // 按"类型 -> 部件分类 -> 产品名称"排序收集
  // migration 017: 类型列直接用 mm.material_type 快照, 不再从 module.module_type 推断
  // (module_type 是"模块类型/项目部/电控部", 跟物料类型不同维度)
  const rows = []
  let serialNo = 0
  // 物料类型 -> 模板"类型"列中文
  const TYPE_TO_TEMPLATE = {
    mechanical: '机械类',
    electrical: '非机械类',
    other: '其他',
  }

  for (const group of props.groupedMaterials || []) {
    for (const mod of group.module_list || []) {
      for (const m of mod.materials || []) {
        // migration 020: 自制件不进"无品号导出" (用户明确需求)
        if (m.is_custom) continue
        if (m.item_no && String(m.item_no).trim() !== '') continue
        serialNo++
        // 备注: param1/2/3 + 品牌, 用"/"分隔
        const params = [m.param1, m.param2, m.param3].filter(p => p && String(p).trim()).join(' / ')
        const remark = [m.brand, params].filter(Boolean).join(' | ')
        rows.push({
          '序号': serialNo,
          // migration 017: 用 mm.material_type 快照 (后端 to_dict 优先 self.material_type)
          '类型': TYPE_TO_TEMPLATE[m.material_type] || m.material_type || '其他',
          // migration 019: 部件分类用 mm.category 快照 (后端 to_dict 优先 self.category)
          '部件分类': getCategoryLabel(m.category),
          // migration 019: 产品名称用 mm.product_name 快照 (后端 to_dict 优先 self.product_name)
          '产品名称': m.product_name || '',
          '产品档次': '',  // 物料表无档次字段, 留空
          '选型关键因素1': m.param1 || '',
          '选型关键因素2': m.param2 || '',
          '选型关键因素3': m.param3 || '',
          '品号': '',  // 故意为空 - 这是"无品号物料"导出的核心目的
          '品名': m.material_name || '',
          '规格': m.specification || '',
          '初次确认报价日期': '',
          '价格更新周期\n（按照月计）': '',
          '价格维护\n（无品号）': '',
          '备注（机械规格）': remark,
        })
      }
    }
  }

  if (rows.length === 0) {
    ElMessage.warning('当前报价单所有物料都有品号, 无需导出')
    return
  }

  // 构造 worksheet (按模板列顺序)
  const headerOrder = [
    '序号', '类型', '部件分类', '产品名称', '产品档次',
    '选型关键因素1', '选型关键因素2', '选型关键因素3',
    '品号', '品名', '规格',
    '初次确认报价日期', '价格更新周期\n（按照月计）', '价格维护\n（无品号）',
    '备注（机械规格）',
  ]
  const aoa = [headerOrder]
  for (const r of rows) {
    aoa.push(headerOrder.map(h => r[h] ?? ''))
  }
  const ws = XLSX.utils.aoa_to_sheet(aoa)

  // 设置列宽 (参照模板风格, 让品号/品名/规格列更宽)
  ws['!cols'] = [
    { wch: 6 },   // 序号
    { wch: 10 },  // 类型
    { wch: 12 },  // 部件分类
    { wch: 22 },  // 产品名称
    { wch: 8 },   // 产品档次
    { wch: 22 },  // 选型关键因素1
    { wch: 22 },  // 选型关键因素2
    { wch: 22 },  // 选型关键因素3
    { wch: 14 },  // 品号
    { wch: 24 },  // 品名
    { wch: 28 },  // 规格
    { wch: 14 },  // 初次确认报价日期
    { wch: 14 },  // 价格更新周期
    { wch: 14 },  // 价格维护
    { wch: 28 },  // 备注
  ]

  // === 样式 (用户要求 2026-07-15: 头固定+背景色, 1-2列固定+背景色, 字体加粗, 2-4列筛选) ===
  // 浅灰色 (#D9D9D9) - 表头+冻结列统一底色
  const FROZEN_COL_FILL = { patternType: 'solid', fgColor: { rgb: 'FFD9D9D9' } }
  const HEADER_FILL = FROZEN_COL_FILL
  // 表头字体 (浅灰底用黑色字)
  const HEADER_FONT = { bold: true, color: { rgb: 'FF000000' }, name: '微软雅黑', sz: 11 }
  // 数据字体 (加粗)
  const DATA_FONT = { bold: true, name: '微软雅黑', sz: 11 }
  // 边框
  const BORDER = {
    top: { style: 'thin', color: { rgb: 'FF000000' } },
    bottom: { style: 'thin', color: { rgb: 'FF000000' } },
    left: { style: 'thin', color: { rgb: 'FF000000' } },
    right: { style: 'thin', color: { rgb: 'FF000000' } },
  }

  // 1. 表头样式: 深蓝底 + 白字加粗
  const headerRow = aoa[0]
  for (let c = 0; c < headerRow.length; c++) {
    const addr = XLSX.utils.encode_cell({ r: 0, c })
    if (ws[addr]) {
      ws[addr].s = { fill: HEADER_FILL, font: HEADER_FONT, border: BORDER, alignment: { horizontal: 'center', vertical: 'center', wrapText: true } }
    }
  }

  // 2. 数据行样式: 全部加粗 + 1-2 列 (序号/类型) 浅灰底
  for (let r = 1; r < aoa.length; r++) {
    for (let c = 0; c < headerRow.length; c++) {
      const addr = XLSX.utils.encode_cell({ r, c })
      if (!ws[addr]) continue
      // 1-2 列 (序号 A, 类型 B) 加浅灰底
      const fill = c <= 1 ? FROZEN_COL_FILL : undefined
      ws[addr].s = {
        font: DATA_FONT,
        border: BORDER,
        alignment: { horizontal: c <= 3 ? 'center' : 'left', vertical: 'center', wrapText: true },
        ...(fill ? { fill } : {}),
      }
    }
  }

  // 3. 冻结: 第 1 行 + 第 1-2 列 (用户要求 2026-07-15: 表格头固定 + 第 1-2 列固定)
  ws['!freeze'] = { xSplit: 2, ySplit: 1, topLeftCell: 'C2', activePane: 'bottomRight', state: 'frozen' }

  // 4. 筛选: B 到 D 列 (用户要求 2026-07-15: 第 2-4 列有刷选)
  //    ws['!autofilter'] = { ref: XLSX.utils.encode_range({ s: { r: 0, c: 1 }, e: { r: aoa.length - 1, c: 3 } }) }
  //    ↑ xlsx 社区版对 !autofilter 支持不稳定, 改用 worksheet 对象的 !autofilter (数字签名)
  ws['!autofilter'] = { ref: 'B1:D' + aoa.length }

  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, '无品号物料汇总')

  // 文件名: 优选清单汇总表_无品号_{YYYYMMDD_HHmm}.xlsx
  const now = new Date()
  const pad = n => String(n).padStart(2, '0')
  const ts = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}_${pad(now.getHours())}${pad(now.getMinutes())}`
  const filename = `优选清单汇总表_无品号_${ts}.xlsx`

  // xlsx-js-style 社区版不支持冻结窗格写入, 用 JSZip 后处理 sheet1.xml 加 pane 元素
  const buf = XLSX.write(wb, { bookType: 'xlsx', type: 'buffer' })
  JSZip.loadAsync(buf).then(zip => {
    return zip.file('xl/worksheets/sheet1.xml').async('string')
  }).then(sheetXml => {
    // 加冻结窗格: 第1行 + 前2列
    const newSheetXml = sheetXml.replace(
      '<sheetViews><sheetView workbookViewId="0"/>',
      '<sheetViews><sheetView workbookViewId="0"><pane xSplit="2" ySplit="1" topLeftCell="C2" activePane="bottomRight" state="frozen"/></sheetView>'
    )
    return JSZip.loadAsync(buf).then(zip => {
      zip.file('xl/worksheets/sheet1.xml', newSheetXml)
      return zip.generateAsync({ type: 'blob' })
    })
  }).then(blob => {
    // 下载
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
    ElMessage.success(`已导出 ${rows.length} 条无品号物料`)
  }).catch(err => {
    console.error('导出失败:', err)
    ElMessage.error('导出失败: ' + (err.message || '未知错误'))
  })
}
</script>

<style scoped>
/* 物料类型 (机械类/非机械类) — migration 017 */
.material-type-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
}
.material-type-tag.mechanical {
  background: #e3f2fd;
  color: #1565c0;
}
.material-type-tag.electrical {
  background: #fff3e0;
  color: #e65100;
}
.material-type-tag.other {
  background: #f5f5f5;
  color: #757575;
}

/* 自制件徽章 — migration 020 */
.custom-tag {
  display: inline-block;
  margin-left: 6px;
  padding: 1px 6px;
  background: linear-gradient(135deg, #ffd54f, #ffa726);
  color: #5d4037;
  border-radius: 3px;
  font-size: 11px;
  font-weight: 600;
  vertical-align: middle;
}

/* 自制件表单 tip + 样式 — migration 020 */
.custom-form-tip {
  margin-bottom: 16px;
}
.custom-form {
  max-width: 700px;
  padding-top: 8px;
}
.add-dialog-tabs {
  margin: -20px 0 0 0;
}
.add-dialog-tabs :deep(.el-tabs__header) {
  margin-bottom: 16px;
}
</style>
