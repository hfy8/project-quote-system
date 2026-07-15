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
          <el-table-column prop="material_type" label="类型" width="100">
            <template #default="{ row }">
              <span class="material-type-tag" :class="row.material_type || 'other'">
                {{ getMaterialTypeLabel(row.material_type) }}
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
        <el-form-item label="类型" prop="material_type">
          <el-select v-model="form.material_type" placeholder="请选择类型" style="width: 100%;">
            <el-option label="机械类" value="mechanical" />
            <el-option label="非机械类" value="electrical" />
            <el-option label="其他" value="other" />
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
    <el-dialog v-model="importDialogVisible" title="批量导入" width="760px" class="import-dialog" :close-on-click-modal="false" destroy-on-close>
      <div class="import-content">
        <!-- 步骤1: 选择文件 (没解析时显示) -->
        <div v-if="!parsedData.length && !fileLoaded" class="import-upload-zone">
          <input
            ref="fileInputRef"
            type="file"
            accept=".xlsx,.xls"
            style="display:none"
            @change="handleFileChange"
          />
          <div class="upload-area" @click="fileInputRef?.click()" @dragover.prevent @drop.prevent="handleDrop">
            <div class="upload-icon">📁</div>
            <div class="upload-text">
              <p>点击选择或拖拽 Excel 文件到此处</p>
              <p class="upload-hint">支持 .xlsx 和 .xls 格式, 推荐使用「汇总表」sheet</p>
            </div>
          </div>
        </div>

        <!-- 步骤2: 解析结果预览 -->
        <div v-if="parsedData.length > 0">
          <!-- 统计信息 -->
          <div class="import-stats">
            <div class="stat-item stat-created">
              <span class="stat-num">{{ stats.created }}</span>
              <span class="stat-label">导入</span>
            </div>
            <div class="stat-item stat-updated">
              <span class="stat-num">{{ stats.updated }}</span>
              <span class="stat-label">更新</span>
            </div>
            <div class="stat-item stat-skipped">
              <span class="stat-num">{{ stats.skipped }}</span>
              <span class="stat-label">跳过</span>
            </div>
            <div class="stat-item stat-total">
              <span class="stat-num">{{ stats.parsed }}</span>
              <span class="stat-label">解析共</span>
            </div>
          </div>

          <!-- 预览表格 -->
          <el-table :data="parsedData" max-height="320" stripe size="small" class="preview-table">
            <el-table-column type="index" label="#" width="40" />
            <el-table-column prop="name" label="品名" min-width="100" />
            <el-table-column prop="item_no" label="品号" min-width="110" />
            <el-table-column prop="spec" label="规格" min-width="120" />
            <el-table-column prop="category" label="分类" width="80">
              <template #default="{ row }">
                <span :class="'cat-tag ' + row.category">{{ row.category === 'large' ? '大件' : '标准' }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="param1" label="关键参数1" min-width="100" show-overflow-tooltip />
            <el-table-column prop="param2" label="关键参数2" min-width="100" show-overflow-tooltip />
            <el-table-column prop="param3" label="关键参数3" min-width="100" show-overflow-tooltip />
            <el-table-column label="操作" width="60">
              <template #default="{ $index }">
                <button class="action-btn delete" @click="removePreviewRow($index)" title="移除">✕</button>
              </template>
            </el-table-column>
          </el-table>

          <div class="import-actions-bar">
            <button class="btn btn-secondary" @click="resetImport">重新选择文件</button>
            <span class="import-info">预览 {{ parsedData.length }} 条, 确认后提交</span>
            <button class="btn btn-primary" :loading="importing" @click="confirmImport">确认导入</button>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { materialsAPI } from '../api'
import { ElMessage, ElMessageBox } from 'element-plus'
import * as XLSX from 'xlsx'

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
  material_type: 'other',  // 机械类/非机械类 — migration 016
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

// 物料类型 (机械类/非机械类) — migration 016
const getMaterialTypeLabel = (t) => {
  const map = { mechanical: '机械类', electrical: '非机械类', other: '其他' }
  return map[t] || t || '其他'
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
  Object.assign(form, { id: null, item_no: '', name: '', spec: '', brand: '', category: 'standard', material_type: 'other', unit: '', unit_price: 0, param1: '', param2: '', param3: '' })
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

// ========== 批量导入逻辑 ==========
const fileInputRef = ref(null)
const parsedData = ref([])
const fileLoaded = ref(false)
const importing = ref(false)
const stats = reactive({ parsed: 0, created: 0, updated: 0, skipped: 0 })

const CATEGORY_MAP = { '大件': 'large', '关键核心部件': 'standard' }
// 模板"类型"列 (机械类/非机械类) → 枚举值, 兼容"非机械类（电控）"等带括号写法
const MATERIAL_TYPE_MAP = {
  '机械类': 'mechanical',
  '非机械类': 'electrical',
  '非机械类（电控）': 'electrical',
  '非机械类(电控)': 'electrical',
  '电控软件类': 'electrical',
  '其他': 'other',
}

const handleImport = () => {
  resetImport()
  importDialogVisible.value = true
}

const resetImport = () => {
  parsedData.value = []
  fileLoaded.value = false
  importing.value = false
  stats.parsed = 0; stats.created = 0; stats.updated = 0; stats.skipped = 0
}

const handleFileChange = (e) => {
  const file = e.target.files?.[0]
  if (file) parseExcel(file)
}

const handleDrop = (e) => {
  const file = e.dataTransfer?.files?.[0]
  if (file) parseExcel(file)
}

const parseExcel = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const data = new Uint8Array(e.target.result)
      const workbook = XLSX.read(data, { type: 'array' })

      // 优先选 '汇总表' sheet
      let sheetName = workbook.SheetNames.find(n => n.includes('汇总'))
      if (!sheetName) sheetName = workbook.SheetNames[0]

      const sheet = workbook.Sheets[sheetName]
      const rows = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: '' })

      // 跳过空行, 找到表头行
      let headerIdx = -1
      for (let i = 0; i < rows.length; i++) {
        const cells = rows[i]
        if (cells.some(c => String(c).includes('品号') || String(c).includes('品名'))) {
          headerIdx = i
          break
        }
      }
      if (headerIdx < 0) {
        ElMessage.error('未找到表头行 (需要包含"品号"、"品名"等列)')
        return
      }

      const headers = rows[headerIdx].map(h => String(h).trim())
      // 列索引映射
      const colIdx = {
        name: headers.findIndex(h => h.includes('品名')),
        itemNo: headers.findIndex(h => h.includes('品号')),
        spec: headers.findIndex(h => h.includes('规格')),
        // 部件分类 (大件/关键核心部件/其他件) — 注意必须排除"类型"列
        partCat: headers.findIndex(h => h === '部件分类' || h === '分类'),
        // 类型 (机械类/非机械类) — 模板"汇总表"第一列
        materialType: headers.findIndex(h => h === '类型' || h.includes('物料类型')),
        param1: headers.findIndex(h => h.includes('关键因素1') || h.includes('选型关键因素1') || h.includes('关键参数01')),
        param2: headers.findIndex(h => h.includes('关键因素2') || h.includes('选型关键因素2') || h.includes('关键参数02')),
        param3: headers.findIndex(h => h.includes('关键因素3') || h.includes('选型关键因素3') || h.includes('关键参数03')),
        unitPrice: headers.findIndex(h => h.includes('价格维护')),
      }

      // 解析数据行 (Excel 内去重: 品号 OR 品名+规格 唯一, 后端会处理 upsert)
      const seenItemNos = new Set()
      const seenNameSpec = new Set()
      const materials = []
      let skipped = 0

      for (let r = headerIdx + 1; r < rows.length; r++) {
        const cells = rows[r]
        // 跳过全空行
        if (!cells.length || cells.every(c => !String(c).trim())) continue

        const itemNo = String(cells[colIdx.itemNo] || '').trim()
        const name = String(cells[colIdx.name] || '').trim()
        const spec = String(cells[colIdx.spec] || '').trim()

        // Excel 内去重 (同品号只保留首次; 无品号不算品号重复)
        if (itemNo && seenItemNos.has(itemNo)) {
          skipped++
          continue
        }
        if (itemNo) seenItemNos.add(itemNo)

        // 品名+规格联合唯一 (有品名和规格才参与)
        const nameSpecKey = name && spec ? `${name}||${spec}` : ''
        if (nameSpecKey && seenNameSpec.has(nameSpecKey)) {
          skipped++
          continue
        }
        if (nameSpecKey) seenNameSpec.add(nameSpecKey)

        const partCatRaw = String(cells[colIdx.partCat] || '').trim()
        const category = CATEGORY_MAP[partCatRaw] || 'standard'
        // 物料类型 (机械类/非机械类) — migration 016, 没匹配到默认 'other'
        const typeRaw = String(cells[colIdx.materialType] || '').trim()
        const material_type = MATERIAL_TYPE_MAP[typeRaw] || 'other'
        const param1 = String(cells[colIdx.param1] || '').trim()
        const param2 = String(cells[colIdx.param2] || '').trim()
        const param3 = String(cells[colIdx.param3] || '').trim()

        // 价格: Excel 有则取, 无则 null (后端不更新已存在的价格)
        const priceRaw = colIdx.unitPrice >= 0 ? cells[colIdx.unitPrice] : null
        const priceNum = priceRaw !== null && priceRaw !== '' && !isNaN(Number(priceRaw)) ? Number(priceRaw) : null

        materials.push({
          item_no: itemNo,
          name: name || itemNo, // 回退
          spec,
          brand: '',
          unit: 'pcs',
          unit_price: priceNum, // null 表示"无价格"信号
          category,
          material_type,  // migration 016 - 机械类/非机械类
          param1: param1 || undefined,
          param2: param2 || undefined,
          param3: param3 || undefined,
        })
      }

      // 假设导入的都是新物料 (后端会做最终 upsert 判断)
      const totalParsed = materials.length
      parsedData.value = materials
      fileLoaded.value = true
      stats.parsed = totalParsed + skipped
      stats.created = totalParsed
      stats.updated = 0
      stats.skipped = skipped

      ElMessage.success(`解析完成: 解析 ${totalParsed + skipped} 行, 导入 ${totalParsed} 条, 跳过 ${skipped} 行`)

    } catch (err) {
      console.error('Excel 解析失败:', err)
      ElMessage.error('Excel 解析失败: ' + err.message)
    }
  }
  reader.onerror = () => ElMessage.error('文件读取失败')
  reader.readAsArrayBuffer(file)
}

const removePreviewRow = (index) => {
  parsedData.value.splice(index, 1)
  stats.created = parsedData.value.length
}

const confirmImport = async () => {
  if (!parsedData.value.length) {
    ElMessage.warning('没有可导入的数据')
    return
  }
  importing.value = true
  try {
    const res = await materialsAPI.import(parsedData.value)
    ElMessage.success(`导入完成: 新增 ${res.created} 条, 更新 ${res.updated} 条, 跳过 ${res.skipped} 条`)
    if (res.errors?.length) {
      console.warn('导入部分错误:', res.errors)
      ElMessage.warning(`${res.errors.length} 条导入失败`)
    }
    importDialogVisible.value = false
    fetchData()
  } catch (err) {
    console.error('导入失败:', err)
    ElMessage.error('导入失败: ' + (err.response?.data?.detail || err.message))
  } finally {
    importing.value = false
  }
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

/* 物料类型 (机械类/非机械类) — migration 016 */
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

/* 导入弹窗 */
.import-dialog {
  --stat-bg-created: #ecfdf5;
  --stat-bg-updated: #eff6ff;
  --stat-bg-skipped: #fef3c7;
  --stat-bg-total: #f5f3ff;
}

.import-upload-zone {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.upload-area {
  width: 100%;
  min-height: 180px;
  border: 2px dashed var(--color-border-light);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  padding: var(--spacing-xl);
  background: var(--color-bg-light);
}

.upload-area:hover {
  border-color: var(--color-primary);
  background: var(--color-primary-light);
}

.upload-icon {
  font-size: 48px;
  line-height: 1;
}

.upload-text p {
  margin: 0;
  text-align: center;
  font-size: 15px;
  color: var(--color-text-primary);
}

.upload-hint {
  font-size: 13px !important;
  color: var(--color-text-muted) !important;
  margin-top: var(--spacing-xs) !important;
}

/* 统计条 */
.import-stats {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.stat-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  gap: 4px;
}

.stat-num {
  font-size: 24px;
  font-weight: 700;
  line-height: 1;
}

.stat-label {
  font-size: 13px;
  color: var(--color-text-muted);
}

.stat-created { background: var(--stat-bg-created); }
.stat-created .stat-num { color: var(--color-success); }
.stat-updated { background: var(--stat-bg-updated); }
.stat-updated .stat-num { color: #2563eb; }
.stat-skipped { background: var(--stat-bg-skipped); }
.stat-skipped .stat-num { color: #d97706; }
.stat-total { background: var(--stat-bg-total); }
.stat-total .stat-num { color: #7c3aed; }

/* 预览表格标签 */
.cat-tag {
  display: inline-block;
  padding: 1px 8px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 500;
}
.cat-tag.large { background: #fef3c7; color: #d97706; }
.cat-tag.standard { background: var(--color-primary-light); color: var(--color-primary); }

/* 导入操作栏 */
.import-actions-bar {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  margin-top: var(--spacing-md);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--color-border-light);
}

.import-info {
  flex: 1;
  font-size: 13px;
  color: var(--color-text-muted);
  text-align: center;
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