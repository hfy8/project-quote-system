<template>
  <div class="messages-page">
    <div class="page-header">
      <div class="header-left">
        <h2 class="page-title">📬 我的消息</h2>
        <span class="page-sub">{{ pagination.total }} 条消息 · {{ unreadCount }} 条未读</span>
      </div>
      <div class="header-right">
        <el-radio-group v-model="filterRead" size="default" @change="loadMessages">
          <el-radio-button label="all">全部</el-radio-button>
          <el-radio-button label="unread">未读</el-radio-button>
          <el-radio-button label="read">已读</el-radio-button>
        </el-radio-group>
        <el-button
          type="primary"
          :disabled="unreadCount === 0"
          @click="handleMarkAllRead"
        >
          <el-icon><CircleCheck /></el-icon>
          全部标为已读
        </el-button>
      </div>
    </div>

    <div class="messages-list" v-loading="loading">
      <div v-if="messages.length === 0 && !loading" class="empty-state">
        <div class="empty-icon">📭</div>
        <p class="empty-text">{{ filterRead === 'unread' ? '没有未读消息' : '暂无消息' }}</p>
      </div>

      <div
        v-for="msg in messages"
        :key="msg.id"
        class="message-item"
        :class="{ 'is-unread': !msg.is_read }"
        @click="handleClickMessage(msg)"
      >
        <div class="msg-icon" :class="iconClass(msg.message_type)">
          <span>{{ iconEmoji(msg.message_type) }}</span>
          <span v-if="!msg.is_read" class="unread-dot"></span>
        </div>
        <div class="msg-body">
          <div class="msg-header">
            <span class="msg-title">{{ msg.title || defaultTitle(msg.message_type) }}</span>
            <span class="msg-time">{{ formatTime(msg.created_at) }}</span>
          </div>
          <div class="msg-content">{{ msg.content }}</div>
          <div v-if="msg.sender_name" class="msg-sender">来自: {{ msg.sender_name }}</div>
        </div>
        <div class="msg-actions">
          <el-button
            v-if="!msg.is_read"
            size="small"
            type="primary"
            text
            @click.stop="handleMarkRead(msg)"
          >
            标为已读
          </el-button>
          <el-icon v-else class="read-icon"><Check /></el-icon>
        </div>
      </div>
    </div>

    <div v-if="pagination.total > pagination.pageSize" class="pagination">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :total="pagination.total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="loadMessages"
        @size-change="loadMessages"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Check, CircleCheck } from '@element-plus/icons-vue'
import messagesAPI from '@/api/messages'
import { formatRelativeTime } from '@/utils/date'

const router = useRouter()

const loading = ref(false)
const messages = ref([])
const filterRead = ref('all')
const unreadCount = ref(0)

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

const defaultTitle = (type) => {
  const map = {
    system: '系统通知',
    archive_approval: '归档审批',
    change_request: '变更审核',
    quotation: '报价单通知',
  }
  return map[type] || '消息通知'
}

const iconEmoji = (type) => {
  const map = {
    system: '🔔',
    archive_approval: '📦',
    change_request: '📝',
    quotation: '📋',
  }
  return map[type] || '💬'
}

const iconClass = (type) => `msg-icon-${type || 'system'}`

const formatTime = formatRelativeTime

const loadMessages = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      pageSize: pagination.pageSize,
    }
    if (filterRead.value !== 'all') {
      params.is_read = filterRead.value === 'read' ? 'true' : 'false'
    }
    const res = await messagesAPI.getMessages(params)
    messages.value = res.items || []
    pagination.total = res.total || 0
    await loadUnreadCount()
  } catch (e) {
    console.error('加载消息失败', e)
    ElMessage.error('加载消息失败: ' + (e.message || ''))
  } finally {
    loading.value = false
  }
}

const loadUnreadCount = async () => {
  try {
    const res = await messagesAPI.getUnreadCount()
    unreadCount.value = res.count || 0
  } catch (e) {
    console.error('加载未读数失败', e)
  }
}

const handleMarkRead = async (msg) => {
  try {
    await messagesAPI.markRead(msg.id)
    msg.is_read = true
    ElMessage.success('已标记为已读')
    await loadUnreadCount()
  } catch (e) {
    ElMessage.error('操作失败: ' + (e.message || ''))
  }
}

const handleMarkAllRead = async () => {
  try {
    await ElMessageBox.confirm(`确认将全部 ${unreadCount.value} 条消息标记为已读?`, '批量操作', {
      confirmButtonText: '全部已读',
      cancelButtonText: '取消',
      type: 'info',
    })
    await messagesAPI.markAllRead()
    ElMessage.success('已全部标记为已读')
    await loadMessages()
  } catch (e) {
    if (e !== 'cancel' && e?.message) {
      ElMessage.error('操作失败: ' + e.message)
    }
  }
}

const handleClickMessage = async (msg) => {
  if (!msg.is_read) {
    try {
      await messagesAPI.markRead(msg.id)
      msg.is_read = true
      await loadUnreadCount()
    } catch (e) {
      console.error('自动标记已读失败', e)
    }
  }
  // 跳转到相关页面 (如果有 link_url)
  if (msg.link_url) {
    router.push(msg.link_url)
  } else if (msg.quotation_id) {
    router.push(`/quotations/${msg.quotation_id}`)
  }
}

onMounted(() => {
  loadMessages()
})
</script>

<style scoped>
.messages-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 16px;
  gap: 12px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 14px 20px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.header-left {
  display: flex;
  align-items: baseline;
  gap: 14px;
}

.page-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary, #303133);
}

.page-sub {
  font-size: 13px;
  color: var(--color-text-secondary, #909399);
}

.header-right {
  display: flex;
  gap: 12px;
  align-items: center;
}

.messages-list {
  flex: 1;
  background: white;
  border-radius: 8px;
  padding: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
  overflow-y: auto;
  min-height: 0;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  color: var(--color-text-secondary, #909399);
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}

.empty-text {
  margin: 0;
  font-size: 14px;
}

.message-item {
  display: flex;
  gap: 14px;
  padding: 14px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
  border-bottom: 1px solid #f0f0f0;
}

.message-item:last-child {
  border-bottom: none;
}

.message-item:hover {
  background: #f8fafc;
}

.message-item.is-unread {
  background: #f0f7ff;
}

.message-item.is-unread:hover {
  background: #e6f0fd;
}

.msg-icon {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.msg-icon-system { background: #f0f9ff; }
.msg-icon-archive_approval { background: #fef3c7; }
.msg-icon-change_request { background: #ede9fe; }
.msg-icon-quotation { background: #dcfce7; }

.unread-dot {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ef4444;
  border: 2px solid white;
}

.msg-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.msg-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.msg-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary, #303133);
}

.is-unread .msg-title {
  color: #1e40af;
}

.msg-time {
  font-size: 12px;
  color: var(--color-text-secondary, #909399);
}

.msg-content {
  font-size: 13px;
  color: #4b5563;
  line-height: 1.5;
  word-break: break-word;
}

.msg-sender {
  font-size: 12px;
  color: var(--color-text-secondary, #909399);
}

.msg-actions {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.read-icon {
  color: #10b981;
  font-size: 18px;
}

.pagination {
  display: flex;
  justify-content: center;
  background: white;
  padding: 12px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}
</style>