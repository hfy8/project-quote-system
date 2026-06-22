<template>
  <div class="app-layout">
    <!-- 侧边栏 - 清新浅色风格 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="header-left">
          <div class="logo">
            <div class="logo-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M9 17H7C5.89543 17 5 16.1046 5 15C5 13.8954 5.89543 13 7 13H9C10.1046 13 11 13.8954 11 15C11 16.1046 10.1046 17 9 17Z" fill="white"/>
                <path d="M15 7H17C18.1046 7 19 7.89543 19 9C19 10.1046 18.1046 11 17 11H15C13.8954 11 13 10.1046 13 9C13 7.89543 13.8954 7 15 7Z" fill="white"/>
                <path d="M7 11H9V13H7V11Z" fill="white"/>
                <path d="M15 13H17V15H15V13Z" fill="white"/>
                <path d="M12 3L4 7V17L12 21L20 17V7L12 3Z" stroke="white" stroke-width="2" fill="none"/>
              </svg>
            </div>
            <span class="logo-text">报价系统</span>
          </div>
        </div>
        <div class="header-right">
          <!-- 消息铃铛 -->
          <div class="message-bell" @click="showMessageDialog">
            <el-icon class="bell-icon"><Bell /></el-icon>
            <span v-if="unreadCount > 0" class="badge">{{ unreadCount > 99 ? '99+' : unreadCount }}</span>
          </div>
        </div>
      </div>

      <nav class="sidebar-nav">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ active: isActive(item.path) }"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-label">{{ item.label }}</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <div class="user-section">
          <div class="user-avatar">{{ userInitials }}</div>
          <div class="user-info-text">
            <span class="user-name">{{ username }}</span>
            <span class="user-role">{{ userRole }}</span>
          </div>
        </div>
        <div class="footer-actions">
          <button class="action-btn" @click="showChangePasswordDialog">
            <span>🔑</span> 修改密码
          </button>
          <button class="logout-btn" @click="handleLogout">
            <span>🚪</span> 退出登录
          </button>
        </div>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <router-view />
    </main>

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
          <el-button v-if="unreadCount > 0" @click="markAllRead">全部已读</el-button>
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
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { ElMessageBox, ElMessage } from 'element-plus'
import { Bell } from '@element-plus/icons-vue'
import messagesAPI from '../api/messages'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const username = computed(() => authStore.userInfo?.real_name || authStore.userInfo?.username || 'Admin')
const userRole = computed(() => authStore.userInfo?.role || 'viewer')
const userPermissions = computed(() => authStore.userInfo?.permissions || [])
const userInitials = computed(() => username.value.slice(0, 1).toUpperCase())

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
    
    // 登录后如果有未读消息，自动弹出通知
    if (unreadCount.value > 0 && localStorage.getItem('just_logged_in') === 'true') {
      localStorage.removeItem('just_logged_in')
      // 延迟一下确保页面已加载
      setTimeout(() => {
        showMessageDialog()
      }, 500)
    }
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
  // 点击查看全部时滚动到顶部查看更多消息
}

// 修改密码
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

// 权限检查函数 - 使用后端返回的权限列表
const hasPermission = (permission) => {
  const perms = userPermissions.value
  if (perms.includes('*')) return true
  if (perms.includes(permission)) return true
  // 通配符匹配
  const parts = permission.split('.')
  for (const p of perms) {
    if (p.endsWith('.*') && p.split('.')[0] === parts[0]) return true
  }
  return false
}

const menuItems = computed(() => {
  const items = [
    { path: '/dashboard', label: '首页', icon: '🏠', permission: 'dashboard.view' },
    { path: '/quotations', label: '报价单管理', icon: '📋', permission: 'quotation.view' },
    { path: '/trends', label: '报价趋势', icon: '📈', permission: 'quotation.view' },
    { path: '/my-assignments', label: '我的分配', icon: '📌', permission: 'module_assignment.view' },
    { path: '/change-requests', label: '变更审核', icon: '📤', permission: 'quotation.edit' },
    { path: '/materials', label: '原材料库', icon: '📦', permission: 'material.view' },
    { path: '/fee-types', label: '费用类型', icon: '💰', permission: 'fee_type.view' },
    { path: '/fee-rates', label: '费用系数', icon: '📊', permission: 'fee_rate.view' },
    { path: '/exchange-rates', label: '汇率配置', icon: '💱', permission: 'exchange_rate.view' },
    { path: '/users', label: '用户管理', icon: '👤', permission: 'user.view' },
    { path: '/roles', label: '角色管理', icon: '👥', permission: 'role.view' },
    { path: '/participant-type-permissions', label: '参与人权限', icon: '🔐', permission: 'role.view' },
    { path: '/travel-fee-config', label: '运输差旅配置', icon: '🚚', permission: 'fee_type.view' },
    { path: '/ai-chat', label: 'AI 助手', icon: '🤖', permission: 'ai.query' },
    { path: '/logs', label: '操作日志', icon: '📝', permission: 'log.view' }
  ]
  return items.filter(item => !item.permission || hasPermission(item.permission))
})

const isActive = (path) => {
  if (path === '/dashboard') return route.path === '/dashboard'
  return route.path.startsWith(path)
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    authStore.logout()
    router.push('/login')
  } catch {}
}

// 定时轮询未读数
onMounted(() => {
  fetchUnreadCount()
  pollTimer = setInterval(fetchUnreadCount, 30000)
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
  background: var(--color-bg-page);
  overflow: hidden;
  width: 100vw;
}

/* 侧边栏 - 清新浅色风格 */
.sidebar {
  width: 220px;
  background: #FFFFFF;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.06);
  border-right: 1px solid var(--color-border-light);
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid var(--color-border-light);
  background: linear-gradient(135deg, #0D9488 0%, #14B8A6 100%);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  color: white;
  letter-spacing: 0.5px;
}

/* 导航 */
.sidebar-nav {
  flex: 1;
  padding: 16px 12px;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 10px;
  color: var(--color-text-secondary);
  text-decoration: none;
  margin-bottom: 4px;
  transition: all 0.2s ease;
  font-weight: 500;
}

.nav-item:hover {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.nav-item.active {
  background: linear-gradient(135deg, #0D9488 0%, #14B8A6 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
}

.nav-item.active .nav-icon {
  filter: brightness(10);
}

.nav-icon {
  font-size: 18px;
  width: 24px;
  text-align: center;
}

.nav-label {
  font-size: 14px;
}

/* 用户信息 */
.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--color-border-light);
  background: var(--color-bg-page);
}

.user-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #0D9488 0%, #14B8A6 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(13, 148, 136, 0.3);
}

.user-info-text {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 12px;
  color: var(--color-text-secondary);
}

.footer-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.action-btn,
.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.action-btn {
  background: var(--color-bg-card);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border-light);
}

.action-btn:hover {
  background: var(--color-primary-light);
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.logout-btn {
  background: var(--color-bg-card);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border-light);
}

.logout-btn:hover {
  background: #FEE2E2;
  color: #EF4444;
  border-color: #FECACA;
}

/* 主内容区 */
.main-content {
  flex: 1;
  margin-left: 240px;
  height: 100vh;
  overflow: auto;
  display: flex;
  flex-direction: column;
}

/* 消息铃铛 */
.message-bell {
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: background-color 0.2s;
  color: #fff;
  position: relative;
}

.message-bell:hover {
  background: rgba(255, 255, 255, 0.2);
}

.bell-icon {
  color: #FFD700;
  font-size: 18px;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.2));
}

.message-bell .badge {
  position: absolute;
  top: 0;
  right: 0;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  background-color: #f56c6c;
  color: white;
  border-radius: 10px;
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
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
  flex-shrink: 0;
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
