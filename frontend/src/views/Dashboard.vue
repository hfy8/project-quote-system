<template>
  <div class="dashboard">
    <!-- ========== 顶部: 欢迎 + 周/月统计 + 操作按钮 (1 行) ========== -->
    <section class="top-row">
      <!-- 欢迎区 -->
      <div class="welcome-card">
        <div class="welcome-bg"></div>
        <div class="welcome-text">
          <h1 class="welcome-title">你好,{{ username }} 👋</h1>
          <p class="welcome-meta">
            <span class="welcome-role">{{ roleLabel }}</span>
            <span class="welcome-sep">·</span>
            <span>{{ currentTime }}</span>
          </p>
        </div>
        <div class="welcome-actions">
          <button v-if="hasPerm('quotation.create')" class="btn-pri" @click="$router.push('/quotations/new')">
            <span>＋</span> 新建报价单
          </button>
          <button class="btn-ghost" @click="$router.push('/ai-chat')">
            🤖 AI 助手
          </button>
        </div>
      </div>

      <!-- 本周业绩卡 (leader 全局, 其他用户 我的业绩) -->
      <div v-if="isLeader" class="summary-card summary-admin">
        <div class="summary-head">
          <span class="summary-icon">📊</span>
          <span class="summary-title">本周业绩</span>
        </div>
        <div class="summary-body">
          <div class="summary-stat">
            <span class="summary-num">{{ stats.quotations.weekly_new }}</span>
            <span class="summary-lbl">本周新增</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-stat">
            <span class="summary-num text-success">{{ stats.weekly_summary.approved || 0 }}</span>
            <span class="summary-lbl">本周通过</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-stat">
            <span class="summary-num text-warning">{{ stats.quotations.by_status.approved_pending }}</span>
            <span class="summary-lbl">待归档</span>
          </div>
        </div>
      </div>

      <div v-else class="summary-card summary-business">
        <div class="summary-head">
          <span class="summary-icon">📌</span>
          <span class="summary-title">我的概览</span>
        </div>
        <div class="summary-body">
          <div class="summary-stat">
            <span class="summary-num">{{ stats.top_clients[0]?.count || 0 }}</span>
            <span class="summary-lbl">参与项目</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-stat">
            <span class="summary-num text-primary">{{ stats.top_clients[1]?.count || 0 }}</span>
            <span class="summary-lbl">本月新增</span>
          </div>
          <div class="summary-divider"></div>
          <div class="summary-stat">
            <span class="summary-num text-success">{{ stats.top_clients[2]?.count || 0 }}</span>
            <span class="summary-lbl">本月通过</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ========== 中部 1: 6 张统计卡 ========== -->
    <section class="stats-row">
      <div class="stat-card stat-primary">
        <div class="stat-icon-wrap"><span>📋</span></div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.quotations.total }}</span>
          <span class="stat-label">报价单总数</span>
        </div>
      </div>
      <div class="stat-card stat-warning">
        <div class="stat-icon-wrap"><span>⏳</span></div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.quotations.by_status.approved_pending }}</span>
          <span class="stat-label">归档审批中</span>
        </div>
      </div>
      <div class="stat-card stat-info">
        <div class="stat-icon-wrap"><span>📝</span></div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.quotations.by_status.draft }}</span>
          <span class="stat-label">草稿</span>
        </div>
      </div>
      <div class="stat-card stat-success">
        <div class="stat-icon-wrap"><span>✅</span></div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.quotations.by_status.approved + stats.quotations.by_status.archived }}</span>
          <span class="stat-label">已通过/已归档</span>
        </div>
      </div>
      <div v-if="isLeader" class="stat-card stat-material">
        <div class="stat-icon-wrap"><span>📦</span></div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.materials.total }}</span>
          <span class="stat-label">物料总数</span>
          <div class="stat-sub">
            <span class="dot dot-large"></span>大件 {{ stats.materials.by_category.large }}
            <span class="dot dot-std"></span>核心 {{ stats.materials.by_category.standard }}
            <span class="dot dot-other"></span>其他 {{ stats.materials.by_category.other }}
          </div>
        </div>
      </div>
      <div v-else class="stat-card stat-msg">
        <div class="stat-icon-wrap"><span>🔔</span></div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.my_tasks.unread_messages }}</span>
          <span class="stat-label">未读消息</span>
        </div>
      </div>
      <div class="stat-card stat-trend">
        <div class="stat-icon-wrap"><span>📈</span></div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.quotations.monthly_new }}</span>
          <span class="stat-label">本月公司新增</span>
        </div>
      </div>
    </section>

    <!-- ========== 中部 2: 趋势 + 快捷 + 最近消息 (3 列等高无空白) ========== -->
    <section class="mid-grid">
      <!-- 最近 7 天趋势 -->
      <div class="panel trend-panel">
        <div class="panel-head">
          <h3 class="panel-title">📊 最近 7 天趋势</h3>
          <span class="panel-sub">新增 vs 已审批</span>
        </div>
        <div class="trend-chart">
          <div v-for="(item, idx) in stats.trend" :key="idx" class="trend-bar-wrap">
            <div class="trend-bar-group">
              <div class="trend-bar trend-new"
                   :style="{ height: getBarHeight(item.new, maxTrend) + 'px' }">
                <span v-if="item.new > 0" class="bar-num">{{ item.new }}</span>
              </div>
              <div class="trend-bar trend-approved"
                   :style="{ height: getBarHeight(item.approved, maxTrend) + 'px' }">
                <span v-if="item.approved > 0" class="bar-num">{{ item.approved }}</span>
              </div>
            </div>
            <div class="trend-bar-label">{{ item.date }}</div>
          </div>
        </div>
        <div class="trend-legend">
          <span class="legend-item"><span class="legend-dot legend-new"></span>新增</span>
          <span class="legend-item"><span class="legend-dot legend-approved"></span>已审批</span>
        </div>
      </div>

      <!-- 快捷操作 - 横排 8 个 -->
      <div class="panel actions-panel">
        <div class="panel-head">
          <h3 class="panel-title">⚡ 快捷操作</h3>
          <span class="panel-sub">常用入口</span>
        </div>
        <div class="actions-grid">
          <div v-if="hasPerm('quotation.create')" class="action-item" @click="$router.push('/quotations/new')">
            <div class="action-icon bg-primary"><span>➕</span></div>
            <span class="action-label">新建</span>
          </div>
          <div class="action-item" @click="$router.push('/quotations')">
            <div class="action-icon bg-success"><span>📋</span></div>
            <span class="action-label">报价单</span>
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
            <span class="action-label">趋势</span>
          </div>
          <div v-if="hasPerm('material.view')" class="action-item" @click="$router.push('/materials')">
            <div class="action-icon bg-amber"><span>📦</span></div>
            <span class="action-label">物料库</span>
          </div>
          <div v-if="hasPerm('fee_rate.view')" class="action-item" @click="$router.push('/fee-rates')">
            <div class="action-icon bg-pink"><span>📊</span></div>
            <span class="action-label">费用系数</span>
          </div>
          <div class="action-item" @click="$router.push('/ai-chat')">
            <div class="action-icon bg-teal"><span>🤖</span></div>
            <span class="action-label">AI</span>
          </div>
        </div>
      </div>

      <!-- 最近消息 -->
      <div class="panel msg-panel">
        <div class="panel-head">
          <h3 class="panel-title">🔔 最近消息</h3>
          <button class="panel-link" @click="$router.push('/messages')">查看 →</button>
        </div>
        <div class="msg-list">
          <div v-for="msg in stats.recent_messages" :key="msg.id"
               class="msg-item"
               :class="{ unread: !msg.is_read }"
               @click="goMessage(msg)">
            <span class="msg-icon" :class="msgTypeClass(msg.type)">{{ msgTypeIcon(msg.type) }}</span>
            <div class="msg-body">
              <div class="msg-title">{{ msg.title }}</div>
              <div class="msg-meta">
                <span>{{ msg.sender_name }}</span>
                <span>·</span>
                <span>{{ formatTime(msg.created_at) }}</span>
              </div>
            </div>
          </div>
          <div v-if="stats.recent_messages.length === 0" class="msg-empty">
            <span class="msg-empty-icon">📭</span>
            <p>暂无消息</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ========== 底部: 最近报价单 + Top 客户/我的业绩 (2 列等高) ========== -->
    <section class="bot-grid">
      <!-- 最近报价单 (占 60%) -->
      <div class="panel recent-panel">
        <div class="panel-head">
          <h3 class="panel-title">📄 最近报价单</h3>
          <button class="panel-link" @click="$router.push('/quotations')">查看全部 →</button>
        </div>
        <div class="quotations-list" v-loading="loading">
          <div
            v-for="item in recentQuotations"
            :key="item.id"
            class="quotation-item"
            @click="$router.push(`/quotations/${item.id}`)"
          >
            <div class="q-main">
              <span class="q-name">{{ item.name }}</span>
              <span class="q-type">{{ formatType(item.type) }}</span>
            </div>
            <div class="q-meta">
              <span class="q-status" :class="item.status">
                {{ formatStatus(item.status) }}
              </span>
              <span class="q-date">{{ formatDate(item.created_at) }}</span>
            </div>
          </div>
          <div v-if="!loading && recentQuotations.length === 0" class="empty">
            <span class="empty-icon">📋</span>
            <p>暂无报价单数据</p>
          </div>
        </div>
      </div>

      <!-- Top 5 客户 (admin) / 我的项目 (普通用户) (占 40%) -->
      <div class="panel clients-panel">
        <div class="panel-head">
          <h3 class="panel-title">
            <span v-if="isLeader">🏢 热门客户</span>
            <span v-else>📊 我的项目</span>
          </h3>
          <span class="panel-sub">{{ isLeader ? '本月 Top 5' : '近况' }}</span>
        </div>
        <div class="clients-list">
          <div
            v-for="(c, idx) in stats.top_clients"
            :key="idx"
            class="client-item"
            @click="c.latest_id && $router.push(`/quotations/${c.latest_id}`)"
          >
            <span class="client-rank" :class="'rank-' + (idx + 1)">{{ idx + 1 }}</span>
            <div class="client-info">
              <span class="client-name">{{ c.name }}</span>
              <span class="client-bar-wrap">
                <span class="client-bar" :style="{ width: getClientBarWidth(c.count) + '%' }"></span>
              </span>
            </div>
            <span class="client-count">{{ c.count }}</span>
          </div>
          <div v-if="stats.top_clients.length === 0" class="empty">
            <span class="empty-icon">📊</span>
            <p>{{ isLeader ? '暂无客户数据' : '暂无项目数据' }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 待办浮层 (高优先级) -->
    <div v-if="hasAnyTask" class="todo-float">
      <div class="todo-card">
        <span class="todo-title">📋 我的待办</span>
        <div class="todo-items">
          <div v-if="stats.my_tasks.pending_archives > 0"
               class="todo-item todo-warn"
               @click="$router.push('/quotations')">
            <span class="todo-num">{{ stats.my_tasks.pending_archives }}</span>
            <span class="todo-lbl">待审批归档</span>
          </div>
          <div v-if="stats.my_tasks.pending_changes > 0"
               class="todo-item todo-info"
               @click="$router.push('/change-requests')">
            <span class="todo-num">{{ stats.my_tasks.pending_changes }}</span>
            <span class="todo-lbl">待审变更</span>
          </div>
          <div v-if="stats.my_tasks.unread_messages > 0"
               class="todo-item todo-pri"
               @click="$router.push('/messages')">
            <span class="todo-num">{{ stats.my_tasks.unread_messages }}</span>
            <span class="todo-lbl">未读消息</span>
          </div>
          <div v-if="stats.my_tasks.unread_messages > 0"
               class="todo-item todo-action"
               @click="handleMarkAllRead">
            <span class="todo-icon">✅</span>
            <span class="todo-lbl">全部已读</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { quotationsAPI } from '../api'
import messagesAPI from '../api/messages'
import request from '../utils/request'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()

const username = computed(() => authStore.userInfo?.real_name || authStore.userInfo?.username || '用户')
const userRole = computed(() => authStore.userInfo?.role || 'business')
const userPosition = computed(() => authStore.userInfo?.position_name || '')
const roleLabel = computed(() => {
  // 优先用 position_name (更精确: 副总经理/经理/总监/业务员...)
  if (userPosition.value) return userPosition.value
  const map = { admin: '管理员', business: '业务员', purchaser: '采购员', viewer: '只读' }
  return map[userRole.value] || '用户'
})
const permissions = computed(() => authStore.userInfo?.permissions || [])
const isAdmin = computed(() => userRole.value === 'admin')
// Leader 判定: admin + 任何领导职位 (副总经理/经理/总监/部长/主管)
const isLeader = computed(() => {
  if (isAdmin.value) return true
  const pos = userPosition.value
  return /副总|经理|总监|部长|主管|总工|主任/i.test(pos)
})
const isGlobalView = isLeader

// 当前时间 (实时)
const currentTime = ref('')
let timer = null
const updateTime = () => {
  const d = new Date()
  const week = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  currentTime.value = `${d.getMonth() + 1}月${d.getDate()}日 ${week[d.getDay()]}`
}

const hasPerm = (p) => permissions.value.includes('*') || permissions.value.includes(p)

const stats = ref({
  quotations: { total: 0, by_status: {}, monthly_new: 0, weekly_new: 0 },
  materials: { total: 0, by_category: {} },
  my_tasks: { pending_archives: 0, pending_changes: 0, unread_messages: 0 },
  trend: [],
  top_clients: [],
  recent_messages: [],
  weekly_summary: {},
  user_role: 'business',
})

const maxTrend = computed(() => {
  let m = 1
  for (const t of stats.value.trend) m = Math.max(m, t.new, t.approved)
  return m
})
const getBarHeight = (val, max) => Math.max(2, Math.round((val / max) * 70))

const maxClient = computed(() => {
  let m = 1
  for (const c of stats.value.top_clients) m = Math.max(m, c.count)
  return m
})
const getClientBarWidth = (count) => Math.round((count / maxClient.value) * 100)

const hasAnyTask = computed(() => {
  const t = stats.value.my_tasks
  return t.pending_archives > 0 || t.pending_changes > 0 || t.unread_messages > 0
})

const recentQuotations = ref([])
const loading = ref(false)

const formatType = (type) => ({ single: '单项', line: '线体', combined: '组合' }[type] || type || '-')
const formatStatus = (s) => ({
  draft: '草稿', submitted: '已提交', approved: '已批准',
  approved_pending: '审批中', archived: '已归档', rejected: '已驳回',
}[s] || s)
const formatDate = (s) => {
  if (!s) return ''
  const d = new Date(s)
  return `${d.getMonth() + 1}/${d.getDate()}`
}
const formatTime = (s) => {
  if (!s) return ''
  const d = new Date(s)
  const now = new Date()
  const diff = (now - d) / 1000
  if (diff < 60) return '刚刚'
  if (diff < 3600) return `${Math.floor(diff / 60)}分钟前`
  if (diff < 86400) return `${Math.floor(diff / 3600)}小时前`
  return `${d.getMonth() + 1}/${d.getDate()}`
}

const msgTypeIcon = (type) => ({
  module_member_added: '👥',
  change_request_submitted: '📤',
  change_request_approved: '✅',
  change_request_rejected: '❌',
  version_updated: '🔄',
}[type] || '🔔')
const msgTypeClass = (type) => `msg-${type}`
const goMessage = (msg) => {
  if (msg.related_id) {
    if (msg.related_type === 'quotation') router.push(`/quotations/${msg.related_id}`)
    else if (msg.related_type === 'change_request') router.push(`/change-requests/${msg.related_id}`)
    else router.push('/messages')
  } else {
    router.push('/messages')
  }
}

const handleMarkAllRead = async () => {
  try {
    await ElMessageBox.confirm(
      `确认将全部 ${stats.value.my_tasks.unread_messages} 条未读消息标记为已读?`,
      '批量已读',
      { confirmButtonText: '全部已读', cancelButtonText: '取消', type: 'info' }
    )
    await messagesAPI.markAllRead()
    ElMessage.success('已全部标记为已读')
    stats.value.my_tasks.unread_messages = 0
    // 同步更新浮层中的消息列表
    if (stats.value.recent_messages) {
      stats.value.recent_messages = stats.value.recent_messages.map(m => ({ ...m, is_read: true }))
    }
    await fetchStats()
  } catch (e) {
    if (e !== 'cancel' && e?.message) {
      ElMessage.error('操作失败: ' + e.message)
    }
  }
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
    const res = await quotationsAPI.getList({ page: 1, pageSize: 6 })
    recentQuotations.value = res.items || res || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 60000)
  fetchStats()
  fetchRecent()
})
onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
/* ========== 整体布局: 占满 viewport, 不滚动 ========== */
.dashboard {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
  height: 100%;
}

/* ========== 顶部行 (欢迎 + 本周业绩) ========== */
.top-row {
  display: grid;
  grid-template-columns: 2.4fr 1fr;
  gap: 12px;
  flex-shrink: 0;
}

.welcome-card {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 24px;
  background: linear-gradient(135deg, var(--color-primary) 0%, #0F766E 100%);
  border-radius: 10px;
  color: white;
  overflow: hidden;
  min-height: 76px;
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
.welcome-text { position: relative; z-index: 1; }
.welcome-title { font-size: 20px; font-weight: 600; margin-bottom: 4px; }
.welcome-meta { font-size: 13px; opacity: 0.95; display: flex; gap: 6px; align-items: center; }
.welcome-role {
  background: rgba(255,255,255,0.22);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
}
.welcome-sep { opacity: 0.5; }

.welcome-actions { display: flex; gap: 8px; position: relative; z-index: 1; }
.btn-pri, .btn-ghost {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 7px 14px;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}
.btn-pri { background: white; color: var(--color-primary); }
.btn-pri:hover { transform: translateY(-1px); box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
.btn-pri span { font-size: 16px; font-weight: 600; }
.btn-ghost {
  background: rgba(255,255,255,0.2);
  color: white;
}
.btn-ghost:hover { background: rgba(255,255,255,0.3); }

/* 业绩卡 */
.summary-card {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border-light);
  border-radius: 10px;
  padding: 10px 18px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 76px;
  overflow: hidden;
}
.summary-head {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
}
.summary-icon { font-size: 14px; }
.summary-title { font-size: 13px; font-weight: 600; color: var(--color-text-primary); }
.summary-body { display: flex; align-items: center; gap: 0; }
.summary-stat { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 2px; }
.summary-num { font-size: 22px; font-weight: 700; line-height: 1; color: var(--color-text-primary); }
.summary-num.text-primary { color: var(--color-primary); }
.summary-num.text-success { color: var(--color-success); }
.summary-num.text-warning { color: var(--color-warning); }
.summary-lbl { font-size: 11px; color: var(--color-text-secondary); }
.summary-divider { width: 1px; height: 32px; background: var(--color-border-light); margin: 0 8px; }

/* ========== 统计卡 (6 张横排, 严格等宽) ========== */
.stats-row {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 10px;
  flex-shrink: 0;
}
.stat-card {
  background: var(--color-bg-card);
  border-radius: 8px;
  padding: 12px 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1px solid var(--color-border-light);
  transition: all 0.2s;
  min-height: 80px;
  overflow: hidden;
}
.stat-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
.stat-icon-wrap {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}
.stat-info { display: flex; flex-direction: column; min-width: 0; gap: 1px; flex: 1; }
.stat-value { font-size: 22px; font-weight: 700; color: var(--color-text-primary); line-height: 1.1; }
.stat-label { font-size: 12px; color: var(--color-text-secondary); line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.stat-sub { font-size: 10.5px; color: var(--color-text-secondary); margin-top: 2px; display: flex; align-items: center; gap: 4px; flex-wrap: wrap; line-height: 1.3; }
.dot { width: 6px; height: 6px; border-radius: 50%; display: inline-block; flex-shrink: 0; }
.dot-large { background: #3B82F6; }
.dot-std { background: var(--color-success); }
.dot-other { background: var(--color-warning); }

.stat-primary .stat-icon-wrap { background: var(--color-primary-light); }
.stat-success .stat-icon-wrap { background: var(--color-success-bg); }
.stat-warning .stat-icon-wrap { background: var(--color-warning-bg); }
.stat-info .stat-icon-wrap { background: var(--color-info-bg); }
.stat-material .stat-icon-wrap { background: #FEF3C7; }
.stat-team .stat-icon-wrap { background: #FCE7F3; }
.stat-msg .stat-icon-wrap { background: var(--color-warning-bg); }
.stat-trend .stat-icon-wrap { background: #F3E8FF; }

/* ========== 中部 3 列 (趋势 + 快捷 + 消息) ========== */
.mid-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 12px;
  flex-shrink: 0;
}
.panel {
  background: var(--color-bg-card);
  border-radius: 10px;
  border: 1px solid var(--color-border-light);
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  min-height: 200px;
  overflow: hidden;
}
.panel-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 10px;
  flex-shrink: 0;
}
.panel-title { font-size: 14px; font-weight: 600; color: var(--color-text-primary); margin: 0; }
.panel-sub { font-size: 11px; color: var(--color-text-secondary); }
.panel-link {
  background: transparent;
  border: none;
  color: var(--color-primary);
  font-size: 12px;
  cursor: pointer;
  padding: 0;
}
.panel-link:hover { opacity: 0.7; }

/* 趋势图 */
.trend-chart {
  display: flex;
  gap: 6px;
  align-items: flex-end;
  height: 200px;
  padding: 8px 0 0;
  border-bottom: 1px dashed var(--color-border-light);
  margin-bottom: 8px;
  margin-top: 6px;
}
.trend-bar-wrap { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 4px; }
.trend-bar-group { display: flex; gap: 3px; align-items: flex-end; height: 168px; width: 100%; justify-content: center; }
.trend-bar {
  width: 14px;
  border-radius: 4px 4px 0 0;
  min-height: 2px;
  position: relative;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  transition: opacity 0.2s;
}
.trend-bar:hover { opacity: 0.8; }
.bar-num { font-size: 10px; color: white; padding-top: 2px; font-weight: 600; }
.trend-new { background: var(--color-primary); }
.trend-approved { background: var(--color-success); }
.trend-bar-label { font-size: 10.5px; color: var(--color-text-secondary); }
.trend-legend {
  display: flex;
  gap: 14px;
  font-size: 11px;
  color: var(--color-text-secondary);
}
.legend-item { display: flex; align-items: center; gap: 4px; }
.legend-dot { width: 8px; height: 8px; border-radius: 50%; }
.legend-new { background: var(--color-primary); }
.legend-approved { background: var(--color-success); }

/* 快捷操作 - 横排 8 个, 一行满 */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
  margin-top: 4px;
}
.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 10px 6px;
  background: var(--color-bg-page);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}
.action-item:hover {
  background: var(--color-primary-light);
  transform: translateY(-1px);
}
.action-icon {
  width: 32px;
  height: 32px;
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}
.bg-primary { background: var(--color-primary-light); }
.bg-success { background: var(--color-success-bg); }
.bg-warning { background: var(--color-warning-bg); }
.bg-info { background: var(--color-info-bg); }
.bg-purple { background: #F3E8FF; }
.bg-amber { background: #FEF3C7; }
.bg-pink { background: #FCE7F3; }
.bg-teal { background: #CCFBF1; }
.action-label { font-size: 12px; font-weight: 500; }

/* 最近消息 */
.msg-list { display: flex; flex-direction: column; gap: 6px; overflow-y: auto; flex: 1; }
.msg-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px;
  background: var(--color-bg-page);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  border-left: 3px solid transparent;
}
.msg-item:hover { background: var(--color-primary-light); }
.msg-item.unread { border-left-color: var(--color-primary); background: var(--color-primary-light); }
.msg-icon {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--color-bg-card);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}
.msg-body { flex: 1; min-width: 0; }
.msg-title { font-size: 12.5px; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.msg-meta { font-size: 10.5px; color: var(--color-text-secondary); display: flex; gap: 4px; margin-top: 1px; }
.msg-empty { text-align: center; padding: 30px 0; color: var(--color-text-secondary); }
.msg-empty-icon { font-size: 28px; display: block; opacity: 0.5; margin-bottom: 4px; }
.msg-empty p { font-size: 12px; margin: 0; }

/* ========== 底部 2 列 (报价单 + 客户) ========== */
.bot-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 12px;
  flex: 1;
  min-height: 0;
}
.quotations-list { display: flex; flex-direction: column; gap: 5px; overflow-y: auto; flex: 1; }
.quotation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: var(--color-bg-page);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}
.quotation-item:hover { background: var(--color-primary-light); transform: translateX(2px); }
.q-main { display: flex; flex-direction: column; gap: 2px; min-width: 0; flex: 1; }
.q-name { font-size: 13px; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.q-type { font-size: 11px; color: var(--color-text-secondary); }
.q-meta { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.q-status {
  font-size: 10.5px;
  padding: 2px 7px;
  border-radius: 3px;
  font-weight: 500;
}
.q-status.draft { background: var(--color-info-bg); color: var(--color-info); }
.q-status.approved { background: var(--color-success-bg); color: var(--color-success); }
.q-status.approved_pending { background: var(--color-warning-bg); color: var(--color-warning); }
.q-status.archived { background: #E0E7FF; color: #4338CA; }
.q-status.rejected { background: var(--color-danger-bg); color: var(--color-danger); }
.q-status.submitted { background: var(--color-warning-bg); color: var(--color-warning); }
.q-date { font-size: 11px; color: var(--color-text-secondary); }

/* Top 客户 */
.clients-list { display: flex; flex-direction: column; gap: 6px; overflow-y: auto; flex: 1; }
.client-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 8px;
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 4px;
}
.client-item:hover { background: var(--color-bg-page); }
.client-rank {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: var(--color-bg-page);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  color: var(--color-text-secondary);
  flex-shrink: 0;
}
.client-rank.rank-1 { background: linear-gradient(135deg, #FFD700, #FFA500); color: white; }
.client-rank.rank-2 { background: linear-gradient(135deg, #C0C0C0, #808080); color: white; }
.client-rank.rank-3 { background: linear-gradient(135deg, #CD7F32, #8B4513); color: white; }
.client-info { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 3px; }
.client-name { font-size: 12.5px; font-weight: 500; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.client-bar-wrap { height: 4px; background: var(--color-bg-page); border-radius: 2px; overflow: hidden; }
.client-bar { display: block; height: 100%; background: linear-gradient(90deg, var(--color-primary), var(--color-success)); border-radius: 2px; }
.client-count { font-size: 14px; font-weight: 700; color: var(--color-text-primary); flex-shrink: 0; }

.empty { text-align: center; padding: 24px 0; color: var(--color-text-secondary); }
.empty-icon { font-size: 28px; display: block; opacity: 0.5; margin-bottom: 4px; }
.empty p { font-size: 12px; margin: 0; }

/* ========== 待办浮层 (右下角悬浮, 不影响布局) ========== */
.todo-float {
  position: fixed;
  bottom: 16px;
  right: 16px;
  z-index: 100;
  max-width: 320px;
}
.todo-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 6px 24px rgba(0,0,0,0.12), 0 2px 6px rgba(0,0,0,0.06);
  padding: 12px 16px;
  border: 1px solid var(--color-border-light);
}
.todo-title {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 8px;
}
.todo-items { display: flex; gap: 8px; flex-wrap: wrap; }
.todo-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 8px 12px;
  background: var(--color-bg-page);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 80px;
  border-left: 3px solid;
}
.todo-item:hover { transform: translateY(-1px); box-shadow: var(--shadow-sm); }
.todo-warn { border-left-color: var(--color-warning); }
.todo-info { border-left-color: var(--color-info); }
.todo-pri { border-left-color: var(--color-primary); }
.todo-action { border-left-color: var(--color-success); cursor: pointer; background: #f0fdf4; }
.todo-action:hover { background: #dcfce7; }
.todo-icon { font-size: 16px; line-height: 1; }
.todo-num { font-size: 18px; font-weight: 700; line-height: 1; }
.todo-lbl { font-size: 11px; color: var(--color-text-secondary); }
</style>