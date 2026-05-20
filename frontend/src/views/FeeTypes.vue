<template>
  <div class="fee-types-page">
    <!-- 页面标题栏 -->
    <div class="page-header-bar">
      <div class="header-left">
        <h1 class="page-title">费用类型管理</h1>
        <span class="page-desc">共 {{ tableData.length }} 种费用类型</span>
      </div>
      <button class="btn btn-primary" @click="handleAdd">
        <span>+</span> 新增费用类型
      </button>
    </div>

    <!-- 费用类型卡片 -->
    <div class="fee-grid">
      <div
        v-for="item in tableData"
        :key="item.id"
        class="fee-card"
        :class="{ disabled: !item.is_active }"
      >
        <div class="fee-card-header">
          <div class="fee-icon" :class="item.location">
            {{ item.location === 'factory' ? '🏭' : '🌐' }}
          </div>
          <div class="fee-status" :class="{ active: item.is_active }">
            {{ item.is_active ? '启用' : '禁用' }}
          </div>
        </div>
        <div class="fee-card-body">
          <h3 class="fee-name">{{ item.name }}</h3>
          <p v-if="item.name_en" class="fee-name-en">{{ item.name_en }}</p>
          <p class="fee-desc">{{ item.description || '暂无描述' }}</p>
        </div>
        <div class="fee-card-footer">
          <div class="fee-location">
            <span class="location-label">{{ item.location === 'internal' ? '厂内' : '厂外' }}</span>
          </div>
          <div class="fee-actions">
            <button class="action-btn edit" @click="handleEdit(item)">编辑</button>
            <button class="action-btn delete" @click="handleDelete(item)">删除</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="520px" class="fee-dialog">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" class="dialog-form">
        <el-form-item label="费用名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入费用名称" />
        </el-form-item>
        <el-form-item label="英文名称">
          <el-input v-model="form.name_en" placeholder="English name (optional)" />
        </el-form-item>
        <el-form-item label="位置" prop="location">
          <el-select v-model="form.location" placeholder="请选择" style="width: 100%;">
            <el-option label="厂内" value="internal" />
            <el-option label="厂外" value="external" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="启用状态">
          <el-switch v-model="form.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="dialogVisible = false">取消</button>
          <button class="confirm-btn" @click="handleSubmit">确定</button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { feesAPI } from '../api'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const tableData = ref([
  { id: 1, name: '运输费', code: 'TRANSPORT', type: 'external', defaultAmount: 0, description: '厂外运输费用', enabled: true },
  { id: 2, name: '安装费', code: 'INSTALL', type: 'external', defaultAmount: 0, description: '现场安装费用', enabled: true },
  { id: 3, name: '调试费', code: 'DEBUG', type: 'internal', defaultAmount: 0, description: '设备调试费用', enabled: true },
  { id: 4, name: '培训费', code: 'TRAIN', type: 'external', defaultAmount: 0, description: '用户培训费用', enabled: true }
])

const dialogVisible = ref(false)
const dialogTitle = ref('新增费用类型')
const formRef = ref(null)

const form = reactive({
  id: null,
  name: '',
  name_en: '',
  location: 'internal',
  description: '',
  is_active: true
})

const rules = {
  name: [{ required: true, message: '请输入费用名称', trigger: 'blur' }],
  location: [{ required: true, message: '请选择位置', trigger: 'change' }]
}

const fetchData = async () => {
  loading.value = true
  try {
    const res = await feesAPI.getFeeTypes()
    tableData.value = Array.isArray(res) ? res : (res.items || [])
  } catch (error) {
    console.error('Failed to fetch fee types:', error)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  dialogTitle.value = '新增费用类型'
  Object.assign(form, { id: null, name: '', name_en: '', location: 'internal', description: '', is_active: true })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑费用类型'
  Object.assign(form, row)
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (form.id) {
          await feesAPI.updateFeeType(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await feesAPI.createFeeType(form)
          ElMessage.success('新增成功')
        }
        dialogVisible.value = false
        fetchData()
      } catch (error) {
        ElMessage.error('操作失败')
      }
    }
  })
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除费用类型「${row.name}」吗？删除后无法恢复。`,
      '确认删除',
      { confirmButtonText: '删除', cancelButtonText: '取消', type: 'warning' }
    )
    await feesAPI.deleteFeeType(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.fee-types-page {
  padding: var(--spacing-lg);
}

/* 页面标题栏 */
.page-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.header-left {
  display: flex;
  align-items: baseline;
  gap: var(--spacing-sm);
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.page-desc {
  font-size: 14px;
  color: var(--color-text-muted);
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  border: none;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
}

.btn-primary:hover {
  background: var(--color-primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

/* 费用卡片网格 */
.fee-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--spacing-md);
}

.fee-card {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  overflow: hidden;
  transition: all var(--transition-fast);
}

.fee-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.fee-card.disabled {
  opacity: 0.6;
}

.fee-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  border-bottom: 1px solid var(--color-border-light);
}

.fee-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
}

.fee-icon.factory {
  background: #CCFBF1;
}

.fee-icon.outside {
  background: #DBEAFE;
}

.fee-status {
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 500;
  background: var(--color-info-bg);
  color: var(--color-text-muted);
}

.fee-status.active {
  background: var(--color-success-bg);
  color: var(--color-success);
}

.fee-card-body {
  padding: var(--spacing-lg);
}

.fee-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
}

.fee-name-en {
  font-size: 13px;
  color: var(--color-text-muted);
  margin-bottom: var(--spacing-xs);
}

.fee-code {
  font-size: 13px;
  color: var(--color-text-muted);
  margin-bottom: var(--spacing-sm);
}

.fee-desc {
  font-size: 14px;
  color: var(--color-text-secondary);
  line-height: 1.5;
}

.fee-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) var(--spacing-lg);
  background: var(--color-bg-hover);
  border-top: 1px solid var(--color-border-light);
}

.fee-location {
  display: flex;
  flex-direction: column;
}

.location-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
}

.fee-actions {
  display: flex;
  gap: var(--spacing-xs);
}

.action-btn {
  padding: 4px 12px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  border: none;
  background: none;
}

.action-btn.edit {
  color: var(--color-primary);
  background: var(--color-primary-light);
}

.action-btn.edit:hover {
  background: var(--color-primary);
  color: white;
}

.action-btn.delete {
  color: var(--color-danger);
  background: var(--color-danger-bg);
}

.action-btn.delete:hover {
  background: var(--color-danger);
  color: white;
}

/* 弹窗样式 */
.fee-dialog :deep(.el-dialog__header) {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--color-border-light);
}

.fee-dialog :deep(.el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.fee-dialog :deep(.el-dialog__body) {
  padding: var(--spacing-lg);
}

.dialog-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--color-text-primary);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
  padding-top: var(--spacing-md);
}

.cancel-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--radius-md);
  font-size: 14px;
  background: var(--color-bg-card);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
  cursor: pointer;
}

.cancel-btn:hover {
  background: var(--color-bg-hover);
}

.confirm-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--radius-md);
  font-size: 14px;
  background: var(--color-primary);
  color: white;
  border: none;
  cursor: pointer;
}

.confirm-btn:hover {
  background: var(--color-primary-hover);
}

/* 响应式 */
@media (max-width: 768px) {
  .fee-grid {
    grid-template-columns: 1fr;
  }
}
</style>