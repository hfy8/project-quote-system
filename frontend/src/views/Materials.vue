<template>
  <div class="materials-page">
    <!-- 左侧分类导航 -->
    <aside class="category-sidebar">
      <div class="sidebar-header">
        <h3 class="sidebar-title">📦 物料分类</h3>
      </div>
      <nav class="category-nav">
        <button
          v-for="cat in categories"
          :key="cat.value"
          class="category-item"
          :class="{ active: activeCategory === cat.value }"
          @click="handleCategoryChange(cat.value)"
        >
          <span class="cat-icon">{{ cat.icon }}</span>
          <span class="cat-name">{{ cat.label }}</span>
          <span class="cat-count">{{ getCategoryCount(cat.value) }}</span>
        </button>
      </nav>
    </aside>

    <!-- 右侧主内容 -->
    <main class="main-content">
      <!-- 页面标题栏 -->
      <div class="page-header-bar">
        <div class="header-left">
          <h1 class="page-title">原材料库</h1>
          <span class="page-desc">共 {{ pagination.total }} 种物料</span>
        </div>
        <div class="header-actions">
          <button class="btn btn-secondary" @click="handleImport">
            <span>📥</span> 批量导入
          </button>
          <button class="btn btn-primary" @click="handleAdd">
            <span>+</span> 新增物料
          </button>
        </div>
      </div>

      <!-- 筛选栏 -->
      <div class="filter-bar card">
        <div class="filter-group">
          <el-input
            v-model="keyword"
            placeholder="搜索物料名称、规格、品牌..."
            clearable
            class="search-input"
          >
            <template #prefix>
              <span>🔍</span>
            </template>
          </el-input>
        </div>
        <button class="btn btn-secondary" @click="fetchData">搜索</button>
      </div>

      <!-- 数据表格 -->
      <div class="table-wrapper">
        <el-table
          :data="tableData"
          v-loading="loading"
          stripe
          class="materials-table"
          :height="'100%'"
          :scrollbar-always-on="true"
          show-overflow-tooltip
        >
          <el-table-column prop="name" label="品名" min-width="120">
            <template #default="{ row }">
              <div class="material-name">
                <span class="name-text">{{ row.name }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="item_no" label="品号" min-width="120">
            <template #default="{ row }">
              <span v-if="row.item_no" style="font-family: monospace;">{{ row.item_no }}</span>
              <span v-else style="color: #c0c4cc;">-</span>
            </template>
          </el-table-column>
          <el-table-column prop="spec" label="规格" min-width="100">
            <template #default="{ row }">
              <span class="spec-text">{{ row.spec || '-' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="brand" label="品牌" width="100">
            <template #default="{ row }">
              <span class="brand-text">{{ row.brand || '-' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="param1" label="关键参数01" min-width="130">
            <template #default="{ row }">
              <span class="param-text">{{ row.param1 || '-' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="param2" label="关键参数02" min-width="130">
            <template #default="{ row }">
              <span class="param-text">{{ row.param2 || '-' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="param3" label="关键参数03" min-width="130">
            <template #default="{ row }">
              <span class="param-text">{{ row.param3 || '-' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="category" label="分类" width="100">
            <template #default="{ row }">
              <span class="category-tag" :class="row.category">
                {{ getCategoryLabel(row.category) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="unit" label="单位" width="80">
            <template #default="{ row }">
              <span class="unit-text">{{ row.unit }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="unit_price" label="单价" width="140">
            <template #default="{ row }">
              <span class="price-text">¥ {{ row.unit_price?.toLocaleString() }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="140" fixed="right">
            <template #default="{ row }">
              <div class="action-buttons">
                <button class="action-btn edit" @click="handleEdit(row)">编辑</button>
                <button class="action-btn delete" @click="handleDelete(row)">删除</button>
              </div>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination-wrapper">
          <el-pagination
            v-model:current-page="pagination.page"
            v-model:page-size="pagination.pageSize"
            :total="pagination.total"
            :page-sizes="[10, 20, 50]"
            layout="total, sizes, prev, pager, next"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </main>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="520px" class="material-dialog">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px" class="dialog-form">
        <el-form-item label="品名" prop="name">
          <el-input v-model="form.name" placeholder="请输入物料品名" />
        </el-form-item>
        <el-form-item label="品号" prop="item_no">
          <el-input v-model="form.item_no" placeholder="可留空, 跨系统同步用" maxlength="50" clearable />
        </el-form-item>
        <el-form-item label="规格" prop="spec">
          <el-input v-model="form.spec" placeholder="请输入规格" />
        </el-form-item>
        <el-form-item label="品牌" prop="brand">
          <el-input v-model="form.brand" placeholder="请输入品牌" />
        </el-form-item>
        <el-form-item label="关键参数01" prop="param1">
          <el-input v-model="form.param1" placeholder="请输入关键参数01" />
        </el-form-item>
        <el-form-item label="关键参数02" prop="param2">
          <el-input v-model="form.param2" placeholder="请输入关键参数02" />
        </el-form-item>
        <el-form-item label="关键参数03" prop="param3">
          <el-input v-model="form.param3" placeholder="请输入关键参数03" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category" placeholder="请选择分类" style="width: 100%;">
            <el-option label="大件" value="large" />
            <el-option label="核心部件" value="standard" />
            <el-option label="其他件" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="单位" prop="unit">
          <el-input v-model="form.unit" placeholder="如: 个、米、套" />
        </el-form-item>
        <el-form-item label="单价" prop="unit_price">
          <el-input-number v-model="form.unit_price" :min="0" :precision="2" style="width: 100%;" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="dialogVisible = false">取消</button>
          <button class="confirm-btn" @click="handleSubmit">确定</button>
        </div>
      </template>
    </el-dialog>

    <!-- 导入弹窗 -->
    <el-dialog v-model="importDialogVisible" title="批量导入" width="400px" class="import-dialog">
      <div class="import-content">
        <el-upload
          ref="uploadRef"
          :auto-upload="false"
          :limit="1"
          accept=".xlsx,.xls"
          action="/api/materials/import"
          class="import-upload"
        >
          <template #trigger>
            <button class="upload-btn">
              <span>📁</span>
              <span>选择 Excel 文件</span>
            </button>
          </template>
        </el-upload>
        <p class="import-tip">支持 .xlsx 和 .xls 格式</p>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="importDialogVisible = false">取消</button>
          <button class="confirm-btn" @click="handleImportSubmit">上传</button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { materialsAPI } from '../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const tableData = ref([])
const keyword = ref('')
const activeCategory = ref('all')

const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

const dialogVisible = ref(false)
const importDialogVisible = ref(false)
const dialogTitle = ref('新增物料')
const formRef = ref(null)

const categories = [
  { label: '全部', value: 'all', icon: '📋' },
  { label: '大件', value: 'large', icon: '📦' },
  { label: '核心部件', value: 'standard', icon: '📚' },
  { label: '其他件', value: 'other', icon: '📎' }
]

const form = reactive({
  id: null,
  item_no: '',  // 品号 (跨系统同步用, 允许为空)
  name: '',
  spec: '',
  brand: '',
  category: 'standard',
  unit: '',
  unit_price: 0,
  param1: '',
  param2: '',
  param3: ''
})

const rules = {
  name: [{ required: true, message: '请输入品名', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  unit: [{ required: true, message: '请输入单位', trigger: 'blur' }],
  unit_price: [{ required: true, message: '请输入单价', trigger: 'blur' }]
}

const getCategoryCount = (cat) => {
  if (cat === 'all') return tableData.value.length
  return tableData.value.filter(item => item.category === cat).length
}

const getCategoryLabel = (cat) => {
  const map = { large: '大件', standard: '核心部件', other: '其他件' }
  return map[cat] || cat || '-'
}

const handleCategoryChange = (val) => {
  activeCategory.value = val
  pagination.page = 1
  fetchData()
}

const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
      keyword: keyword.value,
      category: activeCategory.value === 'all' ? '' : activeCategory.value
    }
    const res = await materialsAPI.getList(params)
    tableData.value = res.items || res || []
    pagination.total = res.total || tableData.value.length
  } catch (error) {
    console.error('Failed to fetch materials:', error)
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  fetchData()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchData()
}

const handleAdd = () => {
  dialogTitle.value = '新增物料'
  Object.assign(form, { id: null, item_no: '', name: '', spec: '', brand: '', category: 'standard', unit: '', unit_price: 0, param1: '', param2: '', param3: '' })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑物料'
  Object.assign(form, row)
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (form.id) {
          await materialsAPI.update(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await materialsAPI.create(form)
          ElMessage.success('新增成功')
        }
        dialogVisible.value = false
        fetchData()
      } catch (error) {
        ElMessage.error('操作失败')
      }
    }
  })
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除物料「${row.name}」吗？删除后无法恢复。`,
      '确认删除',
      { confirmButtonText: '删除', cancelButtonText: '取消', type: 'warning' }
    )
    await materialsAPI.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleImport = () => {
  importDialogVisible.value = true
}

const handleImportSubmit = () => {
  ElMessage.info('导入功能开发中')
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.materials-page {
  display: flex;
  gap: var(--spacing-lg);
  padding: var(--spacing-lg);
  height: 100vh;
  overflow: hidden;
  box-sizing: border-box;
  min-width: 0;
}

/* 左侧分类导航 */
.category-sidebar {
  width: 220px;
  flex-shrink: 0;
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  overflow: hidden;
  height: fit-content;
  position: sticky;
  top: 0;
}

.sidebar-header {
  padding: var(--spacing-md) var(--spacing-lg);
  border-bottom: 1px solid var(--color-border-light);
}

.sidebar-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.category-nav {
  padding: var(--spacing-sm);
}

.category-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: none;
  background: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  text-align: left;
}

.category-item:hover {
  background: var(--color-bg-hover);
}

.category-item.active {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.cat-icon {
  font-size: 16px;
}

.cat-name {
  flex: 1;
  font-size: 14px;
  color: var(--color-text-primary);
}

.cat-count {
  font-size: 12px;
  padding: 2px 8px;
  background: var(--color-bg-hover);
  border-radius: var(--radius-full);
  color: var(--color-text-muted);
}

.category-item.active .cat-count {
  background: rgba(13, 148, 136, 0.15);
  color: var(--color-primary);
}

/* 右侧主内容 */
.main-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

/* 页面标题栏 */
.page-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  flex-shrink: 1;
  min-width: 0;
  width: 100%;
  box-sizing: border-box;
}

.header-left {
  display: flex;
  align-items: baseline;
  gap: var(--spacing-sm);
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.page-desc {
  font-size: 14px;
  color: var(--color-text-muted);
}

.header-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  border: none;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
}

.btn-primary:hover {
  background: var(--color-primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-secondary {
  background: var(--color-bg-card);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

.btn-secondary:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-primary);
}

/* 筛选栏 */
.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) var(--spacing-md);
  margin-bottom: var(--spacing-sm);
  background: var(--color-bg-card);
  border-radius: var(--radius-md);
  flex-shrink: 1;
  min-width: 0;
  width: 100%;
  box-sizing: border-box;
}

.filter-group {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

.search-input {
  width: 300px;
}

/* 数据表格 */
.table-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
}

.table-wrapper :deep(.el-table__header-wrapper table),
.table-wrapper :deep(.el-table__body-wrapper table) {
  table-layout: fixed !important;
  width: 100% !important;
}

.table-wrapper :deep(.el-table) {
  display: block !important;
  width: 100% !important;
  table-layout: fixed;
  min-width: 0;
  overflow-x: auto;
}

.materials-table {
  --el-table-border-color: var(--color-border-light);
  width: 100% !important;
  min-width: 0;
}

.table-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  width: 100%;
  min-width: 0;
  box-sizing: border-box;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  padding: var(--spacing-sm) var(--spacing-md);
  border-top: 1px solid var(--color-border-light);
  flex-shrink: 0;
}

.unit-text {
  font-size: 13px;
  color: var(--color-text-secondary);
}

.material-name .name-text {
  font-weight: 500;
  color: var(--color-text-primary);
}

.spec-text,
.brand-text {
  font-size: 13px;
  color: var(--color-text-secondary);
}

/* 分类标签 */
.category-tag {
  display: inline-block;
  padding: 2px 10px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 500;
}

.category-tag.large {
  background: var(--color-warning-bg);
  color: var(--color-warning);
}

.category-tag.standard {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.category-tag.other {
  background: var(--color-secondary-light);
  color: var(--color-secondary);
}

.price-text {
  font-weight: 600;
  color: var(--color-text-primary);
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: var(--spacing-sm);
}

.action-btn {
  padding: 4px 12px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  border: none;
  background: none;
}

.action-btn.edit {
  color: var(--color-primary);
  background: var(--color-primary-light);
}

.action-btn.edit:hover {
  background: var(--color-primary);
  color: white;
}

.action-btn.delete {
  color: var(--color-danger);
  background: var(--color-danger-bg);
}

.action-btn.delete:hover {
  background: var(--color-danger);
  color: white;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  padding: var(--spacing-md) var(--spacing-lg);
  border-top: 1px solid var(--color-border-light);
}

/* 弹窗样式 */
.material-dialog :deep(.el-dialog__header) {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--color-border-light);
}

.material-dialog :deep(.el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.material-dialog :deep(.el-dialog__body) {
  padding: var(--spacing-lg);
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
}

.cancel-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--radius-md);
  font-size: 14px;
  background: var(--color-bg-card);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
  cursor: pointer;
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
}

.confirm-btn:hover {
  background: var(--color-primary-hover);
}

/* 导入弹窗 */
.import-content {
  text-align: center;
  padding: var(--spacing-lg);
}

.upload-btn {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xl);
  background: var(--color-bg-hover);
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-fast);
  width: 100%;
}

.upload-btn:hover {
  border-color: var(--color-primary);
  background: var(--color-primary-light);
}

.upload-btn span:first-child {
  font-size: 32px;
}

.upload-btn span:last-child {
  font-size: 14px;
  color: var(--color-text-primary);
}

.import-tip {
  margin-top: var(--spacing-md);
  font-size: 13px;
  color: var(--color-text-muted);
}

/* 响应式 */
@media (max-width: 1024px) {
  .materials-page {
    flex-direction: column;
  }

  .category-sidebar {
    width: 100%;
  }

  .category-nav {
    display: flex;
    gap: var(--spacing-sm);
    overflow-x: auto;
  }

  .category-item {
    flex-shrink: 0;
  }
}
</style>