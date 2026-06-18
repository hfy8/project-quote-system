<template>
  <div class="trends-page">
    <!-- 顶部统计卡片 -->
    <section class="stats-grid">
      <div class="stat-card stat-primary">
        <div class="stat-icon">📋</div>
        <div class="stat-info">
          <span class="stat-value">{{ summary.total_count }}</span>
          <span class="stat-label">总报价单数</span>
        </div>
      </div>
      <div class="stat-card stat-success">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <span class="stat-value">{{ summary.total_approved }}</span>
          <span class="stat-label">已通过</span>
        </div>
      </div>
      <div class="stat-card stat-warning">
        <div class="stat-icon">📅</div>
        <div class="stat-info">
          <span class="stat-value">{{ summary.current_month_count }}</span>
          <span class="stat-label">本月新增</span>
        </div>
      </div>
      <div class="stat-card stat-info">
        <div class="stat-icon">💰</div>
        <div class="stat-info">
          <span class="stat-value">{{ formatPercent(summary.avg_gross_margin) }}</span>
          <span class="stat-label">平均毛利率</span>
        </div>
      </div>
    </section>

    <!-- 智能洞察 -->
    <section v-if="insights.length" class="insights-bar card">
      <h3 class="section-title">💡 智能洞察</h3>
      <ul class="insight-list">
        <li v-for="(s, i) in insights" :key="i" class="insight-item">{{ s }}</li>
      </ul>
    </section>

    <!-- 图表区：3 个 ECharts 图表 -->
    <div class="charts-grid">
      <!-- 月度趋势：折线 + 柱状 组合图 -->
      <section class="chart-card card">
        <div class="chart-header">
          <h3 class="section-title">月度趋势（数量 + 毛利率）</h3>
          <el-radio-group v-model="monthsRange" size="small" @change="loadData">
            <el-radio-button :value="3">3 月</el-radio-button>
            <el-radio-button :value="6">6 月</el-radio-button>
            <el-radio-button :value="12">12 月</el-radio-button>
          </el-radio-group>
        </div>
        <v-chart class="chart" :option="monthlyChartOption" autoresize />
      </section>

      <!-- 状态分布：饼图 -->
      <section class="chart-card card">
        <h3 class="section-title">状态分布</h3>
        <v-chart class="chart" :option="statusChartOption" autoresize />
      </section>

      <!-- 毛利率散点图 -->
      <section class="chart-card card chart-card-wide">
        <h3 class="section-title">毛利率散点（每点=一张报价单，颜色=状态）</h3>
        <v-chart class="chart" :option="scatterChartOption" autoresize />
      </section>

      <!-- 类型分布：环形图 -->
      <section class="chart-card card">
        <h3 class="section-title">类型分布</h3>
        <v-chart class="chart" :option="typeChartOption" autoresize />
      </section>
    </div>

    <!-- 加载态 -->
    <div v-if="loading" class="loading-mask">
      <el-icon class="is-loading"><Loading /></el-icon>
      <span>加载中…</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart, ScatterChart } from 'echarts/charts'
import {
  TitleComponent, TooltipComponent, GridComponent, LegendComponent,
  DatasetComponent, TransformComponent, MarkLineComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import { Loading } from '@element-plus/icons-vue'
import axios from 'axios'

use([
  CanvasRenderer, BarChart, LineChart, PieChart, ScatterChart,
  TitleComponent, TooltipComponent, GridComponent, LegendComponent,
  DatasetComponent, TransformComponent, MarkLineComponent,
])

const monthsRange = ref(6)
const summary = ref({ total_count: 0, total_approved: 0, current_month_count: 0, avg_gross_margin: 0, avg_profit_rate: 0 })
const monthly = ref([])
const byStatus = ref([])
const byType = ref([])
const scatter = ref([])
const insights = ref([])
const loading = ref(false)

const formatPercent = (v) => {
  if (!v && v !== 0) return '0%'
  return (v * 100).toFixed(1) + '%'
}

const STATUS_LABEL = {
  draft: '草稿', submitted: '审批中', approved: '已通过', archived: '已归档', rejected: '已驳回',
}
const TYPE_LABEL = { single: '单机', line: '线体', combined: '组合' }
const STATUS_COLOR = {
  draft: '#94a3b8', submitted: '#f59e0b', approved: '#10b981', archived: '#6366f1', rejected: '#ef4444',
}

// ============ 图表配置 ============
const monthlyChartOption = computed(() => {
  const periods = monthly.value.map(m => m.period)
  const counts = monthly.value.map(m => m.count)
  const profits = monthly.value.map(m => (m.avg_gross_margin * 100).toFixed(1))
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' },
    },
    legend: { data: ['报价单数', '平均毛利率(%)'], bottom: 0 },
    grid: { top: 30, right: 60, bottom: 40, left: 50 },
    xAxis: [{ type: 'category', data: periods, axisPointer: { type: 'shadow' } }],
    yAxis: [
      { type: 'value', name: '数量', position: 'left' },
      { type: 'value', name: '毛利率(%)', position: 'right', max: 50, axisLabel: { formatter: '{value}%' } },
    ],
    series: [
      {
        name: '报价单数', type: 'bar', data: counts,
        itemStyle: { color: '#3b82f6', borderRadius: [4, 4, 0, 0] },
        label: { show: true, position: 'top' },
      },
      {
        name: '平均利润率(%)', type: 'line', yAxisIndex: 1, data: profits,
        itemStyle: { color: '#10b981' }, lineStyle: { width: 3 },
        symbol: 'circle', symbolSize: 8,
        markLine: {
          data: [{ type: 'average', name: '平均' }],
          lineStyle: { color: '#f59e0b', type: 'dashed' },
        },
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
    legend: { bottom: 0 },
    series: [{
      name: '状态', type: 'pie', radius: ['45%', '70%'], center: ['50%', '45%'],
      avoidLabelOverlap: true, label: { show: true, formatter: '{b}\n{c} 单' },
      data,
    }],
  }
})

const typeChartOption = computed(() => {
  const data = byType.value.map(t => ({
    name: TYPE_LABEL[t.type] || t.type,
    value: t.count,
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
  // 按状态分组
  const groups = {}
  scatter.value.forEach(s => {
    if (!groups[s.status]) groups[s.status] = []
    groups[s.status].push([s.month, (s.gross_margin * 100).toFixed(1), s.id, s.name, s.status])
  })
  const series = Object.entries(groups).map(([status, data]) => ({
    name: STATUS_LABEL[status] || status,
    type: 'scatter',
    symbolSize: 14,
    itemStyle: { color: STATUS_COLOR[status] || '#94a3b8', opacity: 0.85 },
    data,
    emphasis: { focus: 'series', label: { show: true, formatter: (p) => p.data[3] } },
  }))
  return {
    tooltip: {
      trigger: 'item',
      formatter: (p) => {
        const [month, profit, id, name, status] = p.data
        return `<b>${name}</b><br/>状态: ${STATUS_LABEL[status]}<br/>月份: ${month}<br/>利润率: ${profit}%<br/><a href="/quotations/${id}" target="_blank">查看详情 →</a>`
      },
    },
    legend: { bottom: 0 },
    grid: { top: 30, right: 30, bottom: 50, left: 60 },
    xAxis: { type: 'category', name: '月份' },
    yAxis: { type: 'value', name: '利润率(%)', axisLabel: { formatter: '{value}%' } },
    series,
  }
})

// ============ 数据加载 ============
const loadData = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('token') || ''
    const res = await axios.get(`/api/quotations/trends?months=${monthsRange.value}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    summary.value = res.data.summary || summary.value
    monthly.value = res.data.monthly || []
    byStatus.value = res.data.by_status || []
    byType.value = res.data.by_type || []
    scatter.value = res.data.scatter || []
    insights.value = res.data.insights || []
  } catch (e) {
    console.error('加载趋势数据失败', e)
    // 错误兜底
    summary.value = { total_count: 0, total_approved: 0, current_month_count: 0, avg_gross_margin: 0, avg_profit_rate: 0 }
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
  padding: var(--spacing-lg, 20px);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}
.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  border-left: 4px solid #3b82f6;
}
.stat-card.stat-success { border-left-color: #10b981; }
.stat-card.stat-warning { border-left-color: #f59e0b; }
.stat-card.stat-info { border-left-color: #6366f1; }
.stat-icon { font-size: 32px; }
.stat-info { display: flex; flex-direction: column; }
.stat-value { font-size: 26px; font-weight: 700; color: #1e293b; }
.stat-label { font-size: 13px; color: #64748b; margin-top: 4px; }

.insights-bar {
  background: #fffbeb;
  border-left: 4px solid #f59e0b;
  padding: 16px 20px;
  margin-bottom: 20px;
  border-radius: 8px;
}
.insight-list { list-style: none; padding: 0; margin: 8px 0 0; }
.insight-item { padding: 6px 0; color: #92400e; font-size: 14px; }

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
.chart-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.chart-card-wide { grid-column: 1 / -1; }
.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 12px;
}
.chart {
  height: 360px;
  width: 100%;
}
.chart-card-wide .chart { height: 420px; }

.loading-mask {
  position: fixed;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255,255,255,0.95);
  padding: 20px 30px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 9999;
}

@media (max-width: 1024px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .charts-grid { grid-template-columns: 1fr; }
}
</style>
