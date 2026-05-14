<template>
  <div class="module-assignments">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>我的模块分配</span>
        </div>
      </template>

      <el-table :data="assignedModules" v-loading="loading" stripe>
        <el-table-column prop="module_name" label="模块名称" min-width="120" />
        <el-table-column prop="module_code" label="模块编码" width="120" />
        <el-table-column prop="quotation_name" label="所属报价单" min-width="150" />
        <el-table-column prop="quotation_scheme_no" label="方案号" width="150" />
        <el-table-column label="报价单状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.quotation_status === 'approved' ? 'success' : 'info'" size="small">
              {{ row.quotation_status === 'approved' ? '已归档' : '草稿' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="material_count" label="物料数量" width="100" align="center" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="openMaterialDialog(row)">
              维护物料
            </el-button>
          </template>
        </el-table-column>
        <template #empty>
          <el-empty description="您还没有被分配的模块" />
        </template>
      </el-table>
    </el-card>

    <!-- 物料维护弹窗 -->
    <el-dialog v-model="dialogVisible" :title="`维护物料 - ${currentModule?.module_name || ''}`" width="900px" align-center destroy-on-close>
      <div v-if="currentModule">
        <div class="module-info">
          <span>报价单：{{ currentModule.quotation_name }}</span>
          <span style="margin-left: 20px;">方案号：{{ currentModule.quotation_scheme_no }}</span>
          <el-tag v-if="currentModule.quotation_status === 'approved'" type="warning" size="small" style="margin-left: 20px;">
            已归档
          </el-tag>
        </div>

        <!-- 已归档提示 -->
        <el-alert
          v-if="currentModule.quotation_status === 'approved'"
          title="报价单已归档，物料变更需要提交审核"
          type="warning"
          :closable="false"
          show-icon
          style="margin-top: 12px;"
        >
          <template #default>
            您的物料修改将暂存，提交后由报价单负责人审核，审核通过后生效并更新版本。
          </template>
        </el-alert>

        <!-- 变更预览（仅归档报价单显示） -->
        <div v-if="currentModule.quotation_status === 'approved' && pendingChanges.length > 0" class="pending-changes">
          <el-divider>待提交的变更</el-divider>
          <el-tag v-for="change in pendingChanges" :key="change.id" :type="change.change_type === 'delete' ? 'danger' : (change.change_type === 'update' ? 'warning' : 'success')" style="margin-right: 8px;">
            {{ getChangeTypeLabel(change.change_type) }}: {{ change.material_name }}
          </el-tag>
          <el-button type="primary" size="small" style="margin-left: 16px;" @click="submitChangeRequest">
            提交变更申请
          </el-button>
          <el-button size="small" @click="clearPendingChanges">清空</el-button>
        </div>

        <!-- 物料列表 -->
        <el-table :data="moduleMaterials" border style="margin-top: 16px; max-height: 300px; overflow-y: auto;">
          <el-table-column prop="material_name" label="物料名称" min-width="120" />
          <el-table-column prop="specification" label="规格" min-width="100" />
          <el-table-column prop="brand" label="品牌" width="100" />
          <el-table-column prop="unit" label="单位" width="80" />
          <el-table-column prop="unit_price" label="单价" width="100" align="right" />
          <el-table-column prop="quantity" label="数量" width="100" align="center">
            <template #default="{ row }">
              <span v-if="isPendingDelete(row.id)" class="deleted-material">{{ row.quantity }} (待删除)</span>
              <el-input-number
                v-else-if="currentModule.quotation_status === 'approved'"
                v-model="row._temp_quantity"
                :min="1"
                size="small"
                @change="handleTempQuantityChange(row)"
              />
              <el-input-number
                v-else
                v-model="row.quantity"
                :min="1"
                size="small"
                @change="updateQuantity(row)"
              />
            </template>
          </el-table-column>
          <el-table-column label="小计" width="120" align="right">
            <template #default="{ row }">
              {{ ((parseFloat(row.unit_price) || 0) * (parseInt(isPendingDelete(row.id) ? 0 : (row._temp_quantity || row.quantity)) || 0)).toFixed(2) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="80">
            <template #default="{ row }">
              <el-button
                v-if="currentModule.quotation_status === 'approved'"
                type="danger"
                size="small"
                :disabled="isPendingDelete(row.id)"
                @click="markDelete(row)"
              >
                {{ isPendingDelete(row.id) ? '待删除' : '删除' }}
              </el-button>
              <el-button
                v-else
                type="danger"
                size="small"
                @click="removeMaterial(row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 物料合计 -->
        <div class="material-total">
          物料合计：{{ materialsTotal.toFixed(2) }} 元
        </div>

        <!-- 添加物料 -->
        <div class="add-material-section">
          <el-divider>添加物料</el-divider>

          <!-- 搜索过滤 -->
          <el-form inline style="margin-bottom: 12px;">
            <el-form-item label="物料名称">
              <el-input v-model="materialFilters.name" placeholder="输入物料名称" clearable style="width: 160px;" />
            </el-form-item>
            <el-form-item label="品牌">
              <el-input v-model="materialFilters.brand" placeholder="输入品牌" clearable style="width: 120px;" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchMaterials">搜索</el-button>
              <el-button @click="resetFilters">重置</el-button>
            </el-form-item>
          </el-form>

          <!-- 物料选择表格 -->
          <el-table
            :data="paginatedMaterials"
            border
            max-height="250"
            style="margin-bottom: 12px;"
          >
            <el-table-column prop="name" label="物料名称" min-width="140" />
            <el-table-column prop="code" label="编码" width="100" />
            <el-table-column prop="spec" label="规格" min-width="100" />
            <el-table-column prop="brand" label="品牌" width="100" />
            <el-table-column prop="unit" label="单位" width="70" />
            <el-table-column prop="unit_price" label="单价" width="90" align="right" />
            <el-table-column label="操作" width="80" fixed="right">
              <template #default="{ row }">
                <el-button
                  type="primary"
                  size="small"
                  :disabled="isMaterialAdded(row.id)"
                  @click="selectMaterial(row)"
                >
                  {{ isMaterialAdded(row.id) ? '已添加' : '添加' }}
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <el-pagination
            v-model:current-page="materialPagination.page"
            v-model:page-size="materialPagination.pageSize"
            :total="materialPagination.total"
            :page-sizes="[5, 10, 20]"
            layout="total, sizes, prev, pager, next"
            small
            style="text-align: right;"
          />

          <!-- 添加数量 -->
          <div v-if="selectedMaterialForAdd" style="margin-top: 12px; text-align: right;">
            <span style="margin-right: 8px;">已选：{{ selectedMaterialForAdd.name }}</span>
            <el-input-number v-model="addQuantity" :min="1" size="small" />
            <el-button type="primary" size="small" style="margin-left: 8px;" @click="confirmAddMaterial">确认添加</el-button>
            <el-button size="small" style="margin-left: 4px;" @click="cancelAddMaterial">取消</el-button>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/api/request'
import changeRequestsAPI from '@/api/changeRequests'

const assignedModules = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const currentModule = ref(null)
const moduleMaterials = ref([])
const allMaterials = ref([])
const selectedMaterialId = ref(null)
const addQuantity = ref(1)
const selectedMaterialForAdd = ref(null)

// 待提交的变更（用于归档报价单）
const pendingChanges = ref([])
const pendingDeletes = ref(new Set())

// 物料搜索和分页
const materialFilters = ref({ name: '', brand: '' })
const materialPagination = ref({ page: 1, pageSize: 10, total: 0 })

const materialsTotal = computed(() => {
  return moduleMaterials.value.reduce((sum, m) => {
    if (isPendingDelete(m.id)) return sum
    const price = parseFloat(m.unit_price) || 0
    const qty = parseInt(m._temp_quantity !== undefined ? m._temp_quantity : m.quantity) || 0
    return sum + (price * qty)
  }, 0)
})

// 过滤后的物料数据
const filteredMaterials = computed(() => {
  let result = allMaterials.value
  if (materialFilters.value.name) {
    const name = materialFilters.value.name.toLowerCase()
    result = result.filter(m => (m.name || '').toLowerCase().includes(name))
  }
  if (materialFilters.value.brand) {
    const brand = materialFilters.value.brand.toLowerCase()
    result = result.filter(m => (m.brand || '').toLowerCase().includes(brand))
  }
  return result
})

// 分页后的物料数据
const paginatedMaterials = computed(() => {
  const start = (materialPagination.value.page - 1) * materialPagination.value.pageSize
  const end = start + materialPagination.value.pageSize
  return filteredMaterials.value.slice(start, end)
})

// 检查物料是否已添加
function isMaterialAdded(materialId) {
  try {
    if (!moduleMaterials.value) return false
    return moduleMaterials.value.some(m => (m.material_id === materialId || m.id === materialId) && !isPendingDelete(m.id))
  } catch (e) {
    console.error('isMaterialAdded error:', e)
    return false
  }
}

// 检查是否标记删除
function isPendingDelete(materialId) {
  return pendingDeletes.value.has(materialId)
}

// 获取变更类型标签
function getChangeTypeLabel(type) {
  const map = { add: '添加', update: '更新', delete: '删除' }
  return map[type] || type
}

onMounted(() => {
  fetchAssignedModules()
})

async function fetchAssignedModules() {
  loading.value = true
  try {
    const res = await request.get('/quotations/my-assigned-modules')
    assignedModules.value = res.data || res || []
  } catch (error) {
    console.error('获取分配的模块失败:', error)
    assignedModules.value = []
  } finally {
    loading.value = false
  }
}

async function openMaterialDialog(module) {
  currentModule.value = module
  dialogVisible.value = true
  // 重置变更状态
  pendingChanges.value = []
  pendingDeletes.value = new Set()
  await Promise.all([
    fetchModuleMaterials(module.id),
    fetchAvailableMaterials()
  ])
}

async function fetchModuleMaterials(moduleId) {
  try {
    const res = await request.get(`/modules/${moduleId}/materials`)
    const materials = res.data || res || []
    // 为每个物料添加临时数量字段
    moduleMaterials.value = materials.map(m => ({ ...m, _temp_quantity: m.quantity }))
  } catch (error) {
    ElMessage.error('加载物料失败')
  }
}

async function fetchAvailableMaterials() {
  try {
    const res = await request.get('/materials?status=active&limit=1000')
    const data = res.data || res || []
    allMaterials.value = data
    materialPagination.value.total = data.length
  } catch (error) {
    allMaterials.value = []
  }
}

function searchMaterials() {
  materialPagination.value.page = 1
}

function resetFilters() {
  materialFilters.value = { name: '', brand: '' }
  materialPagination.value.page = 1
}

function selectMaterial(row) {
  console.log('selectMaterial called with:', row)
  selectedMaterialForAdd.value = row
  addQuantity.value = 1
  console.log('selectedMaterialForAdd:', selectedMaterialForAdd.value)
}

function confirmAddMaterial() {
  console.log('confirmAddMaterial called')
  console.log('selectedMaterialForAdd:', selectedMaterialForAdd.value)
  console.log('currentModule:', currentModule.value)
  if (!selectedMaterialForAdd.value) {
    console.log('No material selected')
    return
  }
  selectedMaterialId.value = selectedMaterialForAdd.value.id
  console.log('selectedMaterialId:', selectedMaterialId.value)

  if (currentModule.value.quotation_status === 'approved') {
    // 归档报价单：暂存添加变更
    pendingChanges.value.push({
      id: `add_${Date.now()}`,
      change_type: 'add',
      material_id: selectedMaterialId.value,
      material_name: selectedMaterialForAdd.value.name,
      quantity: addQuantity.value
    })
    ElMessage.info('已添加到变更列表，请点击"提交变更申请"提交审核')
    cancelAddMaterial()
  } else {
    performAddMaterial()
  }
}

function cancelAddMaterial() {
  selectedMaterialForAdd.value = null
  addQuantity.value = 1
  selectedMaterialId.value = null
}

async function performAddMaterial() {
  if (!selectedMaterialId.value) {
    ElMessage.warning('请选择物料')
    return
  }
  try {
    await request.post(`/modules/${currentModule.value.id}/materials`, {
      material_id: selectedMaterialId.value,
      quantity: addQuantity.value
    })
    ElMessage.success('物料已添加')
    await fetchModuleMaterials(currentModule.value.id)
    cancelAddMaterial()
  } catch (error) {
    ElMessage.error('添加物料失败')
  }
}

// 处理归档报价单的临时数量变更
function handleTempQuantityChange(row) {
  const originalQty = row.quantity
  const newQty = row._temp_quantity

  if (originalQty !== newQty) {
    // 查找是否有该物料的更新记录
    const existingIdx = pendingChanges.value.findIndex(c => c.material_id === row.material_id && c.change_type === 'update')
    if (existingIdx >= 0) {
      pendingChanges.value[existingIdx].quantity = newQty
    } else {
      pendingChanges.value.push({
        id: `update_${row.id}`,
        change_type: 'update',
        material_id: row.material_id,
        material_name: row.material_name,
        original_quantity: originalQty,
        quantity: newQty
      })
    }
  }
}

// 标记删除（归档报价单）
function markDelete(row) {
  pendingDeletes.value.add(row.id)
  // 移除该物料的更新记录
  pendingChanges.value = pendingChanges.value.filter(c => c.material_id !== row.material_id || c.change_type !== 'update')
  // 添加删除记录
  pendingChanges.value.push({
    id: row.id,  // 使用模块物料ID（不是 material_id）
    change_type: 'delete',
    material_id: row.material_id,
    material_name: row.material_name,
    original_quantity: row.quantity
  })
}

// 提交变更申请
async function submitChangeRequest() {
  if (pendingChanges.value.length === 0) {
    ElMessage.warning('没有可提交的变更')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要提交 ${pendingChanges.value.length} 项变更申请吗？提交后将由报价单负责人审核。`,
      '提交变更申请',
      { type: 'warning' }
    )

    for (const change of pendingChanges.value) {
      await changeRequestsAPI.create({
        quotation_id: currentModule.value.quotation_id,
        module_id: currentModule.value.id,
        change_type: `material_${change.change_type}`,
        proposed_data: change.change_type === 'add' ? { material_id: change.material_id, quantity: change.quantity } :
                       change.change_type === 'update' ? { id: change.id, quantity: change.quantity } : {},
        original_data: change.change_type === 'delete' || change.change_type === 'update' ?
                       { id: change.id, quantity: change.original_quantity } : {},
      })
    }

    ElMessage.success('变更申请已提交，请等待审核')
    dialogVisible.value = false
    pendingChanges.value = []
    pendingDeletes.value = new Set()
    await fetchAssignedModules()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('提交变更申请失败')
    }
  }
}

// 清空待提交变更
function clearPendingChanges() {
  pendingChanges.value = []
  pendingDeletes.value = new Set()
  // 重置临时数量
  moduleMaterials.value.forEach(m => {
    m._temp_quantity = m.quantity
  })
}

async function updateQuantity(row) {
  try {
    await request.put(`/module_materials/${row.id}`, {
      quantity: row.quantity
    })
    ElMessage.success('数量已更新')
  } catch (error) {
    ElMessage.error('更新数量失败')
  }
}

async function removeMaterial(row) {
  try {
    await ElMessageBox.confirm('确定要删除该物料吗？', '提示', { type: 'warning' })
    await request.delete(`/module_materials/${row.id}`)
    ElMessage.success('已删除')
    moduleMaterials.value = moduleMaterials.value.filter(m => m.id !== row.id)
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}
</script>

<style scoped>
.module-assignments {
  padding: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.module-info {
  background: #f5f7fa;
  padding: 12px;
  border-radius: 4px;
  color: #606266;
}

.material-total {
  text-align: right;
  margin-top: 16px;
  font-size: 16px;
  font-weight: bold;
  color: #409eff;
}

.add-material-section {
  margin-top: 16px;
}

.pending-changes {
  margin-top: 12px;
  padding: 12px;
  background: #fff8e6;
  border-radius: 4px;
}

.deleted-material {
  color: #909399;
  text-decoration: line-through;
}
</style>
