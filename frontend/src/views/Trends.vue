<template>
  <div class="trends-page">
    <!-- ============ 顶部: 4 张统计卡 + 环比 ============ -->
    <section class="stats-grid">
      <div class="stat-card stat-primary">
        <div class="stat-icon">📋</div>
        <div class="stat-info">
          <span class="stat-value">{{ summary.total_count }}</span>
          <span class="stat-label">总报价单数 ({{ monthsRange }}月内)</span>
        </div>
      </div>
      <div class="stat-card stat-success">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <span class="stat-value">{{ summary.total_approved }}</span>
          <span class="stat-label">已通过</span>
          <span class="stat-sub">{{ approvalRate }}% 通过率</span>
        </div>
      </div>
      <div class="stat-card stat-warning">
        <div class="stat-icon">📅</div>
        <div class="stat-info">
          <span class="stat-value">{{ summary.current_month_count }}</span>
          <span class="stat-label">本月新增</span>
          <span class="stat-sub" :class="momClass">
            <span v-if="summary.month_over_month > 0">↑ +{{ summary.month_over_month }}</span>
            <span v-else-if="summary.month_over_month < 0">↓ {{ summary.month_over_month }}</span>
            <span v-else>— 持平</span>
            <span class="mom-suffix">较上月</span>
          </span>
        </div>
      </div>
      <div class="stat-card stat-info">
        <div class="stat-icon">💰</div>
        <div class="stat-info">
          <span class="stat-value">{{ formatPercent(summary.avg_gross_margin) }}</span>
          <span class="stat-label">平均毛利率</span>
          <span class="stat-sub">对外利润率 {{ formatPercent(summary.avg_profit_rate) }}</span>
        </div>
      </div>
    </section>

    <!-- ============ 智能洞察 ============ -->
    <section v-if="insights.length" class="insights-bar card">
      <h3 class="section-title">💡 智能洞察</h3>
      <ul class="insight-list">
        <li v-for="(s, i) in insights" :key="i" class="insight-item">{{ s }}</li>
      </ul>
    </section>

    <!-- ============ 图表区 ============ -->
    <div class="charts-grid">
      <!-- 月度趋势 (宽) -->
      <section class="chart-card card chart-card-wide">
        <div class="chart-header">
          <h3 class="section-title">📈 月度趋势 (数量 + 通过率 + 毛利率)</h3>
          <el-radio-group v-model="monthsRange" size="small" @change="loadData">
            <el-radio-button :value="3">3 月</el-radio-button>
            <el-radio-button :value="6">6 月</el-radio-button>
            <el-radio-button :value="12">12 月</el-radio-button>
            <el-radio-button :value="24">24 月</el-radio-button>
          </el-radio-group>
        </div>
        <v-chart class="chart chart-tall" :option="monthlyChartOption" autoresize />
      </section>

      <!-- 状态分布 -->
      <section class="chart-card card">
        <h3 class="section-title">🥧 状态分布</h3>
        <v-chart class="chart" :option="statusChartOption" autoresize />
      </section>

      <!-- 类型分布 -->
      <section class="chart-card card">
        <h3 class="section-title">🌹 类型分布 (玫瑰图)</h3>
        <v-chart class="chart" :option="typeChartOption" autoresize />
      </section>

      <!-- 毛利率散点 (宽) -->
      <section class="chart-card card chart-card-wide">
        <h3 class="section-title">🎯 毛利率散点 (颜色=状态, 大小=数量, 点击跳转详情)</h3>
        <v-chart v-if="lazyReady" class="chart" :option="scatterChartOption" autoresize @click="onScatterClick" />
      </section>
    </div>

    <!-- ============ 排行榜区 (3 列) ============ -->
    <div v-if="lazyReady" class="rank-grid">
      <!-- 客户 Top 5 -->
      <section class="rank-card card">
        <div class="rank-head">
          <h3 class="section-title">🏆 客户 Top 5</h3>
          <span class="rank-sub">按报价单数量</span>
        </div>
        <ul class="rank-list">
          <li v-for="(c, idx) in topClients" :key="idx" class="rank-item" @click="goQuotation(c)">
            <span class="rank-num" :class="'rank-medal-' + (idx + 1)">{{ idx + 1 }}</span>
            <div class="rank-info">
              <span class="rank-name">{{ c.name }}</span>
              <div class="rank-bar-wrap">
                <div class="rank-bar" :style="{ width: getBarWidth(c.count, maxClientCount) + '%' }"></div>
              </div>
            </div>
            <div class="rank-stats">
              <span class="rank-count">{{ c.count }} 单</span>
              <span class="rank-margin">{{ formatPercent(c.avg_gross_margin) }}</span>
            </div>
          </li>
          <li v-if="topClients.length === 0" class="empty">暂无数据</li>
        </ul>
      </section>

      <!-- 创建人 Top 5 -->
      <section class="rank-card card">
        <div class="rank-head">
          <h3 class="section-title">👨‍💼 创建人 Top 5</h3>
          <span class="rank-sub">按报价单数量</span>
        </div>
        <ul class="rank-list">
          <li v-for="(u, idx) in topCreators" :key="idx" class="rank-item">
            <span class="rank-num" :class="'rank-medal-' + (idx + 1)">{{ idx + 1 }}</span>
            <div class="rank-info">
              <span class="rank-name">{{ u.name }}</span>
              <div class="rank-bar-wrap">
                <div class="rank-bar" :style="{ width: getBarWidth(u.count, maxCreatorCount) + '%' }"></div>
              </div>
            </div>
            <div class="rank-stats">
              <span class="rank-count">{{ u.count }} 单</span>
              <span class="rank-margin">{{ formatPercent(u.avg_gross_margin) }}</span>
            </div>
          </li>
          <li v-if="topCreators.length === 0" class="empty">暂无数据</li>
        </ul>
      </section>

      <!-- 利润率最高 / 最低 -->
      <section class="rank-card card">
        <div class="rank-head">
          <h3 class="section-title">💎 利润率 Top 5</h3>
          <span class="rank-sub">最高 vs 最低</span>
        </div>
        <div class="profit-compare">
          <div class="profit-side profit-top">
            <div class="profit-side-title">🚀 最高</div>
            <ul class="rank-list">
              <li v-for="(q, idx) in topProfitQuotations" :key="'t' + idx" class="rank-item" @click="$router.push(`/quotations/${q.id}`)">
                <span class="rank-num rank-medal-success">{{ idx + 1 }}</span>
                <span class="rank-name" :title="q.name">{{ q.name }}</span>
                <span class="rank-margin text-success">{{ formatPercent(q.gross_margin) }}</span>
              </li>
              <li v-if="topProfitQuotations.length === 0" class="empty">暂无数据</li>
            </ul>
          </div>
          <div class="profit-divider"></div>
          <div class="profit-side profit-bottom">
            <div class="profit-side-title">⚠️ 最低</div>
            <ul class="rank-list">
              <li v-for="(q, idx) in bottomProfitQuotations" :key="'b' + idx" class="rank-item" @click="$router.push(`/quotations/${q.id}`)">
                <span class="rank-num rank-medal-warn">{{ idx + 1 }}</span>
                <span class="rank-name" :title="q.name">{{ q.name }}</span>
                <span class="rank-margin text-warning">{{ formatPercent(q.gross_margin) }}</span>
              </li>
              <li v-if="bottomProfitQuotations.length === 0" class="empty">暂无数据</li>
            </ul>
          </div>
        </div>
      </section>
    </div>

    <!-- ============ 加载态 ============ -->
    <div v-if="loading" class="loading-mask">
      <el-icon class="is-loading"><Loading /></el-icon>
      <span>加载中…</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart, ScatterChart } from 'echarts/charts'
import {
  TitleComponent, TooltipComponent, GridComponent, LegendComponent,
  DatasetComponent, TransformComponent, MarkLineComponent, DataZoomComponent,
} from 'echarts/components'
import VChart from 'vue-echarts'
import { Loading } from '@element-plus/icons-vue'
import request from '@/utils/request'

use([
  CanvasRenderer, BarChart, LineChart, PieChart, ScatterChart,
  TitleComponent, TooltipComponent, GridComponent, LegendComponent,
  DatasetComponent, TransformComponent, MarkLineComponent, DataZoomComponent,
])

const router = useRouter()

const monthsRange = ref(6)
const lazyReady = ref(false)  // 延迟挂载折叠下方图表

onMounted(async () => {
  loadData()
  await nextTick()
  // 等第一帧渲染完再挂载折叠下方图表（scatter + 排行榜）
  setTimeout(() => { lazyReady.value = true }, 200)
})
const summary = ref({
  total_count: 0, total_approved: 0,
  avg_gross_margin: 0, avg_profit_rate: 0,
  current_month_count: 0, prev_month_count: 0, month_over_month: 0,
})
const monthly = ref([])
const byStatus = ref([])
const byType = ref([])
const scatter = ref([])
const topClients = ref([])
const topCreators = ref([])
const topProfitQuotations = ref([])
const bottomProfitQuotations = ref([])
const insights = ref([])
const loading = ref(false)

const approvalRate = computed(() => {
  if (!summary.value.total_count) return 0
  return ((summary.value.total_approved / summary.value.total_count) * 100).toFixed(1)
})

const momClass = computed(() => {
  const m = summary.value.month_over_month
  if (m > 0) return 'text-success'
  if (m < 0) return 'text-danger'
  return ''
})

const maxClientCount = computed(() => Math.max(1, ...topClients.value.map(c => c.count)))
const maxCreatorCount = computed(() => Math.max(1, ...topCreators.value.map(c => c.count)))

const formatPercent = (v) => {
  if (!v && v !== 0) return '0%'
  return (v * 100).toFixed(1) + '%'
}

const getBarWidth = (val, max) => Math.round((val / max) * 100)

const goQuotation = (c) => {
  // 客户名直接跳到列表过滤
  router.push({ path: '/quotations', query: { name: c.name } })
}

const STATUS_LABEL = {
  draft: '草稿', submitted: '审批中', approved: '已通过',
  archived: '已归档', rejected: '已驳回', approved_pending: '待归档',
}
const TYPE_LABEL = { single: '单机', line: '线体', combined: '组合' }
const STATUS_COLOR = {
  draft: '#94a3b8', submitted: '#f59e0b', approved: '#10b981',
  archived: '#6366f1', rejected: '#ef4444', approved_pending: '#3b82f6',
}

// ============ 图表配置 ============
const monthlyChartOption = computed(() => {
  const periods = monthly.value.map(m => m.period)
  const counts = monthly.value.map(m => m.count)
  const approved = monthly.value.map(m => m.approved)
  const approvalRate = monthly.value.map(m =>
    m.count > 0 ? ((m.approved / m.count) * 100).toFixed(1) : 0
  )
  const profits = monthly.value.map(m => (m.avg_gross_margin * 100).toFixed(1))
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' },
    },
    legend: { data: ['报价单数', '已通过', '通过率(%)', '毛利率(%)'], bottom: 0 },
    grid: { top: 50, right: 60, bottom: 60, left: 50 },
    xAxis: [{ type: 'category', data: periods, axisPointer: { type: 'shadow' }, axisLabel: { interval: 0 } }],
    yAxis: [
      { type: 'value', name: '数量', position: 'left' },
      { type: 'value', name: '比率(%)', position: 'right', max: 100, axisLabel: { formatter: '{value}%' } },
    ],
    series: [
      {
        name: '报价单数', type: 'bar', data: counts,
        itemStyle: { color: '#3b82f6', borderRadius: [4, 4, 0, 0] },
        label: { show: true, position: 'top', formatter: '{c}' },
        barGap: 0,
      },
      {
        name: '已通过', type: 'bar', data: approved,
        itemStyle: { color: '#10b981', borderRadius: [4, 4, 0, 0] },
        label: { show: true, position: 'top', formatter: '{c}' },
      },
      {
        name: '通过率(%)', type: 'line', yAxisIndex: 1, data: approvalRate,
        itemStyle: { color: '#f59e0b' }, lineStyle: { width: 3 },
        symbol: 'circle', symbolSize: 8,
        markLine: {
          data: [{ type: 'average', name: '平均' }],
          lineStyle: { color: '#f59e0b', type: 'dashed' },
        },
      },
      {
        name: '毛利率(%)', type: 'line', yAxisIndex: 1, data: profits,
        itemStyle: { color: '#8b5cf6' }, lineStyle: { width: 3, type: 'dashed' },
        symbol: 'diamond', symbolSize: 10,
      },
    ],
  }
})

const statusChartOption = computed(() => {
  const data = byStatus.value.map(s => ({
    name: STATUS_LABEL[s.status] || s.status,
    value: s.count,
    itemStyle: { color: STATUS_COLOR[s.status] || '#94a3b8' },
  }))
  return {
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    legend: { bottom: 0, type: 'scroll' },
    series: [{
      name: '状态', type: 'pie', radius: ['40%', '70%'], center: ['50%', '45%'],
      avoidLabelOverlap: true, label: { show: true, formatter: '{b}\n{c} 单' },
      data,
    }],
  }
})

const typeChartOption = computed(() => {
  const data = byType.value.map(t => ({
    name: TYPE_LABEL[t.type] || t.type,
    value: t.count,
    itemStyle: { color: { single: '#3b82f6', line: '#10b981', combined: '#f59e0b' }[t.type] || '#94a3b8' },
  }))
  return {
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    legend: { bottom: 0 },
    series: [{
      name: '类型', type: 'pie', radius: '65%', center: ['50%', '45%'],
      roseType: 'radius',
      label: { formatter: '{b}\n{c} 单' },
      data,
    }],
  }
})

const scatterChartOption = computed(() => {
  const groups = {}
  const monthSet = new Set()
  scatter.value.forEach(s => {
    monthSet.add(s.month)
    if (!groups[s.status]) groups[s.status] = []
    groups[s.status].push({
      name: s.name,
      value: [s.month, Number((s.gross_margin * 100).toFixed(1)), s.id, s.status],
    })
  })
  const sortedMonths = Array.from(monthSet).sort()
  const series = Object.entries(groups).map(([status, data]) => ({
    name: STATUS_LABEL[status] || status,
    type: 'scatter',
    symbolSize: 14,
    itemStyle: { color: STATUS_COLOR[status] || '#94a3b8', opacity: 0.85 },
    data,
    emphasis: { focus: 'series', label: { show: true, formatter: (p) => p.data.name } },
  }))
  return {
    tooltip: {
      trigger: 'item',
      formatter: (p) => {
        const [month, profit, id, status] = p.data.value
        return `<b>${p.data.name}</b><br/>状态: ${STATUS_LABEL[status]}<br/>月份: ${month}<br/>毛利率: ${profit}%<br/><a href="/quotations/${id}" target="_blank">查看详情 →</a>`
      },
    },
    legend: { bottom: 0, type: 'scroll' },
    grid: { top: 30, right: 30, bottom: 50, left: 60 },
    xAxis: { type: 'category', data: sortedMonths, name: '月份', nameLocation: 'middle', nameGap: 28 },
    yAxis: { type: 'value', name: '毛利率(%)', axisLabel: { formatter: '{value}%' } },
    series,
  }
})

const onScatterClick = (params) => {
  if (params.data?.value?.[2]) {
    router.push(`/quotations/${params.data.value[2]}`)
  }
}

// ============ 数据加载 ============
const loadData = async () => {
  loading.value = true
  try {
    const d = await request.get(`/quotations/trends`, { params: { months: monthsRange.value } })
    summary.value = d.summary || summary.value
    monthly.value = d.monthly || []
    byStatus.value = d.by_status || []
    byType.value = d.by_type || []
    scatter.value = d.scatter || []
    topClients.value = d.top_clients || []
    topCreators.value = d.top_creators || []
    topProfitQuotations.value = d.top_profit_quotations || []
    bottomProfitQuotations.value = d.bottom_profit_quotations || []
    insights.value = d.insights || []
  } catch (e) {
    console.error('加载趋势数据失败', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.trends-page {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-height: 100%;
}

/* ============ 统计卡 ============ */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}
.stat-card {
  background: #fff;
  border-radius: 10px;
  padding: 16px 18px;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  border-left: 4px solid #3b82f6;
  min-height: 80px;
}
.stat-card.stat-success { border-left-color: #10b981; }
.stat-card.stat-warning { border-left-color: #f59e0b; }
.stat-card.stat-info { border-left-color: #6366f1; }
.stat-icon { font-size: 32px; }
.stat-info { display: flex; flex-direction: column; gap: 2px; flex: 1; min-width: 0; }
.stat-value { font-size: 26px; font-weight: 700; color: #1e293b; line-height: 1.1; }
.stat-label { font-size: 12px; color: #64748b; }
.stat-sub { font-size: 11px; color: #94a3b8; margin-top: 1px; }
.mom-suffix { margin-left: 4px; color: #94a3b8; font-size: 10px; }

/* ============ 智能洞察 ============ */
.insights-bar {
  background: linear-gradient(90deg, #fffbeb 0%, #fef3c7 100%);
  border-left: 4px solid #f59e0b;
  padding: 12px 18px;
  border-radius: 8px;
}
.insights-bar .section-title { margin-bottom: 6px; }
.insight-list {
  list-style: none; padding: 0; margin: 0;
  display: flex; flex-wrap: wrap; gap: 8px 16px;
}
.insight-item {
  color: #92400e; font-size: 13px;
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 12px;
}

/* ============ 图表网格 ============ */
.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.chart-card {
  background: #fff;
  border-radius: 10px;
  padding: 14px 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
}
.chart-card-wide { grid-column: 1 / -1; }
.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  flex-wrap: wrap;
  gap: 8px;
}
.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}
.chart {
  height: 280px;
  width: 100%;
}
.chart-tall { height: 360px; }

/* ============ 排行榜 ============ */
.rank-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.rank-card {
  background: #fff;
  border-radius: 10px;
  padding: 14px 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
}
.rank-head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 8px;
}
.rank-sub {
  font-size: 11px;
  color: #94a3b8;
}
.rank-list {
  list-style: none;
  padding: 0;
  margin: 0;
  flex: 1;
}
.rank-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 7px 4px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s;
}
.rank-item:hover { background: #f8fafc; }
.rank-num {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  background: #f1f5f9;
  color: #64748b;
  flex-shrink: 0;
}
.rank-medal-1 { background: linear-gradient(135deg, #fbbf24, #f59e0b); color: white; }
.rank-medal-2 { background: linear-gradient(135deg, #cbd5e1, #94a3b8); color: white; }
.rank-medal-3 { background: linear-gradient(135deg, #d97706, #b45309); color: white; }
.rank-medal-success { background: linear-gradient(135deg, #86efac, #22c55e); color: white; }
.rank-medal-warn { background: linear-gradient(135deg, #fcd34d, #f59e0b); color: white; }

.rank-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.rank-name {
  font-size: 13px;
  color: #1e293b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.rank-bar-wrap {
  height: 4px;
  background: #f1f5f9;
  border-radius: 2px;
  overflow: hidden;
}
.rank-bar {
  height: 100%;
  background: linear-gradient(90deg, #60a5fa, #3b82f6);
  border-radius: 2px;
  transition: width 0.3s;
}
.rank-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
  flex-shrink: 0;
}
.rank-count {
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
}
.rank-margin {
  font-size: 11px;
  color: #94a3b8;
}

/* ============ 利润率对比 ============ */
.profit-compare {
  display: flex;
  flex: 1;
  gap: 0;
}
.profit-side {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.profit-side-title {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  margin-bottom: 6px;
  text-align: center;
  padding-bottom: 4px;
}
.profit-top .profit-side-title { color: #10b981; }
.profit-bottom .profit-side-title { color: #f59e0b; }
.profit-divider {
  width: 1px;
  background: #e2e8f0;
  margin: 0 8px;
}
.text-success { color: #10b981; }
.text-warning { color: #f59e0b; }
.text-danger { color: #ef4444; }

.empty {
  text-align: center;
  color: #94a3b8;
  padding: 20px 0;
  font-size: 13px;
}

/* ============ 加载态 ============ */
.loading-mask {
  position: fixed;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255, 255, 255, 0.95);
  padding: 20px 30px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 9999;
}

/* ============ 响应式 ============ */
@media (max-width: 1100px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .rank-grid { grid-template-columns: 1fr; }
  .charts-grid { grid-template-columns: 1fr; }
}
</style>