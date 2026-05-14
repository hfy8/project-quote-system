<template>
  <div class="fee-rates-container">
    <div class="page-header">
      <h2>费用系数配置</h2>
      <p class="subtitle">配置大件、普通件、其他件的费用系数</p>
    </div>

    <div class="card">
      <div class="card-header">
        <h3>费用系数列表</h3>
        <el-button type="primary" @click="showAddDialog">添加系数</el-button>
      </div>

      <el-table :data="feeRates" border v-loading="loading" height="calc(-200px + 100vh)">
        <el-table-column prop="category" label="物料分类" width="150">
          <template #default="{ row }">
            <el-tag :type="getCategoryType(row.category)">{{ getCategoryLabel(row.category) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="rate" label="系数" width="120">
          <template #default="{ row }">
            <span class="rate-value">{{ row.rate }}x</span>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" />
        <el-table-column label="说明" width="200">
          <template #default="{ row }">
            <span class="rate-hint">
              物料价格 × {{ row.rate }} = 最终计入报价的金额
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button size="small" @click="editRate(row)">编辑</el-button>
              <el-button size="small" type="danger" @click="deleteRate(row.id)">删除</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 添加/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="物料分类" required>
          <el-select v-model="form.category" placeholder="请选择分类" :disabled="isEdit">
            <el-option label="大件" value="large" />
            <el-option label="普通件" value="standard" />
            <el-option label="其他件" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="费用系数" required>
          <el-input-number v-model="form.rate" :min="0.1" :max="10" :step="0.1" :precision="2" />
          <span class="form-hint">例如：1.1 表示价格乘以1.1倍</span>
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
import { feeRatesAPI } from '@/api'

const loading = ref(false)
const feeRates = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('添加费用系数')
const isEdit = ref(false)

const form = reactive({
  id: null,
  category: '',
  rate: 1.0,
  description: ''
})

const getCategoryType = (category) => {
  const types = { 'large': 'warning', 'standard': 'success', 'other': 'info' }
  return types[category] || ''
}

const getCategoryLabel = (cat) => {
  const map = { large: '大件', standard: '普通件', other: '其他件' }
  return map[cat] || cat || '-'
}

const fetchData = async () => {
  loading.value = true
  try {
    const res = await feeRatesAPI.getList()
    feeRates.value = Array.isArray(res) ? res : (res.items || [])
  } catch (error) {
    ElMessage.error('加载费用系数失败')
  } finally {
    loading.value = false
  }
}

const showAddDialog = () => {
  isEdit.value = false
  dialogTitle.value = '添加费用系数'
  form.id = null
  form.category = ''
  form.rate = 1.0
  form.description = ''
  dialogVisible.value = true
}

const editRate = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑费用系数'
  form.id = row.id
  form.category = row.category
  form.rate = row.rate
  form.description = row.description || ''
  dialogVisible.value = true
}

const saveRate = async () => {
  if (!form.category) {
    ElMessage.warning('请选择物料分类')
    return
  }
  if (form.rate <= 0) {
    ElMessage.warning('系数必须大于0')
    return
  }
  try {
    if (isEdit.value) {
      await feeRatesAPI.update(form.id, {
        rate: form.rate,
        description: form.description
      })
      ElMessage.success('更新成功')
    } else {
      await feeRatesAPI.create({
        category: form.category,
        rate: form.rate,
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
    await ElMessageBox.confirm('确定要删除该费用系数吗？', '提示', { type: 'warning' })
    await feeRatesAPI.delete(id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(fetchData)
</script>

<style scoped>
.fee-rates-container {
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

.rate-value {
  font-weight: 600;
  color: var(--color-primary);
  font-size: 16px;
}

.rate-hint {
  color: var(--color-text-muted);
  font-size: 13px;
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
