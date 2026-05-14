<template>
  <div class="header">
    <div class="left">
      <span class="title">项目报价系统</span>
    </div>
    <div class="right">
      <!-- 消息铃铛 -->
      <div class="message-bell" @click="showMessageDialog">
        <i class="el-icon-bell"></i>
        <span v-if="unreadCount > 0" class="badge">{{ unreadCount > 99 ? '99+' : unreadCount }}</span>
      </div>
      
      <el-dropdown @command="handleCommand">
        <span class="user-info">
          <i class="el-icon-user"></i>
          <span>{{ username }}</span>
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="changePassword">修改密码</el-dropdown-item>
            <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>

    <!-- 消息通知弹窗 -->
    <el-dialog v-model="messageDialogVisible" title="消息通知" width="600px" :close-on-click-modal="false">
      <div class="message-list" v-if="messages.length > 0">
        <div
          v-for="msg in messages"
          :key="msg.id"
          class="message-item"
          :class="{ unread: !msg.is_read }"
          @click="handleMessageClick(msg)"
        >
          <div class="message-icon" :class="msg.type">
            <i :class="getMessageIcon(msg.type)"></i>
          </div>
          <div class="message-content">
            <div class="message-title">{{ msg.title }}</div>
            <div class="message-text">{{ msg.content }}</div>
            <div class="message-time">{{ formatTime(msg.created_at) }}</div>
          </div>
          <div v-if="!msg.is_read" class="unread-dot"></div>
        </div>
      </div>
      <div v-else class="empty-messages">
        <i class="el-icon-bell"></i>
        <span>暂无消息</span>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="markAllRead">全部已读</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 修改密码弹窗 -->
    <el-dialog v-model="changePasswordVisible" title="修改密码" width="400px" :close-on-click-modal="false">
      <el-form :model="changePasswordForm" label-width="90px">
        <el-form-item label="原密码">
          <el-input v-model="changePasswordForm.oldPassword" type="password" show-password placeholder="请输入原密码" />
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="changePasswordForm.newPassword" type="password" show-password placeholder="请输入新密码" />
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input v-model="changePasswordForm.confirmPassword" type="password" show-password placeholder="请再次输入新密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="changePasswordVisible = false">取消</el-button>
        <el-button type="primary" @click="handleChangePassword">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { ElMessageBox, ElMessage } from 'element-plus'
import messagesAPI from '../api/messages'

const router = useRouter()
const authStore = useAuthStore()

const username = computed(() => authStore.userInfo?.real_name || authStore.userInfo?.username || '管理员')

// 消息相关
const messageDialogVisible = ref(false)
const messages = ref([])
const unreadCount = ref(0)

let pollTimer = null

// 获取未读数量
const fetchUnreadCount = async () => {
  try {
    const res = await messagesAPI.getUnreadCount()
    unreadCount.value = res.unread_count || 0
  } catch (e) {
    console.error('获取未读数失败', e)
  }
}

// 获取消息列表
const fetchMessages = async () => {
  try {
    const res = await messagesAPI.getMessages({ page: 1, page_size: 20 })
    messages.value = res.items || []
  } catch (e) {
    console.error('获取消息失败', e)
  }
}

// 标记单条已读
const handleMessageClick = async (msg) => {
  if (!msg.is_read) {
    try {
      await messagesAPI.markAsRead(msg.id)
      msg.is_read = true
      unreadCount.value = Math.max(0, unreadCount.value - 1)
    } catch (e) {
      console.error('标记已读失败', e)
    }
  }
  
  // 跳转到相关页面
  if (msg.related_type === 'change_request') {
    messageDialogVisible.value = false
    router.push('/change-requests')
  } else if (msg.related_type === 'quotation') {
    messageDialogVisible.value = false
    router.push(`/quotations/${msg.related_id}`)
  }
}

// 全部已读
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

// 打开消息弹窗
const showMessageDialog = async () => {
  await fetchMessages()
  messageDialogVisible.value = true
}

// 跳转到消息页面
const goToMessages = () => {
  messageDialogVisible.value = false
  router.push('/messages')
}

// 消息图标
const getMessageIcon = (type) => {
  const iconMap = {
    'module_member_added': 'el-icon-user-plus',
    'change_request_submitted': 'el-icon-document-add',
    'change_request_approved': 'el-icon-check',
    'change_request_rejected': 'el-icon-close',
    'version_updated': 'el-icon-document'
  }
  return iconMap[type] || 'el-icon-bell'
}

// 格式化时间
const formatTime = (time) => {
  if (!time) return ''
  const d = new Date(time)
  const now = new Date()
  const diff = now - d
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return d.toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

const handleCommand = async (command) => {
  if (command === 'logout') {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await authStore.logout()
    router.push('/login')
  } else if (command === 'changePassword') {
    showChangePasswordDialog()
  }
}

// 修改密码
import { ref } from 'vue'
const changePasswordVisible = ref(false)
const changePasswordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const showChangePasswordDialog = () => {
  changePasswordForm.value = {
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  }
  changePasswordVisible.value = true
}

const handleChangePassword = async () => {
  if (changePasswordForm.value.newPassword !== changePasswordForm.value.confirmPassword) {
    ElMessage.error('两次输入的新密码不一致')
    return
  }
  if (changePasswordForm.value.newPassword.length < 6) {
    ElMessage.error('新密码长度不能少于6位')
    return
  }
  try {
    await authStore.changePassword({
      old_password: changePasswordForm.value.oldPassword,
      new_password: changePasswordForm.value.newPassword
    })
    ElMessage.success('密码修改成功')
    changePasswordVisible.value = false
  } catch (e) {
    ElMessage.error(e.message || '修改密码失败')
  }
}

// 定时轮询未读数
onMounted(() => {
  fetchUnreadCount()
  // 每30秒刷新一次未读数
  pollTimer = setInterval(fetchUnreadCount, 30000)
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})
</script>

<style scoped>
.header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.right {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* 消息铃铛 */
.message-bell {
  position: relative;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.message-bell:hover {
  background-color: #f5f7fa;
}

.message-bell i {
  font-size: 20px;
  color: #fff;
}

.message-bell .badge {
  position: absolute;
  top: 2px;
  right: 2px;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  background-color: #f56c6c;
  color: white;
  border-radius: 10px;
  font-size: 11px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  padding: 0 10px;
}

.user-info:hover {
  background-color: #f5f7fa;
}

/* 消息列表 */
.message-list {
  max-height: 400px;
  overflow-y: auto;
}

.message-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background-color 0.2s;
}

.message-item:hover {
  background-color: #f5f7fa;
}

.message-item.unread {
  background-color: #f0f9ff;
}

.message-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #e8f5e9;
  color: #0D9488;
  font-size: 16px;
}

.message-icon.change_request_submitted {
  background-color: #fff3e0;
  color: #ff9800;
}

.message-icon.change_request_rejected {
  background-color: #ffebee;
  color: #f44336;
}

.message-icon.module_member_added {
  background-color: #e3f2fd;
  color: #2196f3;
}

.message-content {
  flex: 1;
  min-width: 0;
}

.message-title {
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.message-text {
  font-size: 13px;
  color: #606266;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.message-time {
  font-size: 12px;
  color: #909399;
  margin-top: 6px;
}

.unread-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #f56c6c;
  flex-shrink: 0;
  margin-top: 4px;
}

.empty-messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  color: #909399;
}

.empty-messages i {
  font-size: 48px;
  margin-bottom: 12px;
}

.dialog-footer {
  display: flex;
  justify-content: space-between;
}
</style>