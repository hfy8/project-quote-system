<template>
  <div class="messages-page">
    <!-- 页面标题栏 -->
    <div class="page-header-bar">
      <div class="header-left">
        <h1 class="page-title">消息通知</h1>
        <span class="page-desc">查看您的所有消息通知</span>
      </div>
      <div class="header-right">
        <el-button v-if="unreadCount > 0" @click="markAllRead">全部已读</el-button>
      </div>
    </div>

    <!-- 消息筛选 -->
    <div class="filter-bar">
      <el-select v-model="filterRead" placeholder="消息状态" clearable style="width: 150px;" @change="fetchMessages">
        <el-option label="全部" value="" />
        <el-option label="未读" value="false" />
        <el-option label="已读" value="true" />
      </el-select>
    </div>

    <!-- 消息列表 -->
    <div class="content-card table-container">
      <el-table 
        :data="messages" 
        v-loading="loading"
        stripe
        class="messages-table"
        height="calc(-200px + 100vh)"
      >
        <el-table-column prop="type" label="类型" width="100">
          <template #default="{ row }">
            <div class="type-badge" :class="row.type">
              {{ getTypeLabel(row.type) }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="标题" min-width="180">
          <template #default="{ row }">
            <span class="message-title" :class="{ unread: !row.is_read }">{{ row.title }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="content" label="内容" min-width="300">
          <template #default="{ row }">
            <span class="message-content">{{ row.content }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="时间" width="160">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button v-if="!row.is_read" size="small" @click="handleMarkRead(row)">标记已读</el-button>
            <span v-else class="read-text">已读</span>
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
        @size-change="fetchMessages"
        @current-change="fetchMessages"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import messagesAPI from '../api/messages'

const router = useRouter()

const loading = ref(false)
const messages = ref([])
const unreadCount = ref(0)
const filterRead = ref('')
const pagination = ref({
  page: 1,
  pageSize: 20,
  total: 0
})

const fetchMessages = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.pageSize
    }
    if (filterRead.value !== '') {
      params.is_read = filterRead.value
    }
    const res = await messagesAPI.getMessages(params)
    messages.value = res.items || []
    pagination.value.total = res.total || 0
  } catch (e) {
    console.error('获取消息失败', e)
  } finally {
    loading.value = false
  }
}

const fetchUnreadCount = async () => {
  try {
    const res = await messagesAPI.getUnreadCount()
    unreadCount.value = res.unread_count || 0
  } catch (e) {
    console.error('获取未读数失败', e)
  }
}

const handleMarkRead = async (msg) => {
  try {
    await messagesAPI.markAsRead(msg.id)
    msg.is_read = true
    unreadCount.value = Math.max(0, unreadCount.value - 1)
  } catch (e) {
    console.error('标记已读失败', e)
  }
}

const markAllRead = async () => {
  try {
    await messagesAPI.markAllAsRead()
    messages.value.forEach(m => m.is_read = true)
    unreadCount.value = 0
    ElMessage.success('已全部标记为已读')
  } catch (e) {
    console.error('标记全部已读失败', e)
  }
}

const getTypeLabel = (type) => {
  const labelMap = {
    'module_member_added': '成员加入',
    'change_request_submitted': '变更申请',
    'change_request_approved': '申请通过',
    'change_request_rejected': '申请拒绝',
    'version_updated': '版本更新'
  }
  return labelMap[type] || type
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchMessages()
  fetchUnreadCount()
})
</script>

<style scoped>
.messages-page {
  padding: var(--spacing-lg);
  height: 100vh;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.page-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.header-left {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.page-desc {
  font-size: 14px;
  color: var(--color-text-secondary);
}

.header-right {
  display: flex;
  gap: 8px;
}

.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

/* 内容卡片 */
.content-card {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  overflow: hidden;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.table-container {
  flex: 1;
  overflow: hidden;
}

.table-container :deep(.el-table) {
  max-height: 100%;
}

.table-container :deep(.el-table__body-wrapper) {
  overflow-y: auto;
}

.type-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  background-color: #e8f5e9;
  color: #0D9488;
}

.type-badge.change_request_submitted {
  background-color: #fff3e0;
  color: #ff9800;
}

.type-badge.change_request_rejected {
  background-color: #ffebee;
  color: #f44336;
}

.type-badge.module_member_added {
  background-color: #e3f2fd;
  color: #2196f3;
}

.type-badge.version_updated {
  background-color: #f3e8ff;
  color: #9333ea;
}

.message-title {
  font-weight: 500;
  color: var(--color-text-primary);
}

.message-title.unread {
  font-weight: 600;
}

.message-content {
  color: var(--color-text-secondary);
  font-size: 13px;
}

.read-text {
  color: #909399;
  font-size: 13px;
}

.pagination-wrapper {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>