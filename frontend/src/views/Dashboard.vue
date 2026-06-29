<template>
  <div class="dashboard">
    <!-- 欢迎横幅 -->
    <section class="welcome-section">
      <div class="welcome-bg"></div>
      <div class="welcome-content">
        <h1 class="welcome-title">你好，{{ username }} 👋</h1>
        <p class="welcome-subtitle">
          <span v-if="isAdmin">欢迎回来，今天也要高效处理报价单 ✨</span>
          <span v-else>您参与的报价项目概览</span>
          <span class="welcome-time"> · {{ currentTime }}</span>
        </p>
      </div>
      <div class="welcome-actions">
        <button v-if="hasPerm('quotation.create')" class="btn btn-primary" @click="$router.push('/quotations/new')">
          <span>+</span> 新建报价单
        </button>
        <button class="btn btn-ghost" @click="$router.push('/ai-chat')">
          🤖 AI 助手
        </button>
      </div>
    </section>

    <!-- 统计卡片 + 我的待办 + 物料分类 - 一行内混合布局 -->
    <section class="stats-row">
      <!-- 6 张统计卡 -->
      <div class="stats-grid">
        <div class="stat-card stat-primary">
          <div class="stat-icon">📋</div>
          <div class="stat-info">
            <span class="stat-value">{{ stats.quotations.total }}</span>
            <span class="stat-label">报价单总数</span>
          </div>
        </div>
        <div class="stat-card stat-warning">
          <div class="stat-icon">⏳</div>
          <div class="stat-info">
            <span class="stat-value">{{ stats.quotations.by_status.approved_pending }}</span>
            <span class="stat-label">归档审批中</span>
          </div>
        </div>
        <div class="stat-card stat-info">
          <div class="stat-icon">📝</div>
          <div class="stat-info">
            <span class="stat-value">{{ stats.quotations.by_status.draft }}</span>
            <span class="stat-label">草稿</span>
          </div>
        </div>
        <div class="stat-card stat-success">
          <div class="stat-icon">✅</div>
          <div class="stat-info">
            <span class="stat-value">{{ stats.quotations.by_status.approved + stats.quotations.by_status.archived }}</span>
            <span class="stat-label">已通过 / 已归档</span>
          </div>
        </div>
        <div v-if="isAdmin" class="stat-card stat-material">
          <div class="stat-icon">📦</div>
          <div class="stat-info">
            <span class="stat-value">{{ stats.materials.total }}</span>
            <span class="stat-label">物料总数</span>
            <div class="stat-subtags">
              <span class="subtag subtag-large">大件 {{ stats.materials.by_category.large }}</span>
              <span class="subtag subtag-std">核心 {{ stats.materials.by_category.standard }}</span>
              <span class="subtag subtag-other">其他 {{ stats.materials.by_category.other }}</span>
            </div>
          </div>
        </div>
        <div v-else class="stat-card stat-task">
          <div class="stat-icon">📌</div>
          <div class="stat-info">
            <span class="stat-value">{{ stats.my_tasks.pending_archives + stats.my_tasks.pending_changes }}</span>
            <span class="stat-label">我的待办</span>
          </div>
        </div>
        <div class="stat-card stat-trend">
          <div class="stat-icon">📈</div>
          <div class="stat-info">
            <span class="stat-value">{{ stats.quotations.monthly_new }}</span>
            <span class="stat-label">本月新增</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 我的待办 (独立块, 仅当有内容时显示) -->
    <section v-if="hasAnyTask" class="my-tasks card">
      <div class="section-header">
        <h3 class="section-title">📋 我的待办</h3>
        <span class="section-subtitle">需要您处理的待办事项</span>
      </div>
      <div class="tasks-grid">
        <div v-if="stats.my_tasks.pending_archives > 0"
             class="task-item task-warning"
             @click="$router.push('/quotations')">
          <div class="task-icon">📦</div>
          <div class="task-info">
            <span class="task-count">{{ stats.my_tasks.pending_archives }}</span>
            <span class="task-label">待审批归档</span>
          </div>
          <div class="task-arrow">→</div>
        </div>
        <div v-if="stats.my_tasks.pending_changes > 0"
             class="task-item task-info"
             @click="$router.push('/change-requests')">
          <div class="task-icon">📤</div>
          <div class="task-info">
            <span class="task-count">{{ stats.my_tasks.pending_changes }}</span>
            <span class="task-label">待审变更申请</span>
          </div>
          <div class="task-arrow">→</div>
        </div>
        <div v-if="stats.my_tasks.unread_messages > 0"
             class="task-item task-primary"
             @click="openMessages">
          <div class="task-icon">🔔</div>
          <div class="task-info">
            <span class="task-count">{{ stats.my_tasks.unread_messages }}</span>
            <span class="task-label">未读消息</span>
          </div>
          <div class="task-arrow">→</div>
        </div>
      </div>
    </section>

    <!-- 趋势图 + 快捷操作 + 最近报价单 (三列等高) -->
    <div class="dashboard-main-grid">
      <!-- 最近 7 天趋势 -->
      <section class="trend-section card">
        <div class="section-header">
          <h3 class="section-title">📊 最近 7 天趋势</h3>
        </div>
        <div class="trend-chart">
          <div v-for="(item, idx) in stats.trend" :key="idx" class="trend-bar-wrap">
            <div class="trend-bar-group">
              <div class="trend-bar trend-new"
                   :style="{ height: getBarHeight(item.new, maxTrend) + 'px' }"
                   :title="`新增: ${item.new}`"></div>
              <div class="trend-bar trend-approved"
                   :style="{ height: getBarHeight(item.approved, maxTrend) + 'px' }"
                   :title="`已审批: ${item.approved}`"></div>
            </div>
            <div class="trend-bar-label">{{ item.date }}</div>
          </div>
        </div>
        <div class="trend-legend">
          <span class="legend-item"><span class="legend-dot legend-new"></span>新增</span>
          <span class="legend-item"><span class="legend-dot legend-approved"></span>已审批</span>
        </div>
      </section>

      <!-- 快捷操作 -->
      <section class="quick-actions card">
        <div class="section-header">
          <h3 class="section-title">⚡ 快捷操作</h3>
        </div>
        <div class="actions-grid">
          <div v-if="hasPerm('quotation.create')" class="action-item" @click="$router.push('/quotations/new')">
            <div class="action-icon bg-primary"><span>➕</span></div>
            <span class="action-label">新建报价单</span>
          </div>
          <div class="action-item" @click="$router.push('/quotations')">
            <div class="action-icon bg-success"><span>📋</span></div>
            <span class="action-label">报价单管理</span>
          </div>
          <div class="action-item" @click="$router.push('/my-assignments')">
            <div class="action-icon bg-warning"><span>📌</span></div>
            <span class="action-label">我的分配</span>
          </div>
          <div v-if="hasPerm('quotation.edit')" class="action-item" @click="$router.push('/change-requests')">
            <div class="action-icon bg-info"><span>📤</span></div>
            <span class="action-label">变更审核</span>
          </div>
          <div class="action-item" @click="$router.push('/trends')">
            <div class="action-icon bg-purple"><span>📈</span></div>
            <span class="action-label">报价趋势</span>
          </div>
          <div v-if="hasPerm('material.view')" class="action-item" @click="$router.push('/materials')">
            <div class="action-icon bg-amber"><span>📦</span></div>
            <span class="action-label">原材料库</span>
          </div>
          <div v-if="hasPerm('fee_rate.view')" class="action-item" @click="$router.push('/fee-rates')">
            <div class="action-icon bg-pink"><span>📊</span></div>
            <span class="action-label">费用系数</span>
          </div>
          <div class="action-item" @click="$router.push('/ai-chat')">
            <div class="action-icon bg-teal"><span>🤖</span></div>
            <span class="action-label">AI 助手</span>
          </div>
        </div>
      </section>

      <!-- 最近报价单 (重要信息加大列宽) -->
      <section class="recent-quotations card">
        <div class="section-header">
          <h3 class="section-title">📄 最近报价单</h3>
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
            <button v-if="hasPerm('quotation.create')" class="btn btn-primary" @click="$router.push('/quotations/new')">
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
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { quotationsAPI, materialsAPI } from '../api'
import request from '../utils/request'

const router = useRouter()
const authStore = useAuthStore()

const username = computed(() => authStore.userInfo?.real_name || authStore.userInfo?.username || '管理员')
const userRole = computed(() => authStore.userInfo?.role || 'admin')
const isAdmin = computed(() => userRole.value === 'admin')

// 当前时间
const currentTime = ref('')
const updateTime = () => {
  const d = new Date()
  currentTime.value = d.toLocaleDateString('zh-CN', { month: 'long', day: 'numeric', weekday: 'long' })
}

// 权限判断
const permissions = computed(() => authStore.userInfo?.permissions || [])
const hasPerm = (p) => permissions.value.includes('*') || permissions.value.includes(p)

// 统计数据
const stats = ref({
  quotations: { total: 0, by_status: {}, monthly_new: 0 },
  materials: { total: 0, by_category: {} },
  my_tasks: { pending_archives: 0, pending_changes: 0, unread_messages: 0 },
  trend: [],
})
const maxTrend = computed(() => {
  let m = 1
  for (const t of stats.value.trend) {
    m = Math.max(m, t.new, t.approved)
  }
  return m
})
const getBarHeight = (val, max) => {
  if (max === 0) return 4
  return Math.max(4, (val / max) * 80)
}
const hasAnyTask = computed(() => {
  const t = stats.value.my_tasks
  return t.pending_archives > 0 || t.pending_changes > 0 || t.unread_messages > 0
})

const recentQuotations = ref([])
const loading = ref(false)

const formatType = (type) => {
  const types = { single: '单项', line: '线体', combined: '组合' }
  return types[type] || type
}
const formatStatus = (status) => {
  const statuses = {
    draft: '草稿',
    submitted: '已提交',
    approved: '已批准',
    approved_pending: '审批中',
    archived: '已归档',
    rejected: '已驳回',
  }
  return statuses[status] || status
}
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('zh-CN', { month: 'numeric', day: 'numeric' })
}

const fetchStats = async () => {
  try {
    const res = await request.get('/dashboard/stats')
    stats.value = res
  } catch (e) {
    console.error('Failed to load dashboard stats:', e)
  }
}

const fetchRecent = async () => {
  loading.value = true
  try {
    const res = await quotationsAPI.getList({ page: 1, pageSize: 8 })
    recentQuotations.value = res.items || res || []
  } catch (e) {
    console.error('Failed to load recent quotations:', e)
  } finally {
    loading.value = false
  }
}

const openMessages = () => {
  const bell = document.querySelector('.message-bell')
  if (bell) bell.click()
}

onMounted(() => {
  updateTime()
  fetchStats()
  fetchRecent()
})
</script>

<style scoped>
/* ============== 占满空白 + 自然高度 不滚动 ============== */
.dashboard {
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

/* ============== 欢迎区域 ============== */
.welcome-section {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 24px;
  background: linear-gradient(135deg, var(--color-primary) 0%, #0F766E 100%);
  border-radius: 10px;
  color: white;
  overflow: hidden;
  flex-shrink: 0;
}
.welcome-bg {
  position: absolute;
  top: -50%;
  right: -10%;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
  pointer-events: none;
}
.welcome-content { position: relative; z-index: 1; }
.welcome-title { font-size: 20px; font-weight: 600; margin-bottom: 4px; }
.welcome-subtitle { font-size: 13px; opacity: 0.92; }
.welcome-time { opacity: 0.7; }

.welcome-actions {
  display: flex;
  gap: 8px;
  position: relative;
  z-index: 1;
}
.btn-primary, .btn-ghost {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 7px 16px;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  white-space: nowrap;
}
.btn-primary {
  background: white;
  color: var(--color-primary);
}
.btn-primary:hover { transform: translateY(-1px); box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
.btn-primary span { font-size: 16px; font-weight: 600; }
.btn-ghost {
  background: rgba(255,255,255,0.2);
  color: white;
  backdrop-filter: blur(10px);
}
.btn-ghost:hover { background: rgba(255,255,255,0.3); }

/* ============== 统计卡区 (混合样式) ============== */
.stats-row { flex-shrink: 0; }
.stats-grid {
  display: grid;
  /* 7 列布局: 即使普通用户也是 6 张卡 (我的待办 替换 物料) */
  grid-template-columns: repeat(6, 1fr);
  gap: 10px;
}
.stat-card {
  background: var(--color-bg-card);
  border-radius: 8px;
  padding: 12px 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  border: 1px solid var(--color-border-light);
  transition: all var(--transition-fast);
  overflow: hidden;
  min-height: 90px;
}
.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
.stat-icon {
  font-size: 24px;
  width: 44px;
  height: 44px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  line-height: 1;
}
.stat-info { display: flex; flex-direction: column; min-width: 0; gap: 1px; }
.stat-value { font-size: 26px; font-weight: 700; color: var(--color-text-primary); line-height: 1.1; }
.stat-label { font-size: 12px; color: var(--color-text-secondary); line-height: 1.2; }
.stat-subtags { margin-top: 4px; display: flex; flex-wrap: wrap; gap: 3px; line-height: 1.4; }
.subtag {
  font-size: 11px;
  padding: 2px 5px;
  border-radius: 3px;
  font-weight: 500;
}
.subtag-large { background: #DBEAFE; color: #1E40AF; }
.subtag-std { background: #D1FAE5; color: #065F46; }
.subtag-other { background: #FEF3C7; color: #92400E; }

.stat-primary .stat-icon { background: var(--color-primary-light); color: var(--color-primary); }
.stat-success .stat-icon { background: var(--color-success-bg); color: var(--color-success); }
.stat-warning .stat-icon { background: var(--color-warning-bg); color: var(--color-warning); }
.stat-info .stat-icon { background: var(--color-info-bg); color: var(--color-info); }
.stat-material .stat-icon { background: #FEF3C7; color: #D97706; }
.stat-task .stat-icon { background: #FCE7F3; color: #DB2777; }
.stat-trend .stat-icon { background: #F3E8FF; color: #7C3AED; }

/* 数字长文本不换行 */
.stat-card:nth-child(4) .stat-label,
.stat-card:nth-child(5) .stat-label { white-space: nowrap; }

/* ============== 我的待办 (独立块, 仅待办时显示) ============== */
.my-tasks {
  padding: 12px 16px;
  background: var(--color-bg-card);
  border-radius: 8px;
  border: 1px solid var(--color-border-light);
  flex-shrink: 0;
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 8px;
}
.section-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}
.section-subtitle {
  font-size: 12px;
  color: var(--color-text-secondary);
}
.tasks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 10px;
}
.task-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  background: var(--color-bg-page);
  border-radius: 6px;
  cursor: pointer;
  transition: all var(--transition-fast);
  border: 1px solid var(--color-border-light);
  border-left: 4px solid;
}
.task-item:hover {
  transform: translateX(2px);
  box-shadow: var(--shadow-sm);
}
.task-icon { font-size: 22px; }
.task-info { display: flex; flex-direction: column; flex: 1; }
.task-count { font-size: 20px; font-weight: 700; line-height: 1.1; }
.task-label { font-size: 12px; color: var(--color-text-secondary); }
.task-arrow {
  font-size: 16px;
  opacity: 0.4;
  transition: all var(--transition-fast);
}
.task-item:hover .task-arrow { opacity: 1; transform: translateX(2px); }

.task-warning { border-left-color: var(--color-warning); }
.task-warning .task-count { color: var(--color-warning); }
.task-info { border-left-color: var(--color-info); }
.task-info .task-count { color: var(--color-info); }
.task-primary { border-left-color: var(--color-primary); }
.task-primary .task-count { color: var(--color-primary); }

/* ============== 主体三列 (趋势/快捷/最近) - 自然高度 ============== */
.dashboard-main-grid {
  display: grid;
  grid-template-columns: 0.7fr 0.5fr 1.2fr;
  gap: 12px;
  flex-shrink: 0;
}
.dashboard-main-grid > section {
  padding: 14px 18px;
  background: var(--color-bg-card);
  border-radius: 8px;
  border: 1px solid var(--color-border-light);
  display: flex;
  flex-direction: column;
}
@media (max-width: 1100px) {
  .dashboard-main-grid { grid-template-columns: 1fr; }
}

/* ============== 趋势图 ============== */
.trend-chart {
  display: flex;
  gap: 8px;
  align-items: flex-end;
  height: 120px;
  padding: 10px 0;
  border-bottom: 1px dashed var(--color-border-light);
  margin-bottom: 8px;
  margin-top: 4px;
}
.trend-bar-wrap { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 4px; }
.trend-bar-group { display: flex; gap: 2px; align-items: flex-end; height: 80px; }
.trend-bar {
  width: 10px;
  border-radius: 4px 4px 0 0;
  transition: all var(--transition-fast);
  min-height: 4px;
}
.trend-new { background: var(--color-primary); }
.trend-approved { background: var(--color-success); }
.trend-bar-label { font-size: 11px; color: var(--color-text-secondary); }
.trend-legend {
  display: flex;
  gap: 14px;
  font-size: 12px;
  color: var(--color-text-secondary);
}
.legend-item { display: flex; align-items: center; gap: 4px; }
.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}
.legend-new { background: var(--color-primary); }
.legend-approved { background: var(--color-success); }

/* ============== 快捷操作 ============== */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
  margin-top: 4px;
}
.action-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: var(--color-bg-page);
  border-radius: 6px;
  cursor: pointer;
  transition: all var(--transition-fast);
}
.action-item:hover {
  background: var(--color-primary-light);
  transform: translateX(2px);
}
.action-icon {
  width: 30px;
  height: 30px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  flex-shrink: 0;
}
.bg-primary { background: var(--color-primary-light); }
.bg-success { background: var(--color-success-bg); }
.bg-warning { background: var(--color-warning-bg); }
.bg-info { background: var(--color-info-bg); }
.bg-purple { background: #F3E8FF; }
.bg-amber { background: #FEF3C7; }
.bg-pink { background: #FCE7F3; }
.bg-teal { background: #CCFBF1; }
.action-label { font-size: 13px; font-weight: 500; }

/* ============== 最近报价单 ============== */
.quotations-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: 4px;
}
.quotation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background: var(--color-bg-page);
  border-radius: 6px;
  cursor: pointer;
  transition: all var(--transition-fast);
}
.quotation-item:hover {
  background: var(--color-primary-light);
  transform: translateX(2px);
}
.quotation-main { display: flex; flex-direction: column; gap: 3px; min-width: 0; }
.quotation-name { font-size: 13px; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.quotation-type { font-size: 11px; color: var(--color-text-secondary); }
.quotation-meta { display: flex; flex-direction: column; align-items: flex-end; gap: 3px; flex-shrink: 0; }
.quotation-status {
  font-size: 11px;
  padding: 2px 7px;
  border-radius: 3px;
  font-weight: 500;
}
.quotation-status.draft { background: var(--color-info-bg); color: var(--color-info); }
.quotation-status.approved { background: var(--color-success-bg); color: var(--color-success); }
.quotation-status.approved_pending { background: var(--color-warning-bg); color: var(--color-warning); }
.quotation-status.archived { background: #E0E7FF; color: #4338CA; }
.quotation-status.rejected { background: var(--color-danger-bg); color: var(--color-danger); }
.quotation-status.submitted { background: var(--color-warning-bg); color: var(--color-warning); }
.quotation-date { font-size: 11px; color: var(--color-text-secondary); }

.empty-state {
  text-align: center;
  padding: 24px 0;
  color: var(--color-text-secondary);
}
.empty-icon { font-size: 40px; opacity: 0.5; display: block; margin-bottom: 8px; }
.empty-text { margin-bottom: 10px; }

.card {
  background: var(--color-bg-card);
  border-radius: 8px;
  border: 1px solid var(--color-border-light);
}

.btn-ghost {
  background: transparent;
  color: var(--color-primary);
  border: none;
  cursor: pointer;
  font-size: 12px;
}
.btn-ghost:hover { opacity: 0.7; }
</style>
