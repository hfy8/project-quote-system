<template>
  <el-dialog v-model="dialogVisible" title="版本对比" width="95%" top="3vh" destroy-on-close>
    <div class="version-compare">
      <!-- 版本选择区 -->
      <div class="version-select-section">
        <div class="section-header">
          <span class="section-title">📋 选择要对比的版本（选择2个）</span>
          <span class="selected-count">已选择：{{ selectedVersions.length }} / 2</span>
        </div>
        <el-table
          :data="versions"
          ref="versionTable"
          stripe
          max-height="250"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55" :selectable="checkSelectable" />
          <el-table-column prop="version_no" label="版本号" width="100" align="center">
            <template #default="{ row }">
              <span class="version-tag">v{{ row.version_no }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="operation_type" label="操作类型" width="120">
            <template #default="{ row }">
              {{ getOperationLabel(row.operation_type) }}
            </template>
          </el-table-column>
          <el-table-column prop="remark" label="备注" min-width="150" show-overflow-tooltip />
          <el-table-column prop="creator_name" label="创建人" width="120" />
          <el-table-column prop="created_at" label="创建时间" width="160">
            <template #default="{ row }">
              {{ formatDate(row.created_at) }}
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 对比按钮 -->
      <div class="compare-action">
        <el-button type="primary" size="large" @click="doCompare" :disabled="selectedVersions.length !== 2">
          🔍 开始对比
        </el-button>
      </div>

      <!-- 对比结果 -->
      <div v-if="showResult" class="compare-result" v-loading="loading">
        <!-- 汇总卡片 -->
        <div class="summary-cards">
          <div class="summary-item">
            <div class="summary-label">版本1</div>
            <div class="summary-value primary">V{{ selectedVersions[0]?.version_no }}</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">VS</div>
            <div class="summary-value accent">VS</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">版本2</div>
            <div class="summary-value primary">V{{ selectedVersions[1]?.version_no }}</div>
          </div>
        </div>

        <!-- 基本信息对比 -->
        <div class="compare-section">
          <h4 class="section-title">📋 基本信息对比</h4>
          <table class="compare-table">
            <thead>
              <tr>
                <th>字段</th>
                <th>V{{ selectedVersions[0]?.version_no }}</th>
                <th>V{{ selectedVersions[1]?.version_no }}</th>
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
        <div class="compare-section">
          <h4 class="section-title">📦 模块对比 <span class="count-badge">V1: {{ getModuleCount(data1) }} 个 | V2: {{ getModuleCount(data2) }} 个</span></h4>
          <table class="compare-table">
            <thead>
              <tr>
                <th>模块名称</th>
                <th>V{{ selectedVersions[0]?.version_no }}</th>
                <th>V{{ selectedVersions[1]?.version_no }}</th>
                <th>状态</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="moduleName in getAllModuleNames()" :key="moduleName">
                <tr :class="getModuleRowClass(moduleName)">
                  <td><strong>{{ moduleName }}</strong></td>
                  <td>{{ hasModule(data1, moduleName) ? '✓' : '-' }}</td>
                  <td>{{ hasModule(data2, moduleName) ? '✓' : '-' }}</td>
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
        <div class="compare-section">
          <h4 class="section-title">🏷️ 物料变化</h4>
          <table class="compare-table" v-if="getMaterialChanges().length > 0">
            <thead>
              <tr>
                <th>物料名称</th>
                <th>规格/品牌</th>
                <th>V1 数量×单价</th>
                <th>V2 数量×单价</th>
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
        <div class="compare-section">
          <h4 class="section-title">💰 费用变化</h4>
          <table class="compare-table" v-if="getFeeChanges().length > 0">
            <thead>
              <tr>
                <th>费用类型</th>
                <th>位置</th>
                <th>V1 金额</th>
                <th>V2 金额</th>
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
        <div class="compare-section">
          <h4 class="section-title">⏱️ 人力工时变化</h4>
          <table class="compare-table" v-if="getLaborChanges().length > 0">
            <thead>
              <tr>
                <th>工项名称</th>
                <th>V1 单价×工时</th>
                <th>V2 单价×工时</th>
                <th>变化</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="item in getLaborChanges()" :key="item.key">
                <tr :class="getLaborRowClass(item)">
                  <td>{{ item.name }}</td>
                  <td>{{ formatLaborCell(item, 1) }}</td>
                  <td>{{ formatLaborCell(item, 2) }}</td>
                  <td :class="item.changeClass">{{ item.changeText }}</td>
                </tr>
              </template>
            </tbody>
          </table>
          <el-empty v-else description="无人力工时变化" :image-size="60" />
        </div>

        <!-- 汇总 -->
        <div class="compare-section total-section">
          <h4 class="section-title">📊 费用汇总</h4>
          <div class="total-grid">
            <div class="total-item">
              <div class="total-label">物料小计</div>
              <div class="total-values">
                <span>V1: ¥{{ totals1?.material_total_with_rates?.toFixed(2) ?? '-' }}</span>
                <span class="vs">→</span>
                <span>V2: ¥{{ totals2?.material_total_with_rates?.toFixed(2) ?? '-' }}</span>
              </div>
            </div>
            <div class="total-item">
              <div class="total-label">其他费用</div>
              <div class="total-values">
                <span>V1: ¥{{ totals1?.fees_total?.toFixed(2) ?? '-' }}</span>
                <span class="vs">→</span>
                <span>V2: ¥{{ totals2?.fees_total?.toFixed(2) ?? '-' }}</span>
              </div>
            </div>
            <div class="total-item">
              <div class="total-label">人力工时</div>
              <div class="total-values">
                <span>V1: ¥{{ totals1?.labor_total?.toFixed(2) ?? '-' }}</span>
                <span class="vs">→</span>
                <span>V2: ¥{{ totals2?.labor_total?.toFixed(2) ?? '-' }}</span>
              </div>
            </div>
            <div class="total-item highlight">
              <div class="total-label">含税总计</div>
              <div class="total-values">
                <span>V1: ¥{{ totals1?.grand_total?.toFixed(2) ?? '-' }}</span>
                <span class="vs">→</span>
                <span>V2: ¥{{ totals2?.grand_total?.toFixed(2) ?? '-' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { versionsAPI } from '../api/versions'

const props = defineProps({
  visible: Boolean,
  versions: Array,
  quotationId: [String, Number]
})

const emit = defineEmits(['update:visible'])

const dialogVisible = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val)
})

const versionTable = ref(null)
const selectedVersions = ref([])
const data1 = ref(null)
const data2 = ref(null)
const totals1 = ref(null)
const totals2 = ref(null)
const loading = ref(false)
const showResult = ref(false)

// 限制只能选择2个
function checkSelectable(row) {
  return selectedVersions.value.length < 2 || selectedVersions.value.some(v => v.version_no === row.version_no)
}

function handleSelectionChange(selection) {
  // 保证只选中2个
  if (selection.length > 2) {
    const toUnselect = selection.slice(2)
    toUnselect.forEach(item => {
      versionTable.value?.toggleRowSelection(item, false)
    })
  }
  selectedVersions.value = selection.slice(0, 2)
}

async function doCompare() {
  if (selectedVersions.value.length !== 2) {
    ElMessage.warning('请选择2个版本进行对比')
    return
  }
  
  loading.value = true
  showResult.value = true
  
  try {
    // 确保v1.version_no < v2.version_no
    const sorted = [...selectedVersions.value].sort((a, b) => a.version_no - b.version_no)
    
    const result = await versionsAPI.compare(sorted[0].id, sorted[1].id)
    
    data1.value = parseSnapshotData(result.version1)
    data2.value = parseSnapshotData(result.version2)
    totals1.value = result.totals1
    totals2.value = result.totals2
  } catch (error) {
    ElMessage.error('加载对比数据失败')
    showResult.value = false
  } finally {
    loading.value = false
  }
}

function parseSnapshotData(data) {
  if (typeof data === 'string') {
    try {
      return JSON.parse(data)
    } catch {
      return data
    }
  }
  return data
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return d.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

function getOperationLabel(type) {
  const labels = { archive: '归档', rollback: '回退', change_approve: '变更审批', manual: '手动' }
  return labels[type] || type || '未知'
}

function formatType(type) {
  return type === 'single' ? '单项' : type === 'line' ? '线体' : type || '-'
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
  if (version === 1) {
    return item.q1 && item.p1 ? `${item.q1} × ¥${item.p1}` : '-'
  }
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

function formatLaborCell(item, version) {
  const t = version === 1 ? item.t1 : item.t2
  return t ? `¥${t.toFixed(2)}` : '-'
}

function getLaborRowClass(item) {
  return item.changeClass === 'cell-added' ? 'row-added' : item.changeClass === 'cell-removed' ? 'row-removed' : item.changeClass === 'cell-modified' ? 'row-modified' : ''
}

// 汇总
function getMaterialTotal(data) {
  if (!data?.modules) return '0.00'
  let total = 0
  for (const mod of data.modules) {
    if (mod.materials) {
      for (const mat of mod.materials) {
        total += parseFloat(mat.quantity || 0) * parseFloat(mat.unit_price || 0)
      }
    }
  }
  return total.toFixed(2)
}

function getFeeTotal(data) {
  if (!data?.fees) return '0.00'
  let total = 0
  for (const fee of data.fees) {
    total += parseFloat(fee.amount || 0)
  }
  return total.toFixed(2)
}

function getLaborTotal(data) {
  if (!data?.labor_hours) return '0.00'
  let total = 0
  for (const l of data.labor_hours) {
    total += parseFloat(l.total || 0)
  }
  return total.toFixed(2)
}

function getGrandTotal(data) {
  if (!data?.quotation) return '0.00'
  const subtotal = parseFloat(getMaterialTotal(data)) + parseFloat(getFeeTotal(data)) + parseFloat(getLaborTotal(data))
  const taxRate = parseFloat(data.quotation.tax_rate || 0)
  return (subtotal * (1 + taxRate)).toFixed(2)
}

watch(dialogVisible, (val) => {
  if (!val) {
    selectedVersions.value = []
    data1.value = null
    data2.value = null
    totals1.value = null
    totals2.value = null
    showResult.value = false
  }
})
</script>

<style scoped>
.version-compare {
  max-height: 80vh;
  overflow-y: auto;
}

.version-select-section {
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.section-title {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.selected-count {
  font-size: 13px;
  color: #909399;
}

.count-badge {
  font-size: 12px;
  font-weight: normal;
  color: #909399;
  margin-left: 10px;
}

.version-tag {
  display: inline-block;
  padding: 2px 8px;
  background: #409eff;
  color: white;
  border-radius: 4px;
  font-weight: 600;
}

.compare-action {
  text-align: center;
  padding: 15px 0;
  border-top: 1px solid #ebeef5;
  border-bottom: 1px solid #ebeef5;
  margin-bottom: 20px;
}

.compare-result {
  padding: 0 5px;
}

.summary-cards {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  margin-bottom: 20px;
}

.summary-item {
  text-align: center;
  color: white;
}

.summary-label {
  font-size: 13px;
  opacity: 0.9;
  margin-bottom: 5px;
}

.summary-value {
  font-size: 24px;
  font-weight: bold;
}

.summary-value.accent {
  background: rgba(255,255,255,0.2);
  padding: 5px 15px;
  border-radius: 20px;
}

.compare-section {
  margin-bottom: 25px;
}

.compare-section .section-title {
  padding-bottom: 8px;
  border-bottom: 2px solid #409eff;
  margin-bottom: 12px;
}

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

.row-added {
  background: #f0f9eb !important;
}

.row-removed {
  background: #fef0f0 !important;
}

.row-modified {
  background: #fdf6ec !important;
}

.cell-added {
  color: #67c23a;
  font-weight: 600;
}

.cell-removed {
  color: #f56c6c;
  font-weight: 600;
}

.cell-modified {
  color: #e6a23c;
  font-weight: 600;
}

.total-section {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 8px;
}

.total-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.total-item {
  padding: 15px;
  background: white;
  border-radius: 8px;
  text-align: center;
}

.total-item.highlight {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  color: white;
}

.total-label {
  font-size: 13px;
  margin-bottom: 8px;
  color: inherit;
  opacity: 0.9;
}

.total-values {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 600;
}

.total-values .vs {
  opacity: 0.5;
}
</style>
