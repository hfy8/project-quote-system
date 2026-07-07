<template>
  <div class="logs-page">
    <!-- 页面标题栏 -->
    <div class="page-header-bar">
      <div class="header-left">
        <h1 class="page-title">操作日志</h1>
        <span class="page-desc">查看用户操作记录</span>
      </div>
      <div class="header-right">
        <button class="btn btn-secondary" @click="fetchData">
          🔄 刷新
        </button>
      </div>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-bar">
      <div class="filter-item">
        <select v-model="filters.action" class="filter-select">
          <option value="">全部操作</option>
          <option value="create">创建</option>
          <option value="update">更新</option>
          <option value="delete">删除</option>
          <option value="login">登录</option>
          <option value="export">导出</option>
        </select>
      </div>
      <div class="filter-item">
        <select v-model="filters.user" class="filter-select">
          <option value="">全部用户</option>
          <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
        </select>
      </div>
      <div class="filter-item search-box">
        <span class="search-icon">🔍</span>
        <input 
          v-model="filters.keyword" 
          type="text" 
          class="search-input" 
          placeholder="搜索操作内容..."
          @keyup.enter="fetchData"
        />
      </div>
      <button class="btn btn-primary" @click="fetchData">搜索</button>
    </div>

    <!-- 日志列表 -->
    <div class="content-card table-container">
      <el-table 
        :data="tableData" 
        :loading="loading"
        stripe
        class="log-table"
        height="calc(-200px + 100vh)"
      >
        <el-table-column prop="created_at" label="时间" width="180">
          <template #default="{ row }">
            <div class="time-cell">
              <span class="date">{{ formatDate(row.created_at) }}</span>
              <span class="time">{{ formatTime(row.created_at) }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户" width="120">
          <template #default="{ row }">
            <div class="user-cell">
              <span class="user-avatar">{{ (row.username || 'S').slice(0, 1).toUpperCase() }}</span>
              <span class="username">{{ row.username }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="action" label="操作类型" width="100">
          <template #default="{ row }">
            <span class="action-badge" :class="row.action">{{ getActionText(row.action) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="module" label="模块" width="100">
          <template #default="{ row }">
            {{ getModuleText(row.module) }}
          </template>
        </el-table-column>
        <el-table-column prop="detail" label="操作内容" min-width="300">
          <template #default="{ row }">
            <span class="description">{{ row.detail || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="ip_address" label="IP地址" width="130">
          <template #default="{ row }">
            <span class="ip-address">{{ row.ip_address || '-' }}</span>
          </template>
        </el-table-column>
        <template #empty>
          <div class="empty-state">
            <span class="empty-icon">📝</span>
            <p>暂无操作记录</p>
          </div>
        </template>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper" v-if="total > 0">
        <span class="total-count">共 {{ total }} 条记录</span>
        <el-pagination
          v-model:current-page="pagination.page"
          :page-size="pagination.pageSize"
          :total="total"
          layout="prev, pager, next"
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { logsAPI, usersAPI } from '../api'

const loading = ref(false)
const tableData = ref([])
const users = ref([])
const total = ref(0)

const pagination = reactive({
  page: 1,
  pageSize: 20
})

const filters = reactive({
  action: '',
  user: '',
  keyword: ''
})

const formatDate = (date) => {
  if (!date) return '-'
  return date.split('T')[0]
}

const formatTime = (date) => {
  if (!date) return ''
  const timePart = date.split('T')[1] || ''
  return timePart.split(':').slice(0, 2).join(':')
}

const getActionText = (action) => {
  const map = {
    create: '创建',
    update: '更新',
    delete: '删除',
    login: '登录',
    logout: '登出',
    export: '导出',
    reset_password: '重置密码'
  }
  return map[action] || action
}

const getModuleText = (module) => {
  const map = {
    auth: '认证',
    quotation: '报价单',
    module: '模块',
    material: '原材料',
    user: '用户管理',
    fee: '费用',
    exchange_rate: '汇率',
    fee_rate: '费用系数'
  }
  return map[module] || module
}

const fetchData = async () => {
  loading.value = true
  try {
    const res = await logsAPI.getList({
      page: pagination.page,
      page_size: pagination.pageSize,
      action: filters.action || undefined,
      user_id: filters.user || undefined,
      keyword: filters.keyword || undefined
    })
    tableData.value = res.items || []
    total.value = res.total || tableData.value.length
    // 加载用户列表
    if (users.value.length === 0) {
      const userRes = await usersAPI.getList({ page_size: 100 })
      users.value = userRes.items || []
    }
  } catch (error) {
    console.error('Failed to fetch logs:', error)
    ElMessage.error('加载日志失败')
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchData()
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.logs-page {
  padding: var(--spacing-lg);
}

.page-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
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

.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-primary {
  background: linear-gradient(135deg, #0D9488 0%, #14B8A6 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.4);
}

.btn-secondary {
  background: var(--color-bg-card);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border-light);
}

.btn-secondary:hover {
  background: var(--color-bg-page);
}

/* 筛选栏 */
.filter-bar {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
  align-items: center;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid var(--color-border-light);
  border-radius: 6px;
  font-size: 14px;
  background: var(--color-bg-card);
  color: var(--color-text-primary);
  cursor: pointer;
}

.search-box {
  flex: 1;
  display: flex;
  align-items: center;
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-light);
  border-radius: 6px;
  padding: 0 12px;
}

.search-icon {
  font-size: 16px;
  margin-right: 8px;
}

.search-input {
  flex: 1;
  border: none;
  background: transparent;
  padding: 8px 0;
  font-size: 14px;
  outline: none;
  color: var(--color-text-primary);
}

/* 内容卡片 */
.content-card {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  overflow: hidden;
  max-height: calc(100vh - 200px);
  display: flex;
  flex-direction: column;
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

.time-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.time-cell .date {
  font-weight: 500;
  color: var(--color-text-primary);
}

.time-cell .time {
  font-size: 12px;
  color: var(--color-text-secondary);
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-avatar {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: linear-gradient(135deg, #0D9488 0%, #14B8A6 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.username {
  font-weight: 500;
}

.action-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.action-badge.create {
  background: #DCFCE7;
  color: #16A34A;
}

.action-badge.update {
  background: #DBEAFE;
  color: #2563EB;
}

.action-badge.delete {
  background: #FEE2E2;
  color: #DC2626;
}

.action-badge.login, .action-badge.logout {
  background: #F3E8FF;
  color: #9333EA;
}

.action-badge.export {
  background: #FEF3C7;
  color: #D97706;
}

.description {
  color: var(--color-text-primary);
}

.ip-address {
  font-family: monospace;
  font-size: 12px;
  color: var(--color-text-secondary);
}

.empty-state {
  padding: 48px;
  text-align: center;
  color: var(--color-text-secondary);
}

.empty-icon {
  font-size: 48px;
  display: block;
  margin-bottom: 16px;
}

.pagination-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-top: 1px solid var(--color-border-light);
}

.total-count {
  font-size: 14px;
  color: var(--color-text-secondary);
}
</style>
