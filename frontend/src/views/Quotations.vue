<template>
  <div class="quotations-page">
    <!-- 页面标题栏 -->
    <div class="page-header-bar">
      <div class="header-left">
        <h1 class="page-title">报价单管理</h1>
        <span class="page-desc">共 {{ pagination.total }} 个报价单</span>
      </div>
      <button class="btn btn-primary" :disabled="!canCreate" @click="$router.push('/quotations/new')">
        <span>+</span> 新建报价单
      </button>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-bar card">
      <div class="filter-group">
        <el-select v-model="filters.status" placeholder="状态" clearable @change="fetchData">
          <el-option label="全部状态" value="" />
          <el-option label="草稿" value="draft" />
          <el-option label="审批中" value="approved_pending" />
          <el-option label="已归档" value="approved" />
        </el-select>
        <el-select v-model="filters.type" placeholder="类型" clearable @change="fetchData">
          <el-option label="全部类型" value="" />
          <el-option label="单项" value="single" />
          <el-option label="线体" value="line" />
        </el-select>
        <el-input
          v-model="filters.keyword"
          placeholder="搜索项目名称..."
          clearable
          class="search-input"
          @keyup.enter="fetchData"
        >
          <template #prefix>
            <span>🔍</span>
          </template>
        </el-input>
      </div>
      <button class="btn btn-secondary" @click="fetchData">搜索</button>
    </div>

    <!-- 数据表格 -->
    <div class="table-container card" style="flex:1;overflow:hidden;display:flex;flex-direction:column;">
      <el-table
        :data="tableData"
        v-loading="loading"
        stripe
        class="quotations-table"
        style="flex:1;width:100%;"
        row-key="id"
        :tree-props="{ children: '_children' }"
        default-expand-all
        max-height="calc(-200px + 100vh)"
      >
        <el-table-column prop="name" label="项目名称" width="200" show-overflow-tooltip />
        <el-table-column label="" width="90" align="center">
          <template #default="{ row }">
            <span v-if="row._children && row._children.length" class="child-count-tag">
              {{ row._children.length }}个子项
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="scheme_no" label="方案号" width="130" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <span class="type-tag" :class="row.type">
              {{ formatType(row.type) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <span class="status-badge" :class="row.status">
              <span class="status-dot"></span>
              {{ formatStatus(row.status) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="项目落地" width="120" align="center">
          <template #default="{ row }">
            <el-tooltip v-if="row.has_project" :content="`方案号 ${row.scheme_no} 已在项目管理系统落地, 不可撤销归档`" placement="top">
              <span class="project-badge landed">
                <span class="project-dot"></span>
                已落地
              </span>
            </el-tooltip>
            <span v-else class="project-badge not-landed">未落地</span>
          </template>
        </el-table-column>
        <el-table-column prop="creator_name" label="创建人" min-width="150" />
        <el-table-column prop="business_owner_name" label="负责人" min-width="150" />
        <el-table-column prop="created_at" label="创建时间" min-width="150">
          <template #default="{ row }">
            <span class="date-text">{{ formatDate(row.created_at) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="320" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <button v-if="row.type === 'line'" class="action-btn add-child" @click="handleAddChild(row)">+子项</button>
              <button v-if="row.status === 'draft' && !row.parent_id" class="action-btn archive" @click="handleArchive(row)">归档</button>
              <button v-if="row.status === 'approved_pending' && !row.parent_id && row.business_owner_id === currentUserId" class="action-btn cancel" @click="handleCancelArchive(row)">撤回申请</button>
              <button v-if="row.status === 'approved' && !row.parent_id" class="action-btn unarchive" :disabled="row.has_project" :title="row.has_project ? '该报价单已在项目管理系统落地, 不可撤销归档' : '撤销归档'" @click="handleUnarchive(row)">撤销归档</button>
              <button v-if="row.status === 'approved'" class="action-btn version" @click="handleViewVersions(row)">版本</button>
              <button class="action-btn edit" :disabled="!canEdit(row)" @click="handleEdit(row)">编辑</button>
              <button class="action-btn delete" :disabled="!canDelete(row)" @click="handleDelete(row)">删除</button>
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

    <!-- 版本历史对话框 -->
    <el-dialog v-model="versionDialogVisible" title="版本历史" width="900px">
      <div class="version-dialog-toolbar">
        <el-button type="primary" @click="openVersionCompare" :disabled="versions.length < 2">
          🔍 版本对比
        </el-button>
        <span v-if="versions.length < 2" class="toolbar-hint">至少需要2个版本才能对比</span>
      </div>
      <el-table :data="versions" stripe v-if="versions.length > 0" max-height="350">
        <el-table-column prop="version_no" label="版本号" width="100" align="center">
          <template #default="{ row }">
            <span class="version-tag">v{{ row.version_no }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="operation_type" label="操作" width="100">
          <template #default="{ row }">
            {{ row.operation_type === 'archive' ? '归档' : row.operation_type }}
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" min-width="150" show-overflow-tooltip />
        <el-table-column prop="created_at" label="时间" width="150">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleViewVersionDetail(row)">查看</el-button>
            <el-dropdown trigger="click" @command="(cmd) => handleExportVersion(row, cmd)">
              <el-button type="warning" size="small">导出PDF ▾</el-button>
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
      <el-empty v-else description="暂无版本记录" />
    </el-dialog>

    <!-- 版本详情对话框 -->
    <el-dialog v-model="versionDetailDialogVisible" title="版本详情" width="800px">
      <div v-if="selectedVersion" class="version-detail">
        <p><strong>版本号：</strong>v{{ selectedVersion.version_no }}</p>
        <p><strong>操作类型：</strong>{{ selectedVersion.operation_type === 'archive' ? '归档' : selectedVersion.operation_type }}</p>
        <p><strong>备注：</strong>{{ selectedVersion.remark || '-' }}</p>
        <p><strong>创建时间：</strong>{{ formatDate(selectedVersion.created_at) }}</p>
        <el-divider />
        <h4>快照数据</h4>
        <pre class="snapshot-data">{{ JSON.stringify(selectedVersion.snapshot_data, null, 2) }}</pre>
      </div>
    </el-dialog>

    <!-- 版本对比弹窗 -->
    <el-dialog v-model="versionCompareVisible" title="版本对比" width="95%" fullscreen destroy-on-close>
      <VersionCompare
        :versions="versions"
        :quotation-id="currentQuotationId"
      />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { hasPermission } from '../router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { quotationsAPI } from '../api/quotations'
import { openDownload } from '../utils/download'
import { parseUtcDate } from '../utils/date'
import { useAuthStore } from '../stores/auth'
import { usePermission } from '../composables/usePermission'
import VersionCompare from './VersionCompare.vue'

const router = useRouter()
const authStore = useAuthStore()

// 当前用户 ID (computed 跟随 authStore.userInfo 变化)
const currentUserId = computed(() => authStore.userInfo?.id)

// 是否有创建报价单权限
const canCreate = computed(() => {
  return hasPermission('quotation.create')
})

// 是否有编辑报价单权限
const canEdit = (row) => {
  // 已归档或审批中的报价单不能编辑（但可以导出报表）
  if (row.status === 'approved') return false
  if (row.status === 'approved_pending' && authStore.userInfo?.role !== 'admin') return false
  const userId = authStore.userInfo?.id
  if (authStore.userInfo?.role === 'admin' || hasPermission('quotation.edit')) {
    if (authStore.userInfo?.role === 'admin') return true
    return row.business_owner_id === userId  // 看负责人，不是创建人
  }
  return false
}

// 编辑报价单（检查归档状态）
const handleEdit = (row) => {
  if (row.status === 'approved') {
    ElMessage.warning('已归档的报价单无法编辑，如需修改请先撤销归档')
    return
  }
  if (row.status === 'approved_pending' && authStore.userInfo?.role !== 'admin') {
    ElMessage.warning('报价单正在审批中, 不能修改. 如需修改请先撤回审批申请')
    return
  }
  router.push(`/quotations/${row.id}`)
}

// 添加子报价单
const handleAddChild = (row) => {
  if (row.child_count >= 99) {
    ElMessage.warning('子报价单数量已达上限（99个）')
    return
  }
  router.push(`/quotations/new?parent_id=${row.id}`)
}

// 是否有删除报价单权限
const canDelete = (row) => {
  // 已归档或审批中的报价单不能删除
  if (row.status === 'approved') return false
  if (row.status === 'approved_pending' && authStore.userInfo?.role !== 'admin') return false
  if (authStore.userInfo?.role === 'admin' || hasPermission('quotation.delete')) {
    if (authStore.userInfo?.role === 'admin') return true
    return row.business_owner_id === authStore.userInfo?.id  // 看负责人
  }
  return false
}

const loading = ref(false)
const tableData = ref([])

const formatApprovalDate = (iso) => {
  if (!iso) return ''
  const d = parseUtcDate(iso)
  if (!d) return ''
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

// 待审批相关函数 (handleApproveArchive / handleRejectArchivePrompt / handlePendingExportPDF) 已迁至 views/PendingApprovals.vue

const filters = reactive({
  status: '',
  type: '',
  keyword: ''
})

// 版本历史相关
const versionDialogVisible = ref(false)
const versionDetailDialogVisible = ref(false)
const versionCompareVisible = ref(false)
const versions = ref([])
const selectedVersion = ref(null)
const currentQuotationId = ref(null)

// 打开版本对比
const openVersionCompare = () => {
  if (!currentQuotationId.value) {
    ElMessage.warning('请先选择一个报价单')
    return
  }
  versionCompareVisible.value = true
}

// 分页
const pagination = reactive({ page: 1, pageSize: 20, total: 0 })

const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize,
    }
    if (filters.status) params.status = filters.status
    if (filters.type) params.type = filters.type
    if (filters.keyword) params.keyword = filters.keyword

    const res = await quotationsAPI.getList(params)
    const items = res.items || res || []

    // 后端已分页+内联子报价单 _children
    tableData.value = items
    pagination.total = res.total || items.length
  } catch (error) {
    console.error('Failed to fetch quotations:', error)
    ElMessage.error('获取报价单列表失败')
  } finally {
    loading.value = false
  }
}

const formatType = (type) => {
  const types = { single: '单项', line: '线体' }
  return types[type] || type
}

const formatStatus = (status) => {
  const statuses = {
    draft: '草稿',
    submitted: '待审核',
    approved: '已审批',
    archived: '已归档',
    cancelled: '已取消',
    rejected: '已驳回',
    approved_pending: '审批中',
  }
  return statuses[status] || status
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = parseUtcDate(dateStr)
  if (!date) return '-'
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric' })
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

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除报价单「${row.name}」吗？删除后无法恢复。`,
      '确认删除',
      {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await quotationsAPI.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleArchive = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要归档报价单「${row.name}」吗？归档后将创建版本快照。`,
      '归档报价单',
      {
        confirmButtonText: '归档',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    const res = await quotationsAPI.archive(row.id)
    // 后端可能返回两种结果:
    //   { message: '归档成功', quotation, version }       → admin 直接归档
    //   { message: '归档申请已提交, 等待部门领导审批', approval_id, approver, status: 'pending' } → 走审批流
    if (res.status === 'pending' && res.approver) {
      ElMessageBox.alert(
        `您的归档申请已提交, 等待 <b>${res.approver.real_name || res.approver.username}</b> 审批. 审批通过后将自动归档.`,
        '已提交审批',
        {
          dangerouslyUseHTMLString: true,
          confirmButtonText: '我知道了'
        }
      )
    } else {
      ElMessage.success('归档成功')
    }
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      const msg = error?.response?.data?.detail || error?.message || '归档失败'
      ElMessage.error(msg)
    }
  }
}

const handleCancelArchive = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要撤回报价单「${row.name}」的归档申请吗？撤回后状态回到草稿, 您可以修改后重新提交.`,
      '撤回归档申请',
      {
        confirmButtonText: '撤回',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    const res = await quotationsAPI.cancelArchive(row.id)
    ElMessage.success(res?.message || '已撤回')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      const msg = error?.response?.data?.detail || error?.message || '撤回失败'
      ElMessage.error(msg)
    }
  }
}

const handleUnarchive = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要撤销归档「${row.name}」吗？撤销后可以重新编辑。`,
      '撤销归档',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await quotationsAPI.unarchive(row.id)
    ElMessage.success('撤销归档成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      // 后端返回的 detail 优先展示 (如"已落地项目")
      const msg = error?.response?.data?.detail || error?.message || '撤销归档失败'
      ElMessage.error(msg)
    }
  }
}

const handleViewVersions = async (row) => {
  currentQuotationId.value = row.id
  try {
    const res = await quotationsAPI.getVersions(row.id)
    versions.value = res || []
    versionDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取版本历史失败')
  }
}

const handleViewVersionDetail = async (row) => {
  try {
    const res = await quotationsAPI.getVersionDetail(currentQuotationId.value, row.version_no)
    selectedVersion.value = res
    versionDetailDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取版本详情失败')
  }
}

// 导出版本报价单
const handleExportVersion = (row, cmd) => {
  const [fmt, lang] = cmd.split('_')
  openDownload(`/api/quotations/${currentQuotationId.value}/versions/${row.version_no}/export/${fmt}?lang=${lang}`)
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.quotations-page {
  padding: var(--spacing-lg);
  height: 100vh;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 页面标题栏 */
.page-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
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

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.btn-primary span {
  font-size: 16px;
}

.btn-secondary {
  background: var(--color-bg-card);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

.btn-secondary:hover {
  background: var(--color-bg-hover);
}

/* 筛选栏 */
.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  margin-bottom: var(--spacing-md);
}

/* 待审批栏相关 CSS 已迁至 views/PendingApprovals.vue */

.filter-group {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

.filter-bar :deep(.el-select) {
  width: 140px;
}

.filter-bar :deep(.el-select .el-input__wrapper) {
  border-radius: var(--radius-md);
}

.search-input {
  width: 240px;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: var(--radius-md);
}

/* 表格容器 */
.table-container {
  overflow: hidden;
}

.quotations-table {
  --el-table-border-color: var(--color-border-light);
}

/* 子项数量标签 */
.child-count-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  background: var(--color-bg-page);
  color: var(--color-text-secondary);
  border-radius: 10px;
  font-size: 12px;
}

/* 子报价单行样式（树形子节点） */
::v-deep(.el-table__row--level-1) {
  background-color: var(--color-bg-page) !important;
}

::v-deep(.el-table__row--level-1:hover > td) {
  background-color: #F3F4F6 !important;
}

.no-scheme {
  color: var(--color-text-muted);
}

/* 类型标签 */
.type-tag {
  display: inline-block;
  padding: 2px 10px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 500;
}

.type-tag.single {
  background: var(--color-info-bg);
  color: var(--color-info);
}

.type-tag.line {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

/* 状态徽章 */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 500;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-badge.draft {
  background: var(--color-info-bg);
  color: var(--color-info);
}

.status-badge.draft .status-dot {
  background: var(--color-info);
}

.status-badge.submitted {
  background: var(--color-warning-bg);
  color: var(--color-warning);
}

.status-badge.submitted .status-dot {
  background: var(--color-warning);
}

.status-badge.approved {
  background: var(--color-success-bg);
  color: var(--color-success);
}

.status-badge.approved .status-dot {
  background: var(--color-success);
}

.status-badge.rejected {
  background: var(--color-danger-bg);
  color: var(--color-danger);
}

.status-badge.rejected .status-dot {
  background: var(--color-danger);
}

/* 项目落地状态徽章 */
.project-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
}

.project-badge.landed {
  background: #FEF3C7;
  color: #92400E;
}

.project-badge.landed .project-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #D97706;
  box-shadow: 0 0 0 2px rgba(217, 119, 6, 0.2);
}

.project-badge.not-landed {
  background: #F3F4F6;
  color: #6B7280;
  font-weight: 400;
}

.creator-name,
.date-text {
  font-size: 13px;
  color: var(--color-text-secondary);
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

.action-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.action-btn.delete:hover {
  background: var(--color-danger);
  color: white;
}

/* 添加子项按钮样式 */
.action-btn.add-child {
  background: #D1FAE5;
  color: #059669;
  border: none;
  padding: 4px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
}

.action-btn.add-child:hover {
  background: #A7F3D0;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  padding: var(--spacing-md) var(--spacing-lg);
  border-top: 1px solid var(--color-border-light);
}

.pagination-wrapper :deep(.el-pagination) {
  font-weight: 500;
}

/* 归档按钮样式 */
.action-btn.archive {
  background: #FEF3C7;
  color: #D97706;
  border: none;
  padding: 4px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
}

.action-btn.archive:hover {
  background: #FDE68A;
}

/* 撤回归档申请按钮样式 */
.action-btn.cancel {
  background: #FEE2E2;
  color: #DC2626;
  border: none;
  padding: 4px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
}

.action-btn.cancel:hover {
  background: #FECACA;
}

/* 审批中状态徽章 */
.status-badge.approved_pending {
  background: #FEF3C7;
  color: #D97706;
  font-weight: 500;
}

.status-badge.approved_pending .status-dot {
  background: #D97706;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* 撤销归档按钮样式 */
.action-btn.unarchive {
  background: #DBEAFE;
  color: #2563EB;
  border: none;
  padding: 4px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
}

.action-btn.unarchive:hover {
  background: #BFDBFE;
}

/* 版本按钮样式 */
.action-btn.version {
  background: #E0E7FF;
  color: #4F46E5;
  border: none;
  padding: 4px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
}

.action-btn.version:hover {
  background: #C7D2FE;
}

/* 版本标签 */
.version-tag {
  display: inline-block;
  padding: 2px 8px;
  background: #E0E7FF;
  color: #4F46E5;
  border-radius: 4px;
  font-weight: 600;
  font-size: 12px;
}

/* 版本详情 */
.version-detail {
  font-size: 14px;
  line-height: 1.8;
}

.version-detail h4 {
  margin: 16px 0 8px;
  font-size: 14px;
  color: var(--color-text-primary);
}

.snapshot-data {
  background: #F9FAFB;
  padding: 16px;
  border-radius: 8px;
  font-size: 12px;
  overflow-x: auto;
  max-height: 400px;
  white-space: pre-wrap;
  word-break: break-all;
}

/* 版本对话框工具栏 */
.version-dialog-toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--color-border-light);
}

.toolbar-hint {
  font-size: 13px;
  color: #909399;
}
</style>
