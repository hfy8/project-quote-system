<template>
  <div class="version-compare-page">
    <!-- 页面标题栏 -->
    <div class="page-header-bar">
      <div class="header-left">
        <h1 class="page-title">版本对比</h1>
        <span class="page-desc">对比报价单不同版本的差异</span>
      </div>
      <div class="header-right">
        <!-- 导出按钮组 -->
        <el-dropdown @command="handleExport" trigger="click">
          <el-button type="primary" :disabled="!selectedVersionNo">
            导出 <el-icon class="el-icon--right"><arrow-down /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="pdf">导出 PDF</el-dropdown-item>
              <el-dropdown-item command="word">导出 Word</el-dropdown-item>
              <el-dropdown-item command="excel">导出 Excel</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <!-- 版本选择区 -->
    <div class="version-select-section card">
      <div class="select-row">
        <div class="select-item">
          <label>版本 1（较旧）</label>
          <el-select v-model="v1Select" placeholder="选择版本" @change="onVersionSelect" filterable>
            <el-option
              v-for="v in versionOptions"
              :key="v.version_no"
              :label="`V${v.version_no} - ${formatDate(v.created_at)} - ${v.operator_name || v.creator_name || '未知'}`"
              :value="v.version_no"
              :disabled="v2Select && v.version_no >= v2Select"
            />
          </el-select>
        </div>
        <div class="vs-icon">VS</div>
        <div class="select-item">
          <label>版本 2（较新）</label>
          <el-select v-model="v2Select" placeholder="选择版本" @change="onVersionSelect" filterable>
            <el-option
              v-for="v in versionOptions"
              :key="v.version_no"
              :label="`V${v.version_no} - ${formatDate(v.created_at)} - ${v.operator_name || v.creator_name || '未知'}`"
              :value="v.version_no"
              :disabled="v1Select && v.version_no <= v1Select"
            />
          </el-select>
        </div>
        <div class="compare-btn-wrap">
          <el-button type="primary" size="default" @click="doCompare" :disabled="!v1Select || !v2Select">
            对比
          </el-button>
        </div>
      </div>
    </div>

    <!-- 加载状态 - 骨架屏 -->
    <div v-if="loading" class="compare-result" v-loading="loading" element-loading-text="加载对比数据...">
      <div class="skeleton-cards">
        <div class="skeleton-card" v-for="i in 4" :key="i"></div>
      </div>
    </div>

    <!-- 对比结果 -->
    <div v-else-if="compareData" class="compare-result">
      <!-- 变更汇总卡片 -->
      <div class="summary-cards">
        <div class="summary-card" :class="totalChangeClass('grand_total')">
          <div class="card-label">含税总计</div>
          <div class="card-values">
            <span class="v1">¥{{ totals1?.grand_total?.toFixed(2) ?? '-' }}</span>
            <span class="arrow">→</span>
            <span class="v2">¥{{ totals2?.grand_total?.toFixed(2) ?? '-' }}</span>
          </div>
          <div class="card-change" :class="totalChangeClass('grand_total')">
            {{ formatTotalChange('grand_total') }}
          </div>
        </div>
        <div class="summary-card" :class="totalChangeClass('material_total')">
          <div class="card-label">物料合计</div>
          <div class="card-values">
            <span class="v1">¥{{ totals1?.material_total?.toFixed(2) ?? '-' }}</span>
            <span class="arrow">→</span>
            <span class="v2">¥{{ totals2?.material_total?.toFixed(2) ?? '-' }}</span>
          </div>
          <div class="card-change" :class="totalChangeClass('material_total')">
            {{ formatTotalChange('material_total') }}
          </div>
        </div>
        <div class="summary-card" :class="totalChangeClass('fee_total')">
          <div class="card-label">其他费用</div>
          <div class="card-values">
            <span class="v1">¥{{ totals1?.fee_total?.toFixed(2) ?? '-' }}</span>
            <span class="arrow">→</span>
            <span class="v2">¥{{ totals2?.fee_total?.toFixed(2) ?? '-' }}</span>
          </div>
          <div class="card-change" :class="totalChangeClass('fee_total')">
            {{ formatTotalChange('fee_total') }}
          </div>
        </div>
        <div class="summary-card" :class="totalChangeClass('labor_total')">
          <div class="card-label">人力工时</div>
          <div class="card-values">
            <span class="v1">¥{{ totals1?.labor_total?.toFixed(2) ?? '-' }}</span>
            <span class="arrow">→</span>
            <span class="v2">¥{{ totals2?.labor_total?.toFixed(2) ?? '-' }}</span>
          </div>
          <div class="card-change" :class="totalChangeClass('labor_total')">
            {{ formatTotalChange('labor_total') }}
          </div>
        </div>
      </div>

      <!-- 版本信息 -->
      <div class="version-info-bar">
        <span class="info-item"><strong>V{{ v1Select }}</strong> 创建于 {{ formatDate(compareData.created_at1) }}，操作人：{{ compareData.operator_name1 || '-' }}</span>
        <span class="vs-tag">对比</span>
        <span class="info-item"><strong>V{{ v2Select }}</strong> 创建于 {{ formatDate(compareData.created_at2) }}，操作人：{{ compareData.operator_name2 || '-' }}</span>
      </div>

      <!-- 基本信息对比 -->
      <div class="compare-section card">
        <h4 class="section-title">📋 基本信息对比</h4>
        <table class="compare-table">
          <thead>
            <tr>
              <th>字段</th>
              <th>V{{ v1Select }}</th>
              <th>V{{ v2Select }}</th>
              <th>变化</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>报价单名称</td>
              <td>{{ data1?.quotation?.name || '-' }}</td>
              <td>{{ data2?.quotation?.name || '-' }}</td>
              <td :class="getCellClass(data1?.quotation?.name, data2?.quotation?.name)">
                {{ getChangeText(data1?.quotation?.name, data2?.quotation?.name) }}
              </td>
            </tr>
            <tr>
              <td>项目类型</td>
              <td>{{ formatType(data1?.quotation?.type) }}</td>
              <td>{{ formatType(data2?.quotation?.type) }}</td>
              <td :class="getCellClass(data1?.quotation?.type, data2?.quotation?.type)">
                {{ getChangeText(data1?.quotation?.type, data2?.quotation?.type) }}
              </td>
            </tr>
            <tr>
              <td>税率</td>
              <td>{{ data1?.quotation?.tax_rate !== undefined ? (data1.quotation.tax_rate * 100).toFixed(1) + '%' : '-' }}</td>
              <td>{{ data2?.quotation?.tax_rate !== undefined ? (data2.quotation.tax_rate * 100).toFixed(1) + '%' : '-' }}</td>
              <td :class="getCellClass(data1?.quotation?.tax_rate, data2?.quotation?.tax_rate)">
                {{ getChangeText(data1?.quotation?.tax_rate, data2?.quotation?.tax_rate) }}
              </td>
            </tr>
            <tr>
              <td>业务负责人</td>
              <td>{{ data1?.quotation?.business_owner_name || '-' }}</td>
              <td>{{ data2?.quotation?.business_owner_name || '-' }}</td>
              <td :class="getCellClass(data1?.quotation?.business_owner_name, data2?.quotation?.business_owner_name)">
                {{ getChangeText(data1?.quotation?.business_owner_name, data2?.quotation?.business_owner_name) }}
              </td>
            </tr>
            <tr>
              <td>大件系数</td>
              <td>{{ data1?.quotation?.coefficients?.large ?? '-' }}</td>
              <td>{{ data2?.quotation?.coefficients?.large ?? '-' }}</td>
              <td :class="getCellClass(data1?.quotation?.coefficients?.large, data2?.quotation?.coefficients?.large)">
                {{ getChangeText(data1?.quotation?.coefficients?.large, data2?.quotation?.coefficients?.large) }}
              </td>
            </tr>
            <tr>
              <td>普通件系数</td>
              <td>{{ data1?.quotation?.coefficients?.standard ?? '-' }}</td>
              <td>{{ data2?.quotation?.coefficients?.standard ?? '-' }}</td>
              <td :class="getCellClass(data1?.quotation?.coefficients?.standard, data2?.quotation?.coefficients?.standard)">
                {{ getChangeText(data1?.quotation?.coefficients?.standard, data2?.quotation?.coefficients?.standard) }}
              </td>
            </tr>
            <tr>
              <td>其他件系数</td>
              <td>{{ data1?.quotation?.coefficients?.other ?? '-' }}</td>
              <td>{{ data2?.quotation?.coefficients?.other ?? '-' }}</td>
              <td :class="getCellClass(data1?.quotation?.coefficients?.other, data2?.quotation?.coefficients?.other)">
                {{ getChangeText(data1?.quotation?.coefficients?.other, data2?.quotation?.coefficients?.other) }}
              </td>
            </tr>
            <tr>
              <td>对外利润率</td>
              <td>{{ data1?.quotation?.profit_rate !== undefined ? (data1.quotation.profit_rate * 100).toFixed(1) + '%' : '-' }}</td>
              <td>{{ data2?.quotation?.profit_rate !== undefined ? (data2.quotation.profit_rate * 100).toFixed(1) + '%' : '-' }}</td>
              <td :class="getCellClass(data1?.quotation?.profit_rate, data2?.quotation?.profit_rate)">
                {{ getChangeText(data1?.quotation?.profit_rate, data2?.quotation?.profit_rate) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 模块变化 -->
      <div class="compare-section card">
        <h4 class="section-title">📦 模块变化 <span class="count-badge">V{{ v1Select }}: {{ getModuleCount(data1) }} 个 | V{{ v2Select }}: {{ getModuleCount(data2) }} 个</span></h4>
        <table class="compare-table">
          <thead>
            <tr>
              <th>模块名称</th>
              <th>V{{ v1Select }}</th>
              <th>V{{ v2Select }}</th>
              <th>状态</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="moduleName in getAllModuleNames()" :key="moduleName">
              <tr :class="getModuleRowClass(moduleName)">
                <td><strong>{{ moduleName }}</strong></td>
                <td>{{ hasModule(data1, moduleName) ? '✓ 存在' : '-' }}</td>
                <td>{{ hasModule(data2, moduleName) ? '✓ 存在' : '-' }}</td>
                <td>
                  <el-tag v-if="isModuleAdded(moduleName)" type="success" size="small">新增</el-tag>
                  <el-tag v-else-if="isModuleRemoved(moduleName)" type="danger" size="small">删除</el-tag>
                  <el-tag v-else type="info" size="small">不变</el-tag>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>

      <!-- 物料变化 -->
      <div class="compare-section card">
        <h4 class="section-title">🏷️ 物料变化 <span class="count-badge" v-if="getMaterialChanges().length > 0">{{ getMaterialChanges().length }} 项</span></h4>
        <table class="compare-table" v-if="getMaterialChanges().length > 0">
          <thead>
            <tr>
              <th>物料名称</th>
              <th>规格/品牌</th>
              <th>V{{ v1Select }} 数量×单价</th>
              <th>V{{ v2Select }} 数量×单价</th>
              <th>变化</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="item in getMaterialChanges()" :key="item.key">
              <tr :class="getMaterialRowClass(item)">
                <td>{{ item.name }}</td>
                <td>{{ item.spec }}/{{ item.brand }}</td>
                <td>{{ formatMaterialCell(item, 1) }}</td>
                <td>{{ formatMaterialCell(item, 2) }}</td>
                <td :class="item.changeClass">{{ item.changeText }}</td>
              </tr>
            </template>
          </tbody>
        </table>
        <el-empty v-else description="无物料变化" :image-size="60" />
      </div>

      <!-- 费用变化 -->
      <div class="compare-section card">
        <h4 class="section-title">💰 费用变化 <span class="count-badge" v-if="getFeeChanges().length > 0">{{ getFeeChanges().length }} 项</span></h4>
        <table class="compare-table" v-if="getFeeChanges().length > 0">
          <thead>
            <tr>
              <th>费用类型</th>
              <th>位置</th>
              <th>V{{ v1Select }} 金额</th>
              <th>V{{ v2Select }} 金额</th>
              <th>变化</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="fee in getFeeChanges()" :key="fee.key">
              <tr :class="getFeeRowClass(fee)">
                <td>{{ fee.type }}</td>
                <td>{{ fee.location }}</td>
                <td>¥{{ fee.v1?.toFixed(2) || '-' }}</td>
                <td>¥{{ fee.v2?.toFixed(2) || '-' }}</td>
                <td :class="fee.changeClass">{{ fee.changeText }}</td>
              </tr>
            </template>
          </tbody>
        </table>
        <el-empty v-else description="无费用变化" :image-size="60" />
      </div>

      <!-- 人力工时变化 -->
      <div class="compare-section card">
        <h4 class="section-title">⏱️ 人力工时变化 <span class="count-badge" v-if="getLaborChanges().length > 0">{{ getLaborChanges().length }} 项</span></h4>
        <table class="compare-table" v-if="getLaborChanges().length > 0">
          <thead>
            <tr>
              <th>工项名称</th>
              <th>V{{ v1Select }} 金额</th>
              <th>V{{ v2Select }} 金额</th>
              <th>变化</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="item in getLaborChanges()" :key="item.key">
              <tr :class="getLaborRowClass(item)">
                <td>{{ item.name }}</td>
                <td>¥{{ item.t1?.toFixed(2) || '-' }}</td>
                <td>¥{{ item.t2?.toFixed(2) || '-' }}</td>
                <td :class="item.changeClass">{{ item.changeText }}</td>
              </tr>
            </template>
          </tbody>
        </table>
        <el-empty v-else description="无人力工时变化" :image-size="60" />
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state card">
      <el-empty description="请选择两个版本进行对比" :image-size="100" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowDown } from '@element-plus/icons-vue'
import request from '../utils/request'

const route = useRoute()
const quotationId = computed(() => route.params.id)

// 版本选择
const versionOptions = ref([])
const v1Select = ref(null)
const v2Select = ref(null)

// 对比数据
const loading = ref(false)
const compareData = ref(null)
const data1 = ref(null)
const data2 = ref(null)
const totals1 = ref(null)
const totals2 = ref(null)
const selectedVersionNo = ref(null)

// 加载版本列表
async function loadVersions() {
  try {
    const res = await request.get(`/quotations/${quotationId.value}/versions`)
    versionOptions.value = res || []
    // 默认选中最后两个版本
    if (versionOptions.value.length >= 2) {
      const sorted = [...versionOptions.value].sort((a, b) => a.version_no - b.version_no)
      v1Select.value = sorted[sorted.length - 2].version_no
      v2Select.value = sorted[sorted.length - 1].version_no
      await doCompare()
    }
  } catch (e) {
    ElMessage.error('加载版本列表失败')
  }
}

function onVersionSelect() {
  // 清除对比结果
  compareData.value = null
  data1.value = null
  data2.value = null
  totals1.value = null
  totals2.value = null
}

async function doCompare() {
  if (!v1Select.value || !v2Select.value) return
  if (v1Select.value === v2Select.value) {
    ElMessage.warning('请选择不同的版本')
    return
  }

  loading.value = true
  try {
    const res = await request.get(`/quotations/${quotationId.value}/versions/compare`, {
      params: { v1: v1Select.value, v2: v2Select.value }
    })
    compareData.value = res
    data1.value = parseSnapshotData(res.version1)
    data2.value = parseSnapshotData(res.version2)
    totals1.value = res.totals1
    totals2.value = res.totals2
    // 导出默认选 v2
    selectedVersionNo.value = v2Select.value
  } catch (e) {
    ElMessage.error('加载对比数据失败')
    compareData.value = null
  } finally {
    loading.value = false
  }
}

function parseSnapshotData(data) {
  if (typeof data === 'string') {
    try { return JSON.parse(data) } catch { return data }
  }
  return data
}

// 导出
function handleExport(format) {
  if (!selectedVersionNo.value) {
    ElMessage.warning('请选择要导出的版本')
    return
  }
  window.open(`/api/quotations/${quotationId.value}/versions/${selectedVersionNo.value}/export/${format}`, '_blank')
}

// 工具函数
function formatDate(dateStr) {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return d.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

function formatType(type) {
  return type === 'single' ? '单项' : type === 'line' ? '线体' : type || '-'
}

// 汇总卡片
function totalChangeClass(field) {
  const t1 = totals1.value?.[field] || 0
  const t2 = totals2.value?.[field] || 0
  if (t2 > t1) return 'diff-added'
  if (t2 < t1) return 'diff-removed'
  return ''
}

function formatTotalChange(field) {
  const t1 = totals1.value?.[field] || 0
  const t2 = totals2.value?.[field] || 0
  const diff = t2 - t1
  if (diff === 0) return '无变化'
  return (diff > 0 ? '+' : '') + '¥' + diff.toFixed(2)
}

// 比较相关
function getCellClass(v1, v2) {
  if (v1 === v2) return ''
  return v1 === undefined || v1 === null ? 'cell-added' :
         v2 === undefined || v2 === null ? 'cell-removed' : 'cell-modified'
}

function getChangeText(v1, v2) {
  if (v1 === v2) return '-'
  if (v1 === undefined || v1 === null) return `+ ${v2}`
  if (v2 === undefined || v2 === null) return `- ${v1}`
  return `${v1} → ${v2}`
}

// 模块相关
function getModuleCount(data) {
  return data?.modules?.length || 0
}

function getModuleNames(data) {
  if (!data?.modules) return new Set()
  return new Set(data.modules.map(m => m.name))
}

function getAllModuleNames() {
  const names1 = getModuleNames(data1.value)
  const names2 = getModuleNames(data2.value)
  return [...new Set([...names1, ...names2])]
}

function hasModule(data, name) {
  return getModuleNames(data).has(name)
}

function isModuleAdded(name) {
  return !hasModule(data1.value, name) && hasModule(data2.value, name)
}

function isModuleRemoved(name) {
  return hasModule(data1.value, name) && !hasModule(data2.value, name)
}

function getModuleRowClass(name) {
  if (isModuleAdded(name)) return 'row-added'
  if (isModuleRemoved(name)) return 'row-removed'
  return ''
}

// 物料相关
function getMaterialsMap(data) {
  const map = new Map()
  if (!data?.modules) return map
  for (const mod of data.modules) {
    if (mod.materials) {
      for (const mat of mod.materials) {
        const key = mat.material_id || mat.id
        map.set(key, { ...mat, moduleName: mod.name })
      }
    }
  }
  return map
}

function getMaterialChanges() {
  const changes = []
  const map1 = getMaterialsMap(data1.value)
  const map2 = getMaterialsMap(data2.value)
  const allKeys = new Set([...map1.keys(), ...map2.keys()])

  for (const key of allKeys) {
    const m1 = map1.get(key)
    const m2 = map2.get(key)
    const q1 = m1 ? parseFloat(m1.quantity || 0) : 0
    const q2 = m2 ? parseFloat(m2.quantity || 0) : 0
    const p1 = m1 ? parseFloat(m1.unit_price || 0) : 0
    const p2 = m2 ? parseFloat(m2.unit_price || 0) : 0

    if (!m1 && m2) {
      changes.push({ key, name: m2.material_name || m2.name, spec: m2.spec || '-', brand: m2.brand || '-', q1, q2, p1, p2, changeClass: 'cell-added', changeText: `新增: ${q2}×¥${p2}` })
    } else if (m1 && !m2) {
      changes.push({ key, name: m1.material_name || m1.name, spec: m1.spec || '-', brand: m1.brand || '-', q1, q2, p1, p2, changeClass: 'cell-removed', changeText: `删除: ${q1}×¥${p1}` })
    } else if (q1 !== q2 || p1 !== p2) {
      const qChange = q2 - q1
      const pChange = p2 - p1
      changes.push({ key, name: m2?.material_name || m1?.material_name, spec: (m2?.spec || m1?.spec) || '-', brand: (m2?.brand || m1?.brand) || '-', q1, q2, p1, p2, changeClass: 'cell-modified', changeText: `数量${qChange > 0 ? '+' : ''}${qChange}, 单价${pChange > 0 ? '+' : ''}¥${pChange.toFixed(2)}` })
    }
  }
  return changes
}

function formatMaterialCell(item, version) {
  if (version === 1) return item.q1 && item.p1 ? `${item.q1} × ¥${item.p1}` : '-'
  return item.q2 && item.p2 ? `${item.q2} × ¥${item.p2}` : '-'
}

function getMaterialRowClass(item) {
  return item.changeClass === 'cell-added' ? 'row-added' : item.changeClass === 'cell-removed' ? 'row-removed' : item.changeClass === 'cell-modified' ? 'row-modified' : ''
}

// 费用相关
function getFeesMap(data) {
  const map = new Map()
  if (!data?.fees) return map
  for (const fee of data.fees) {
    const key = `${fee.fee_type}_${fee.location}`
    map.set(key, fee)
  }
  return map
}

function getFeeChanges() {
  const changes = []
  const map1 = getFeesMap(data1.value)
  const map2 = getFeesMap(data2.value)
  const allKeys = new Set([...map1.keys(), ...map2.keys()])

  for (const key of allKeys) {
    const f1 = map1.get(key)
    const f2 = map2.get(key)
    const v1 = f1 ? parseFloat(f1.amount || 0) : 0
    const v2 = f2 ? parseFloat(f2.amount || 0) : 0

    if (!f1 && f2) {
      changes.push({ key, type: f2.fee_type, location: f2.location, v1, v2, changeClass: 'cell-added', changeText: `+ ¥${v2.toFixed(2)}` })
    } else if (f1 && !f2) {
      changes.push({ key, type: f1.fee_type, location: f1.location, v1, v2, changeClass: 'cell-removed', changeText: `- ¥${v1.toFixed(2)}` })
    } else if (v1 !== v2) {
      const change = v2 - v1
      changes.push({ key, type: f2?.fee_type || f1?.fee_type, location: f2?.location || f1?.location, v1, v2, changeClass: 'cell-modified', changeText: `${change > 0 ? '+' : ''}¥${change.toFixed(2)}` })
    }
  }
  return changes
}

function getFeeRowClass(fee) {
  return fee.changeClass === 'cell-added' ? 'row-added' : fee.changeClass === 'cell-removed' ? 'row-removed' : fee.changeClass === 'cell-modified' ? 'row-modified' : ''
}

// 人力工时相关
function getLaborChanges() {
  const changes = []
  const list1 = data1.value?.labor_hours || []
  const list2 = data2.value?.labor_hours || []
  const map1 = new Map(list1.map(l => [l.name, l]))
  const map2 = new Map(list2.map(l => [l.name, l]))
  const allNames = [...new Set([...map1.keys(), ...map2.keys()])]

  for (const name of allNames) {
    const l1 = map1.get(name)
    const l2 = map2.get(name)
    const t1 = l1 ? parseFloat(l1.total || 0) : 0
    const t2 = l2 ? parseFloat(l2.total || 0) : 0

    if (!l1 && l2) {
      changes.push({ key: name, name, t1, t2, changeClass: 'cell-added', changeText: `+ ¥${t2.toFixed(2)}` })
    } else if (l1 && !l2) {
      changes.push({ key: name, name, t1, t2, changeClass: 'cell-removed', changeText: `- ¥${t1.toFixed(2)}` })
    } else if (t1 !== t2) {
      const change = t2 - t1
      changes.push({ key: name, name, t1, t2, changeClass: 'cell-modified', changeText: `${change > 0 ? '+' : ''}¥${change.toFixed(2)}` })
    }
  }
  return changes
}

function getLaborRowClass(item) {
  return item.changeClass === 'cell-added' ? 'row-added' : item.changeClass === 'cell-removed' ? 'row-removed' : item.changeClass === 'cell-modified' ? 'row-modified' : ''
}

onMounted(() => {
  loadVersions()
})
</script>

<style scoped>
.version-compare-page {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

/* 头部 */
.page-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 0 5px;
}

.header-left {
  display: flex;
  align-items: baseline;
  gap: 12px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.page-desc {
  font-size: 13px;
  color: #909399;
}

.header-right {
  display: flex;
  gap: 10px;
  align-items: center;
}

/* 版本选择区 */
.version-select-section {
  padding: 20px;
  margin-bottom: 20px;
}

.select-row {
  display: flex;
  align-items: flex-end;
  gap: 16px;
  flex-wrap: wrap;
}

.select-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
  min-width: 200px;
}

.select-item label {
  font-size: 13px;
  font-weight: 600;
  color: #606266;
}

.vs-icon {
  font-size: 18px;
  font-weight: bold;
  color: #0D9488;
  padding: 0 10px 8px;
}

.compare-btn-wrap {
  padding-bottom: 0;
}

/* 骨架屏 */
.skeleton-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.skeleton-card {
  height: 100px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: 8px;
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* 汇总卡片 */
.summary-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.summary-card {
  background: white;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  transition: all 0.3s;
  border-top: 3px solid #e4e7ed;
}

.summary-card.diff-added {
  border-top-color: #0D9488;
  background: #f0f9f8;
}

.summary-card.diff-removed {
  border-top-color: #f56c6c;
  background: #fef0f0;
}

.card-label {
  font-size: 13px;
  color: #909399;
  margin-bottom: 10px;
}

.card-values {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 6px;
}

.card-values .v1 {
  color: #909399;
}

.card-values .v2 {
  color: #303133;
}

.card-values .arrow {
  color: #c0c4cc;
  font-size: 12px;
}

.card-change {
  font-size: 13px;
  font-weight: 600;
}

.diff-added .card-change { color: #0D9488; }
.diff-removed .card-change { color: #f56c6c; }

/* 版本信息栏 */
.version-info-bar {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px 16px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 13px;
  color: #606266;
}

.vs-tag {
  padding: 2px 12px;
  background: #0D9488;
  color: white;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

/* 对比区 */
.compare-result {
  padding: 0 5px;
}

.compare-section {
  margin-bottom: 20px;
  padding: 20px;
}

.section-title {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 15px 0;
  padding-bottom: 10px;
  border-bottom: 2px solid #0D9488;
}

.count-badge {
  font-size: 12px;
  font-weight: normal;
  color: #909399;
  margin-left: 8px;
}

/* 对比表格 */
.compare-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.compare-table th,
.compare-table td {
  padding: 10px 12px;
  border: 1px solid #ebeef5;
  text-align: left;
}

.compare-table th {
  background: #fafafa;
  font-weight: 600;
  color: #606266;
}

.compare-table tbody tr:hover {
  background: #f5f7fa;
}

/* 差异行 */
.row-added { background: #f0f9eb !important; }
.row-removed { background: #fef0f0 !important; }
.row-modified { background: #fdf6ec !important; }

/* 差异单元格 */
.cell-added { color: #0D9488; font-weight: 600; }
.cell-removed { color: #f56c6c; font-weight: 600; }
.cell-modified { color: #e6a23c; font-weight: 600; }

/* 空状态 */
.empty-state {
  padding: 60px 20px;
  text-align: center;
}

/* 卡片通用 */
.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  border: 1px solid #ebeef5;
}

/* 响应式 */
@media (max-width: 900px) {
  .summary-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  .select-row {
    flex-direction: column;
    align-items: stretch;
  }
  .vs-icon {
    text-align: center;
    padding: 0;
  }
}

@media (max-width: 600px) {
  .version-compare-page {
    padding: 10px;
  }
  .summary-cards {
    grid-template-columns: 1fr;
  }
}
</style>