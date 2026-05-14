<template>
  <div class="fees-page">
    <!-- 页面标题栏 -->
    <div class="page-header-bar">
      <div class="header-left">
        <h1 class="page-title">费用管理</h1>
        <span class="page-desc">按项目查看所有费用明细</span>
      </div>
    </div>

    <!-- 费用汇总卡片 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon factory">🏭</div>
        <div class="stat-info">
          <span class="stat-label">厂内费用</span>
          <span class="stat-value">¥ {{ formatNumber(factoryTotal) }}</span>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon outside">🌐</div>
        <div class="stat-info">
          <span class="stat-label">厂外费用</span>
          <span class="stat-value">¥ {{ formatNumber(outsideTotal) }}</span>
        </div>
      </div>
      <div class="stat-card highlight">
        <div class="stat-icon total">💰</div>
        <div class="stat-info">
          <span class="stat-label">费用总计</span>
          <span class="stat-value">¥ {{ formatNumber(factoryTotal + outsideTotal) }}</span>
        </div>
      </div>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-bar">
      <div class="filter-item">
        <select v-model="filters.quotation_id" class="filter-select" @change="fetchFees">
          <option value="">全部项目</option>
          <option v-for="q in quotations" :key="q.id" :value="q.id">
            {{ q.name || '未命名' }} ({{ q.scheme_no }})
          </option>
        </select>
      </div>
      <div class="filter-item">
        <select v-model="filters.location" class="filter-select" @change="fetchFees">
          <option value="">全部位置</option>
          <option value="internal">厂内</option>
          <option value="external">厂外</option>
        </select>
      </div>
      <div class="filter-item search-box">
        <span class="search-icon">🔍</span>
        <input
          v-model="filters.keyword"
          type="text"
          class="search-input"
          placeholder="搜索费用名称..."
          @keyup.enter="fetchFees"
        />
      </div>
      <button class="btn btn-secondary" @click="fetchFees">搜索</button>
    </div>

    <!-- 按项目分组显示 -->
    <div v-if="groupedFees.length > 0" class="quotation-groups">
      <div v-for="group in groupedFees" :key="group.quotation_id" class="quotation-group">
        <div class="group-header" @click="toggleGroup(group.quotation_id)">
          <div class="group-info">
            <span class="expand-icon">{{ expandedGroups[group.quotation_id] ? '▼' : '▶' }}</span>
            <span class="project-name">{{ group.project_name || '未命名项目' }}</span>
            <span class="project-no">{{ group.project_no }}</span>
          </div>
          <div class="group-stats">
            <span class="stat-item internal">厂内: ¥ {{ formatNumber(group.internal_total) }}</span>
            <span class="stat-item external">厂外: ¥ {{ formatNumber(group.external_total) }}</span>
            <span class="stat-item total">合计: ¥ {{ formatNumber(group.total) }}</span>
          </div>
        </div>

        <div v-if="expandedGroups[group.quotation_id]" class="group-content">
          <el-table :data="group.fees" stripe class="fee-table">
            <el-table-column prop="module_name" label="模块" min-width="120">
              <template #default="{ row }">
                {{ row.module_name || '-' }}
              </template>
            </el-table-column>
            <el-table-column prop="fee_type" label="费用类型" min-width="150">
              <template #default="{ row }">
                <div class="fee-type-cell">
                  <span class="fee-badge" :class="row.location">{{ row.location === 'internal' ? '厂内' : '厂外' }}</span>
                  <span class="fee-name">{{ row.fee_type }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="amount" label="金额" width="140" align="right">
              <template #default="{ row }">
                <span class="amount">¥ {{ formatNumber(row.amount) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="description" label="说明" min-width="200" show-overflow-tooltip />
            <el-table-column prop="created_at" label="创建时间" width="120">
              <template #default="{ row }">
                {{ formatDate(row.created_at) }}
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <span class="empty-icon">📋</span>
      <p>暂无费用记录</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { feesAPI } from '../api/fees'
import { quotationsAPI } from '../api/quotations'

const loading = ref(false)
const quotations = ref([])
const allFees = ref([])
const expandedGroups = ref({})

const filters = reactive({
  quotation_id: '',
  location: '',
  keyword: ''
})

// 计算费用汇总
const factoryTotal = computed(() => {
  return allFees.value
    .filter(f => f.location === 'internal')
    .reduce((sum, f) => sum + (f.amount || 0), 0)
})

const outsideTotal = computed(() => {
  return allFees.value
    .filter(f => f.location === 'external')
    .reduce((sum, f) => sum + (f.amount || 0), 0)
})

// 按项目分组
const groupedFees = computed(() => {
  const groups = {}

  let fees = [...allFees.value]

  // 按项目筛选
  if (filters.quotation_id) {
    fees = fees.filter(f => f.quotation_id === parseInt(filters.quotation_id))
  }

  // 按位置筛选
  if (filters.location) {
    fees = fees.filter(f => f.location === filters.location)
  }

  // 按关键字筛选
  if (filters.keyword) {
    const kw = filters.keyword.toLowerCase()
    fees = fees.filter(f =>
      (f.fee_type || '').toLowerCase().includes(kw) ||
      (f.module_name || '').toLowerCase().includes(kw) ||
      (f.description || '').toLowerCase().includes(kw)
    )
  }

  // 按quotation_id分组
  fees.forEach(fee => {
    const qid = fee.quotation_id
    if (!groups[qid]) {
      const quotation = quotations.value.find(q => q.id === qid) || {}
      groups[qid] = {
        quotation_id: qid,
        project_name: quotation.name || '未命名项目',
        project_no: quotation.scheme_no || '',
        fees: [],
        internal_total: 0,
        external_total: 0,
        total: 0
      }
    }
    groups[qid].fees.push(fee)
    groups[qid].total += fee.amount || 0
    if (fee.location === 'internal') {
      groups[qid].internal_total += fee.amount || 0
    } else {
      groups[qid].external_total += fee.amount || 0
    }
  })

  return Object.values(groups).sort((a, b) => b.quotation_id - a.quotation_id)
})

const formatNumber = (num) => {
  return Number(num || 0).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDate = (date) => {
  if (!date) return '-'
  return date.split('T')[0]
}

const toggleGroup = (quotationId) => {
  expandedGroups.value[quotationId] = !expandedGroups.value[quotationId]
}

const fetchQuotations = async () => {
  try {
    const res = await quotationsAPI.getList({ page_size: 100 })
    quotations.value = res.items || res || []
  } catch (error) {
    console.error('Failed to fetch quotations:', error)
  }
}

const fetchFees = async () => {
  loading.value = true
  try {
    // 获取所有报价单的费用
    const feesData = []
    for (const q of quotations.value) {
      try {
        const res = await feesAPI.getByQuotation(q.id)
        const fees = Array.isArray(res) ? res : (res.items || [])
        fees.forEach(f => {
          feesData.push({
            ...f,
            quotation_id: q.id,
            project_name: q.project_name,
            project_no: q.project_no
          })
        })
      } catch (e) {
        // 忽略单个报价单费用获取失败
      }
    }
    allFees.value = feesData

    // 默认展开第一个分组
    if (groupedFees.value.length > 0 && !expandedGroups.value[groupedFees.value[0].quotation_id]) {
      expandedGroups.value[groupedFees.value[0].quotation_id] = true
    }
  } catch (error) {
    console.error('Failed to fetch fees:', error)
    ElMessage.error('获取费用数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchQuotations().then(() => {
    fetchFees()
  })
})
</script>

<style scoped>
.fees-page {
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

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.stat-card {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  border: 1px solid var(--color-border-light);
  transition: all 0.2s;
}

.stat-card.highlight {
  background: linear-gradient(135deg, #0D9488 0%, #14B8A6 100%);
}

.stat-card.highlight .stat-label,
.stat-card.highlight .stat-value {
  color: white;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.stat-icon.factory { background: #CCFBF1; }
.stat-icon.outside { background: #DBEAFE; }
.stat-icon.total { background: rgba(255, 255, 255, 0.2); }

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  font-size: 13px;
  color: var(--color-text-secondary);
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
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
  min-width: 160px;
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

.btn-secondary {
  background: var(--color-bg-card);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border-light);
}

/* 项目分组 */
.quotation-groups {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  overflow-y: auto;
  min-height: 0;
}

.quotation-group {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  overflow: hidden;
}

.group-content {
  overflow: hidden;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  cursor: pointer;
  background: var(--color-bg-page);
  transition: background 0.2s;
}

.group-header:hover {
  background: #F0FDFA;
}

.group-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.expand-icon {
  font-size: 12px;
  color: var(--color-text-secondary);
  width: 16px;
}

.project-name {
  font-weight: 600;
  color: var(--color-text-primary);
}

.project-no {
  font-size: 13px;
  color: var(--color-text-secondary);
  padding: 2px 8px;
  background: var(--color-bg-page);
  border-radius: 4px;
}

.group-stats {
  display: flex;
  gap: 20px;
}

.stat-item {
  font-size: 14px;
  font-weight: 500;
}

.stat-item.internal { color: #0D9488; }
.stat-item.external { color: #3B82F6; }
.stat-item.total { color: var(--color-text-primary); font-weight: 600; }

.group-content {
  padding: 0;
}

.fee-table {
  width: 100%;
  border-top: 1px solid var(--color-border-light);
}

.fee-type-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.fee-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.fee-badge.internal {
  background: #CCFBF1;
  color: #0D9488;
}

.fee-badge.external {
  background: #DBEAFE;
  color: #3B82F6;
}

.amount {
  font-weight: 600;
  color: var(--color-text-primary);
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
}

.empty-icon {
  font-size: 48px;
  display: block;
  margin-bottom: 16px;
}

.empty-state p {
  color: var(--color-text-secondary);
  font-size: 14px;
  margin: 0;
}
</style>
