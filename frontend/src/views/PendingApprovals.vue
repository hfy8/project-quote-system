<template>
  <div class="pending-approvals-page">
    <div class="page-header card">
      <div class="header-left">
        <span class="header-icon">📋</span>
        <h2 class="header-title">待审批归档申请</h2>
        <el-tag size="large" type="warning" effect="dark" class="count-tag">
          {{ pendingApprovals.length }} 个待审批
        </el-tag>
      </div>
      <div class="header-right">
        <el-button :icon="Refresh" @click="fetchPendingApprovals" :loading="loading">刷新</el-button>
      </div>
    </div>

    <!-- 待审批列表 -->
    <div v-if="!loading && pendingApprovals.length === 0" class="empty-state card">
      <div class="empty-icon">✅</div>
      <div class="empty-text">暂无待审批的归档申请</div>
      <div class="empty-hint">所有归档申请均已处理完毕</div>
    </div>

    <div v-else class="pending-grid">
      <div
        v-for="approval in pendingApprovals"
        :key="approval.id"
        class="pending-card card"
      >
        <div class="pending-card-header">
          <div class="pending-card-title">
            <b>{{ approval.quotation_name }}</b>
            <span class="pending-code">{{ approval.quotation_code }}</span>
          </div>
          <el-tag type="warning" size="small" effect="plain">待审批</el-tag>
        </div>

        <div class="pending-card-body">
          <div class="meta-row">
            <span class="meta-label">申请人</span>
            <span class="meta-value">{{ approval.requester_name || '-' }}</span>
          </div>
          <div class="meta-row">
            <span class="meta-label">申请时间</span>
            <span class="meta-value">{{ formatApprovalDate(approval.requested_at) }}</span>
          </div>
          <div v-if="approval.remark" class="meta-row">
            <span class="meta-label">备注</span>
            <span class="meta-value remark-text">{{ approval.remark }}</span>
          </div>
        </div>

        <div class="pending-card-footer">
          <el-button type="info" size="small" @click="handlePendingExportPDF(approval)">导出 PDF</el-button>
          <div class="right-actions">
            <el-button type="danger" size="small" plain @click="handleRejectArchivePrompt(approval)">驳回</el-button>
            <el-button type="success" size="small" @click="handleApproveArchive(approval)">同意</el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { quotationsAPI } from '../api/quotations'
import { parseUtcDate } from '../utils/date'

const pendingApprovals = ref([])
const loading = ref(false)
let pollTimer = null

const formatApprovalDate = (iso) => {
  if (!iso) return ''
  const d = parseUtcDate(iso)
  if (!d) return ''
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

const fetchPendingApprovals = async () => {
  loading.value = true
  try {
    const res = await quotationsAPI.listPendingArchiveApprovals()
    pendingApprovals.value = res?.items || []
  } catch (error) {
    pendingApprovals.value = []
  } finally {
    loading.value = false
  }
}

// 部门领导同意
const handleApproveArchive = async (approval) => {
  try {
    await ElMessageBox.confirm(
      `确定同意报价单「${approval.quotation_name}」的归档申请吗？同意后系统将自动创建版本快照并归档.`,
      '同意归档',
      {
        confirmButtonText: '同意',
        cancelButtonText: '取消',
        type: 'success'
      }
    )
    const res = await quotationsAPI.approveArchive(approval.quotation_id)
    ElMessage.success(res?.message || '已审批通过, 归档成功')
    await fetchPendingApprovals()
  } catch (error) {
    if (error !== 'cancel') {
      const msg = error?.response?.data?.error || error?.response?.data?.detail || error?.message || '操作失败'
      ElMessage.error(msg)
    }
  }
}

// 部门领导驳回 (弹窗输入原因)
const handleRejectArchivePrompt = async (approval) => {
  try {
    const { value: reason } = await ElMessageBox.prompt(
      `请填写驳回报价单「${approval.quotation_name}」归档的原因 (至少 5 个字). 驳回后报价单回到草稿状态.`,
      '驳回归档',
      {
        confirmButtonText: '驳回',
        cancelButtonText: '取消',
        inputPlaceholder: '例如: 报价单数据未完整, 请补充物料规格',
        inputValidator: (val) => (val && val.trim().length >= 5) || '至少 5 个字',
        inputErrorMessage: '至少 5 个字'
      }
    )
    await quotationsAPI.rejectArchive(approval.quotation_id, reason)
    ElMessage.success('已驳回, 报价单回到草稿状态')
    await fetchPendingApprovals()
  } catch (error) {
    if (error !== 'cancel' && error !== 'close') {
      const msg = error?.response?.data?.error || error?.response?.data?.detail || error?.message || '操作失败'
      ElMessage.error(msg)
    }
  }
}

// 审批人导出 PDF (待审批时也能看, 不需先进报价单详情)
const handlePendingExportPDF = async (approval) => {
  try {
    ElMessage.info(`正在生成「${approval.quotation_name}」PDF, 请稍候...`)
    const token = localStorage.getItem('token')
    const res = await fetch(`/api/quotations/${approval.quotation_id}/export/pdf`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (!res.ok) {
      const errJson = await res.json().catch(() => ({}))
      ElMessage.error(errJson.detail || errJson.error || `导出失败 (HTTP ${res.status})`)
      return
    }
    const disposition = res.headers.get('content-disposition') || ''
    const match = disposition.match(/filename="?([^"]+)"?/)
    const filename = match ? match[1] : `quotation_${approval.quotation_id}.pdf`
    const blob = await res.blob()
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    ElMessage.success('PDF 已下载')
  } catch (error) {
    ElMessage.error(error?.message || '导出失败')
  }
}

onMounted(() => {
  fetchPendingApprovals()
  // 30s 自动刷新, 让审批人看到新申请
  pollTimer = setInterval(fetchPendingApprovals, 30000)
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})
</script>

<style scoped>
.pending-approvals-page {
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  font-size: 24px;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: var(--color-text-primary);
}

.count-tag {
  font-size: 13px;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  font-size: 56px;
  margin-bottom: 16px;
  opacity: 0.6;
}

.empty-text {
  font-size: 16px;
  color: var(--color-text-primary);
  margin-bottom: 4px;
}

.empty-hint {
  font-size: 13px;
  color: var(--color-text-muted);
}

.pending-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 16px;
}

.pending-card {
  display: flex;
  flex-direction: column;
  border-left: 4px solid #e6a23c;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.pending-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

.pending-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px 12px;
  border-bottom: 1px dashed var(--color-border-light);
}

.pending-card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  color: var(--color-text-primary);
  min-width: 0;
}

.pending-card-title b {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 220px;
}

.pending-code {
  font-family: monospace;
  font-size: 12px;
  color: var(--color-text-muted);
  padding: 2px 6px;
  background: var(--color-bg-hover);
  border-radius: 4px;
}

.pending-card-body {
  padding: 12px 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.meta-row {
  display: flex;
  align-items: flex-start;
  font-size: 13px;
}

.meta-label {
  width: 70px;
  color: var(--color-text-secondary);
  flex-shrink: 0;
}

.meta-value {
  color: var(--color-text-primary);
  flex: 1;
}

.remark-text {
  font-style: italic;
  color: var(--color-text-secondary);
}

.pending-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  border-top: 1px solid var(--color-border-light);
  background: var(--color-bg-hover);
  border-radius: 0 0 8px 8px;
}

.right-actions {
  display: flex;
  gap: 8px;
}
</style>