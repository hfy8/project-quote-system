<template>
  <div class="exchange-rates-container">
    <div class="page-header">
      <h2>汇率配置</h2>
      <p class="subtitle">配置货币汇率，支持多币种转换</p>
    </div>

    <div class="card">
      <div class="card-header">
        <h3>汇率列表</h3>
        <el-button type="primary" @click="showAddDialog">添加汇率</el-button>
      </div>

      <el-table :data="exchangeRates" border v-loading="loading" height="calc(-200px + 100vh)">
        <el-table-column prop="currency" label="货币代码" width="120">
          <template #default="{ row }">
            <span class="currency-code">{{ row.currency }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="rate" label="汇率" width="120">
          <template #default="{ row }">
            <span class="rate-value">{{ row.rate }}</span>
          </template>
        </el-table-column>
        <el-table-column label="基准货币" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.is_base" type="success">是</el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" />
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button size="small" @click="editRate(row)">编辑</el-button>
              <el-button size="small" type="warning" @click="setAsBase(row)" :disabled="row.is_base">设为基准</el-button>
              <el-button size="small" type="danger" @click="deleteRate(row.id)">删除</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 货币转换工具 -->
    <div class="card convert-card">
      <div class="card-header">
        <h3>货币转换</h3>
      </div>
      <div class="convert-form">
        <el-input-number v-model="convertForm.amount" :min="0" :precision="2" placeholder="金额" />
        <el-select v-model="convertForm.from" placeholder="从" style="width: 100px;">
          <el-option v-for="r in exchangeRates" :key="r.currency" :label="r.currency" :value="r.currency" />
        </el-select>
        <span class="arrow">→</span>
        <el-select v-model="convertForm.to" placeholder="到" style="width: 100px;">
          <el-option v-for="r in exchangeRates" :key="r.currency" :label="r.currency" :value="r.currency" />
        </el-select>
        <el-button type="primary" @click="doConvert" :disabled="!convertForm.from || !convertForm.to">转换</el-button>
      </div>
      <div v-if="convertResult !== null" class="convert-result">
        <span class="result-amount">{{ convertForm.amount }} {{ convertForm.from }}</span>
        <span class="arrow">=</span>
        <span class="result-value">{{ convertResult }} {{ convertForm.to }}</span>
      </div>
    </div>

    <!-- 添加/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="货币代码" required>
          <el-input v-model="form.currency" placeholder="如：USD、EUR" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="汇率" required>
          <el-input-number v-model="form.rate" :min="0.0001" :precision="4" />
          <span class="form-hint">相对于基准货币的汇率</span>
        </el-form-item>
        <el-form-item label="设为基准货币">
          <el-switch v-model="form.is_base" />
          <span class="form-hint">基准货币汇率为1.0</span>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="2" placeholder="可选描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveRate">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { exchangeRatesAPI } from '@/api'

const loading = ref(false)
const exchangeRates = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('添加汇率')
const isEdit = ref(false)
const convertResult = ref(null)

const form = reactive({
  id: null,
  currency: '',
  rate: 1.0,
  is_base: false,
  description: ''
})

const convertForm = reactive({
  amount: 100,
  from: 'CNY',
  to: 'USD'
})

const fetchData = async () => {
  loading.value = true
  try {
    const res = await exchangeRatesAPI.getList()
    exchangeRates.value = Array.isArray(res) ? res : (res.items || [])
  } catch (error) {
    ElMessage.error('加载汇率失败')
  } finally {
    loading.value = false
  }
}

const showAddDialog = () => {
  isEdit.value = false
  dialogTitle.value = '添加汇率'
  form.id = null
  form.currency = ''
  form.rate = 1.0
  form.is_base = false
  form.description = ''
  dialogVisible.value = true
}

const editRate = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑汇率'
  form.id = row.id
  form.currency = row.currency
  form.rate = row.rate
  form.is_base = row.is_base
  form.description = row.description || ''
  dialogVisible.value = true
}

const saveRate = async () => {
  if (!form.currency) {
    ElMessage.warning('请输入货币代码')
    return
  }
  if (form.rate <= 0) {
    ElMessage.warning('汇率必须大于0')
    return
  }
  try {
    if (isEdit.value) {
      await exchangeRatesAPI.update(form.id, {
        rate: form.rate,
        is_base: form.is_base,
        description: form.description
      })
      ElMessage.success('更新成功')
    } else {
      await exchangeRatesAPI.create({
        currency: form.currency.toUpperCase(),
        rate: form.rate,
        is_base: form.is_base,
        description: form.description
      })
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const deleteRate = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除该汇率吗？', '提示', { type: 'warning' })
    await exchangeRatesAPI.deleteExchangeRate(id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const setAsBase = async (row) => {
  try {
    await exchangeRatesAPI.setBaseCurrency(row.id)
    ElMessage.success('已设为基准货币')
    fetchData()
  } catch (error) {
    ElMessage.error('设置失败')
  }
}

const doConvert = async () => {
  try {
    const res = await exchangeRatesAPI.convert(convertForm.from, convertForm.to, convertForm.amount)
    convertResult.value = res.result
  } catch (error) {
    ElMessage.error('转换失败')
  }
}

onMounted(fetchData)
</script>

<style scoped>
.exchange-rates-container {
  padding: var(--spacing-lg);
  height: 100vh;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.page-header {
  margin-bottom: var(--spacing-lg);
}

.page-header h2 {
  margin: 0 0 8px 0;
  color: var(--color-text-primary);
}

.subtitle {
  color: var(--color-text-secondary);
  margin: 0;
}

.card {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  border: 1px solid var(--color-border);
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.card-header h3 {
  margin: 0;
  color: var(--color-text-primary);
}

.currency-code {
  font-weight: 600;
  color: var(--color-primary);
}

.rate-value {
  font-weight: 600;
}

.convert-card {
  background: var(--color-primary-light);
  border-color: var(--color-primary);
}

.convert-form {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.arrow {
  color: var(--color-primary);
  font-size: 18px;
  font-weight: bold;
}

.convert-result {
  margin-top: var(--spacing-md);
  padding: var(--spacing-md);
  background: white;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 18px;
}

.result-amount {
  color: var(--color-text-secondary);
}

.result-value {
  color: var(--color-primary);
  font-weight: 600;
  font-size: 22px;
}

.form-hint {
  margin-left: 12px;
  color: var(--color-text-muted);
  font-size: 13px;
}

.action-buttons {
  display: flex;
  gap: 4px;
  flex-wrap: nowrap;
}
</style>
