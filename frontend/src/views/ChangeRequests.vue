<template>
  <div class="change-requests-container">
    <div class="page-header">
      <h2>变更申请审核</h2>
      <p class="subtitle">管理已归档报价单的物料变更申请</p>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-bar">
      <el-select v-model="filters.status" placeholder="状态" clearable style="width: 150px;">
        <el-option label="待审核" value="pending" />
        <el-option label="已批准" value="approved" />
        <el-option label="已拒绝" value="rejected" />
      </el-select>
      <el-button @click="fetchData">搜索</el-button>
    </div>

    <!-- 申请列表 -->
    <div style="flex:1;overflow:hidden;">
    <el-table :data="list" v-loading="loading" stripe height="calc(-200px + 100vh)">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="quotation_name" label="报价单" min-width="150" />
      <el-table-column prop="module_name" label="模块" min-width="120" />
      <el-table-column label="变更类型" min-width="100">
        <template #default="{ row }">
          <el-tag :type="getChangeTypeTag(row.change_type)">
            {{ getChangeTypeLabel(row.change_type) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="状态" min-width="80">
        <template #default="{ row }">
          <el-tag :type="row.status === 'pending' ? 'warning' : (row.status === 'approved' ? 'success' : 'danger')">
            {{ getStatusLabel(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="requester_name" label="申请人" min-width="100" />
      <el-table-column label="物料名称" width="200">
        <template #default="{ row }">
          {{ row.material_name || '-' }}
        </template>
      </el-table-column>
      <el-table-column label="品牌" min-width="100">
        <template #default="{ row }">
          {{ row.brand || '-' }}
        </template>
      </el-table-column>
      <el-table-column label="数量" min-width="70">
        <template #default="{ row }">
          {{ row.quantity || '-' }}
        </template>
      </el-table-column>
      <el-table-column label="申请时间" min-width="160">
        <template #default="{ row }">
          {{ formatTime(row.requested_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <template v-if="row.status === 'pending'">
            <el-button type="success" size="small" @click="handleApprove(row)">批准</el-button>
            <el-button type="danger" size="small" @click="handleReject(row)">拒绝</el-button>
          </template>
          <span v-else class="status-text">{{ getStatusLabel(row.status) }}</span>
        </template>
      </el-table-column>
    </el-table>
    </div>

    <!-- 分页 -->
    <div class="pagination-wrapper">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :total="pagination.total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        @size-change="fetchData"
        @current-change="fetchData"
      />
    </div>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="变更详情" width="600px">
      <div v-if="currentRequest" class="detail-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="报价单">{{ currentRequest.quotation_name }}</el-descriptions-item>
          <el-descriptions-item label="模块">{{ currentRequest.module_name }}</el-descriptions-item>
          <el-descriptions-item label="变更类型">
            <el-tag :type="getChangeTypeTag(currentRequest.change_type)">
              {{ getChangeTypeLabel(currentRequest.change_type) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="currentRequest.status === 'pending' ? 'warning' : (currentRequest.status === 'approved' ? 'success' : 'danger')">
              {{ getStatusLabel(currentRequest.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="申请人">{{ currentRequest.requester_name }}</el-descriptions-item>
          <el-descriptions-item label="申请时间">{{ formatTime(currentRequest.requested_at) }}</el-descriptions-item>
        </el-descriptions>

        <div class="change-data-section">
          <h4>变更内容</h4>
          <div v-if="currentRequest.change_type === 'material_add'" class="change-detail">
            <p><strong>操作：</strong>添加物料</p>
            <p><strong>物料ID：</strong>{{ currentRequest.proposed_data.material_id }}</p>
            <p><strong>数量：</strong>{{ currentRequest.proposed_data.quantity }}</p>
          </div>
          <div v-else-if="currentRequest.change_type === 'material_update'" class="change-detail">
            <p><strong>操作：</strong>更新物料数量</p>
            <p><strong>原数量：</strong>{{ currentRequest.original_data.quantity }}</p>
            <p><strong>新数量：</strong>{{ currentRequest.proposed_data.quantity }}</p>
          </div>
          <div v-else-if="currentRequest.change_type === 'material_delete'" class="change-detail">
            <p><strong>操作：</strong>删除物料</p>
            <p><strong>物料ID：</strong>{{ currentRequest.original_data.material_id }}</p>
            <p><strong>原数量：</strong>{{ currentRequest.original_data.quantity }}</p>
          </div>
        </div>

        <div v-if="currentRequest.status !== 'pending'" class="review-info">
          <h4>审核信息</h4>
          <p><strong>审核人：</strong>{{ currentRequest.reviewer_name || '-' }}</p>
          <p><strong>审核时间：</strong>{{ formatTime(currentRequest.reviewed_at) }}</p>
          <p><strong>审核备注：</strong>{{ currentRequest.review_remark || '-' }}</p>
        </div>
      </div>
    </el-dialog>

    <!-- 审核对话框 -->
    <el-dialog v-model="reviewDialogVisible" :title="reviewAction === 'approve' ? '批准变更申请' : '拒绝变更申请'" width="400px">
      <el-form>
        <el-form-item label="备注">
          <el-input v-model="reviewRemark" type="textarea" :rows="3" placeholder="请输入审核备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="reviewDialogVisible = false">取消</el-button>
        <el-button :type="reviewAction === 'approve' ? 'success' : 'danger'" @click="submitReview">
          {{ reviewAction === 'approve' ? '批准' : '拒绝' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { changeRequestsAPI } from '@/api/changeRequests'
import { parseUtcDate } from '../utils/date'

const loading = ref(false)
const list = ref([])
const filters = reactive({
  status: 'pending'
})
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

const detailDialogVisible = ref(false)
const reviewDialogVisible = ref(false)
const currentRequest = ref(null)
const reviewAction = ref('')
const reviewRemark = ref('')

const getChangeTypeLabel = (type) => {
  const map = {
    material_add: '添加物料',
    material_update: '更新物料',
    material_delete: '删除物料',
    module_update: '更新模块'
  }
  return map[type] || type
}

const getChangeTypeTag = (type) => {
  const map = {
    material_add: 'success',
    material_update: 'warning',
    material_delete: 'danger',
    module_update: 'info'
  }
  return map[type] || ''
}

const getStatusLabel = (status) => {
  const map = {
    pending: '待审核',
    approved: '已批准',
    rejected: '已拒绝'
  }
  return map[status] || status
}

const formatTime = (time) => {
  if (!time) return '-'
  const d = parseUtcDate(time)
  if (!d) return '-'
  return d.toLocaleString('zh-CN')
}

async function fetchData() {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.pageSize
    }
    if (filters.status) {
      params.status = filters.status
    }
    const data = await changeRequestsAPI.getList(params)
    list.value = data.items || data
    pagination.total = data.total || list.value.length
  } catch (error) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

function viewDetail(row) {
  currentRequest.value = row
  detailDialogVisible.value = true
}

function handleApprove(row) {
  currentRequest.value = row
  reviewAction.value = 'approve'
  reviewRemark.value = ''
  reviewDialogVisible.value = true
}

function handleReject(row) {
  currentRequest.value = row
  reviewAction.value = 'reject'
  reviewRemark.value = ''
  reviewDialogVisible.value = true
}

async function submitReview() {
  try {
    if (reviewAction.value === 'approve') {
      await changeRequestsAPI.approve(currentRequest.value.id, reviewRemark.value)
      ElMessage.success('已批准变更申请')
    } else {
      await changeRequestsAPI.reject(currentRequest.value.id, reviewRemark.value)
      ElMessage.success('已拒绝变更申请')
    }
    reviewDialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.change-requests-container {
  padding: var(--spacing-lg);
  height: 100vh;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.subtitle {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.pagination-wrapper {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.status-text {
  color: #909399;
  font-size: 12px;
}

.detail-content {
  padding: 12px 0;
}

.change-data-section,
.review-info {
  margin-top: 20px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 4px;
}

.change-data-section h4,
.review-info h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 600;
}

.change-detail p {
  margin: 8px 0;
  font-size: 14px;
}
</style>
