<template>
  <div class="dashboard">
    <!-- 欢迎区域 -->
    <section class="welcome-section">
      <div class="welcome-content">
        <h1 class="welcome-title">你好，{{ username }} 👋</h1>
        <p class="welcome-subtitle">
          <span v-if="isAdmin">管理系统总览</span>
          <span v-else>您参与的报价项目</span>
        </p>
      </div>
      <div class="welcome-actions">
        <button v-if="isAdmin" class="btn btn-primary" @click="$router.push('/quotations/new')">
          <span>+</span> 新建报价单
        </button>
      </div>
    </section>

    <!-- 统计卡片 -->
    <section class="stats-grid">
      <div class="stat-card stat-primary">
        <div class="stat-icon">📋</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.total }}</span>
          <span class="stat-label">{{ isAdmin ? '报价单总数' : '参与的报价单' }}</span>
        </div>
      </div>
      <div class="stat-card stat-success">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.approved }}</span>
          <span class="stat-label">已通过</span>
        </div>
      </div>
      <div class="stat-card stat-warning">
        <div class="stat-icon">⏳</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.pending }}</span>
          <span class="stat-label">待审核</span>
        </div>
      </div>
      <div v-if="isAdmin" class="stat-card stat-info">
        <div class="stat-icon">📦</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.materials }}</span>
          <span class="stat-label">物料数量</span>
        </div>
      </div>
    </section>

    <!-- 快捷操作 & 最近报价 -->
    <div class="dashboard-grid">
      <!-- 快捷操作 -->
      <section class="quick-actions card">
        <h3 class="section-title">快捷操作</h3>
        <div class="actions-grid">
          <div class="action-item" @click="$router.push('/quotations/new')">
            <div class="action-icon bg-primary">
              <span>➕</span>
            </div>
            <span class="action-label">新建报价单</span>
          </div>
          <div class="action-item" @click="$router.push('/quotations')">
            <div class="action-icon bg-success">
              <span>📋</span>
            </div>
            <span class="action-label">报价单管理</span>
          </div>
          <div class="action-item" @click="$router.push('/materials')">
            <div class="action-icon bg-warning">
              <span>📦</span>
            </div>
            <span class="action-label">原材料库</span>
          </div>
          <div class="action-item" @click="$router.push('/users')">
            <div class="action-icon bg-info">
              <span>👥</span>
            </div>
            <span class="action-label">用户管理</span>
          </div>
        </div>
      </section>

      <!-- 最近报价单 -->
      <section class="recent-quotations card">
        <div class="section-header">
          <h3 class="section-title">最近报价单</h3>
          <button class="btn btn-ghost" @click="$router.push('/quotations')">查看全部 →</button>
        </div>

        <div class="quotations-list" v-loading="loading">
          <div
            v-for="item in recentQuotations"
            :key="item.id"
            class="quotation-item"
            @click="$router.push(`/quotations/${item.id}`)"
          >
            <div class="quotation-main">
              <span class="quotation-name">{{ item.name }}</span>
              <span class="quotation-type">{{ formatType(item.type) }}</span>
            </div>
            <div class="quotation-meta">
              <span class="quotation-status" :class="item.status">
                {{ formatStatus(item.status) }}
              </span>
              <span class="quotation-date">{{ formatDate(item.created_at) }}</span>
            </div>
          </div>

          <div v-if="!loading && recentQuotations.length === 0" class="empty-state">
            <span class="empty-icon">📋</span>
            <p class="empty-text">暂无报价单数据</p>
            <button class="btn btn-primary" @click="$router.push('/quotations/new')">
              创建第一个报价单
            </button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { quotationsAPI, materialsAPI, modulesAPI } from '../api'

const authStore = useAuthStore()

const username = computed(() => authStore.userInfo?.real_name || authStore.userInfo?.username || '管理员')
const userRole = computed(() => authStore.userInfo?.role || 'admin')
const isAdmin = computed(() => userRole.value === 'admin')

const recentQuotations = ref([])
const materials = ref([])
const myModules = ref([])
const loading = ref(false)

const stats = computed(() => ({
  total: recentQuotations.value.length || 0,
  approved: recentQuotations.value.filter(q => q.status === 'approved').length || 0,
  pending: recentQuotations.value.filter(q => q.status === 'draft' || q.status === 'submitted').length || 0,
  materials: materials.value.length || 0
}))

const formatType = (type) => {
  const types = { single: '单项', line: '线体', combined: '组合' }
  return types[type] || type
}

const formatStatus = (status) => {
  const statuses = {
    draft: '草稿',
    submitted: '已提交',
    approved: '已批准',
    rejected: '已拒绝'
  }
  return statuses[status] || status
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}

const fetchData = async () => {
  loading.value = true
  try {
    const [quotationsRes, materialsRes] = await Promise.all([
      quotationsAPI.getList(),
      materialsAPI.getList().catch(() => ({ items: [] }))
    ])

    const quotations = quotationsRes.items || quotationsRes || []
    recentQuotations.value = quotations.slice(0, 5)
    materials.value = materialsRes.items || materialsRes || []
  } catch (error) {
    console.error('Failed to fetch data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.dashboard {
  padding: var(--spacing-lg);
}

/* 欢迎区域 */
.welcome-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xl);
  padding: var(--spacing-xl);
  background: linear-gradient(135deg, var(--color-primary) 0%, #0F766E 100%);
  border-radius: var(--radius-xl);
  color: white;
}

.welcome-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: var(--spacing-xs);
}

.welcome-subtitle {
  font-size: 14px;
  opacity: 0.9;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-lg);
  background: white;
  color: var(--color-primary);
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-primary span {
  font-size: 18px;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.stat-card {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  border: 1px solid var(--color-border-light);
  transition: all var(--transition-normal);
  overflow: hidden;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.stat-icon {
  font-size: 28px;
  width: 52px;
  height: 52px;
  border-radius: var(--radius-lg);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  line-height: 1;
}

.stat-primary .stat-icon { background: var(--color-primary-light); }
.stat-success .stat-icon { background: var(--color-success-bg); }
.stat-warning .stat-icon { background: var(--color-warning-bg); }
.stat-info .stat-icon { background: var(--color-info-bg); }

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-top: 2px;
}

/* 仪表盘网格 */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: var(--spacing-lg);
}

/* 卡片通用样式 */
.card {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  border: 1px solid var(--color-border-light);
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-md);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.section-header .section-title {
  margin-bottom: 0;
}

.btn-ghost {
  background: none;
  border: none;
  color: var(--color-primary);
  font-size: 13px;
  cursor: pointer;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  transition: all var(--transition-fast);
}

.btn-ghost:hover {
  background: var(--color-bg-hover);
}

/* 快捷操作 */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-lg);
  border-radius: var(--radius-md);
  background: var(--color-bg-hover);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.action-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.action-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}

.bg-primary { background: var(--color-primary-light); }
.bg-success { background: var(--color-success-bg); }
.bg-warning { background: var(--color-warning-bg); }
.bg-info { background: var(--color-info-bg); }

.action-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-primary);
}

/* 报价单列表 */
.quotations-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.quotation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  border-radius: var(--radius-md);
  background: var(--color-bg-hover);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.quotation-item:hover {
  background: var(--color-primary-light);
}

.quotation-main {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.quotation-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.quotation-type {
  font-size: 12px;
  color: var(--color-text-muted);
  padding: 2px 8px;
  background: var(--color-bg-card);
  border-radius: var(--radius-full);
}

.quotation-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.quotation-status {
  font-size: 12px;
  padding: 2px 10px;
  border-radius: var(--radius-full);
  font-weight: 500;
}

.quotation-status.draft {
  background: var(--color-info-bg);
  color: var(--color-info);
}

.quotation-status.submitted {
  background: var(--color-warning-bg);
  color: var(--color-warning);
}

.quotation-status.approved {
  background: var(--color-success-bg);
  color: var(--color-success);
}

.quotation-status.rejected {
  background: var(--color-danger-bg);
  color: var(--color-danger);
}

.quotation-date {
  font-size: 12px;
  color: var(--color-text-muted);
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: var(--spacing-2xl);
}

.empty-icon {
  font-size: 48px;
  opacity: 0.5;
  display: block;
  margin-bottom: var(--spacing-md);
}

.empty-text {
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-md);
}

/* 响应式 */
@media (max-width: 1024px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .welcome-section {
    flex-direction: column;
    text-align: center;
    gap: var(--spacing-md);
  }

  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
