<template>
  <div class="roles-page">
    <!-- 页面标题栏 -->
    <div class="page-header-bar">
      <div class="header-left">
        <h1 class="page-title">角色管理</h1>
        <span class="page-desc">管理系统用户角色和权限</span>
      </div>
      <button class="btn btn-primary" @click="handleAdd">
        <span>+</span> 新增角色
      </button>
    </div>

    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="keyword"
        placeholder="搜索角色名称或代码..."
        clearable
        style="width: 300px;"
        @input="handleSearch"
      >
        <template #prefix>
          <span>🔍</span>
        </template>
      </el-input>
    </div>

    <!-- 角色卡片列表 -->
    <div v-loading="loading" class="roles-grid">
      <div
        v-for="item in tableData"
        :key="item.id"
        class="role-card"
      >
        <div class="role-card-header">
          <div class="role-icon">
            {{ item.name.charAt(0) }}
          </div>
          <div class="role-info">
            <h3 class="role-name">{{ item.name }}</h3>
            <span class="role-code">{{ item.code }}</span>
          </div>
          <div class="role-users">
            <span class="user-count">{{ item.user_count }}</span>
            <span class="user-label">用户</span>
          </div>
        </div>

        <div class="role-card-body">
          <p class="role-desc">{{ item.description || '暂无描述' }}</p>

          <div class="permissions-preview">
            <el-tag
              v-for="perm in item.permissions.slice(0, 3)"
              :key="perm"
              size="small"
              :type="perm === '*' ? 'danger' : 'info'"
            >
              {{ formatPermission(perm) }}
            </el-tag>
            <el-tag v-if="item.permissions.length > 3" size="small">
              +{{ item.permissions.length - 3 }}
            </el-tag>
          </div>
        </div>

        <div class="role-card-footer">
          <button class="action-btn edit" @click="handleEdit(item)">编辑</button>
          <button class="action-btn permission" @click="handlePermissions(item)">权限</button>
          <button class="action-btn delete" @click="handleDelete(item)">删除</button>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination-wrapper">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :total="pagination.total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>

    <!-- 新增/编辑角色弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px" class="role-dialog">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="角色代码" prop="code">
          <el-input v-model="form.code" placeholder="请输入角色代码，如 admin" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="dialogVisible = false">取消</button>
          <button class="confirm-btn" @click="handleSubmit">确定</button>
        </div>
      </template>
    </el-dialog>

    <!-- 权限配置弹窗 -->
    <el-dialog v-model="permDialogVisible" title="权限配置" width="700px" class="perm-dialog">
      <div class="permissions-panel">
        <el-tabs v-model="activePermTab">
          <el-tab-pane
            v-for="group in permissionGroups"
            :key="group.name"
            :label="group.name"
            :name="group.name"
          >
            <div class="perm-list">
              <el-checkbox
                v-for="perm in group.permissions"
                :key="perm.code"
                v-model="selectedPermissions"
                :label="perm.code"
                :disabled="form.permissions.includes('*')"
              >
                {{ perm.name }}
              </el-checkbox>
            </div>
          </el-tab-pane>
        </el-tabs>
        <div v-if="form.permissions.includes('*')" class="super-perm-hint">
          超级管理员拥有全部权限，无需勾选
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="permDialogVisible = false">取消</button>
          <button class="confirm-btn" @click="handlePermSubmit">确定</button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../api/request'

const loading = ref(false)
const tableData = ref([])
const keyword = ref('')
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

const dialogVisible = ref(false)
const permDialogVisible = ref(false)
const dialogTitle = ref('新增角色')
const formRef = ref(null)
const activePermTab = ref('报价单')
const selectedPermissions = ref([])

const form = reactive({
  id: null,
  name: '',
  code: '',
  description: '',
  permissions: []
})

const rules = {
  name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入角色代码', trigger: 'blur' }]
}

// 权限分组（与后端 ALL_PERMISSIONS 对齐）
const permissionGroups = ref([
  { name: '首页', permissions: [
    { code: 'dashboard.view', name: '查看首页' },
  ]},
  { name: '报价单', permissions: [
    { code: 'quotation.view', name: '查看报价单' },
    { code: 'quotation.create', name: '创建报价单' },
    { code: 'quotation.edit', name: '编辑报价单' },
    { code: 'quotation.delete', name: '删除报价单' },
    { code: 'quotation.export', name: '导出报价单' },
  ]},
  { name: '原材料', permissions: [
    { code: 'material.view', name: '查看物料' },
    { code: 'material.create', name: '创建物料' },
    { code: 'material.edit', name: '编辑物料' },
    { code: 'material.delete', name: '删除物料' },
    { code: 'material.import', name: '导入物料' },
  ]},
  { name: '费用类型', permissions: [
    { code: 'fee_type.view', name: '查看费用类型' },
    { code: 'fee_type.create', name: '创建费用类型' },
    { code: 'fee_type.edit', name: '编辑费用类型' },
    { code: 'fee_type.delete', name: '删除费用类型' },
  ]},
  { name: '费用系数', permissions: [
    { code: 'fee_rate.view', name: '查看系数' },
    { code: 'fee_rate.edit', name: '编辑系数' },
  ]},
  { name: '汇率', permissions: [
    { code: 'exchange_rate.view', name: '查看汇率' },
    { code: 'exchange_rate.edit', name: '编辑汇率' },
  ]},
  { name: '模块', permissions: [
    { code: 'module.view', name: '查看模块' },
    { code: 'module.create', name: '创建模块' },
    { code: 'module.edit', name: '编辑模块' },
    { code: 'module.delete', name: '删除模块' },
  ]},
  { name: '版本', permissions: [
    { code: 'version.view', name: '查看版本' },
    { code: 'version.create', name: '创建版本' },
    { code: 'version.edit', name: '编辑版本' },
  ]},
  { name: '用户', permissions: [
    { code: 'user.view', name: '查看用户' },
    { code: 'user.create', name: '创建用户' },
    { code: 'user.edit', name: '编辑用户' },
    { code: 'user.delete', name: '删除用户' },
    { code: 'user.reset_password', name: '重置密码' },
  ]},
  { name: '角色', permissions: [
    { code: 'role.view', name: '查看角色' },
    { code: 'role.create', name: '创建角色' },
    { code: 'role.edit', name: '编辑角色' },
    { code: 'role.delete', name: '删除角色' },
  ]},
  { name: '日志', permissions: [
    { code: 'log.view', name: '查看日志' },
  ]},
  { name: '系统', permissions: [
    { code: 'system.view', name: '查看设置' },
    { code: 'system.edit', name: '编辑设置' },
  ]},
  { name: '我的分配', permissions: [
    { code: 'module_assignment.view', name: '查看我的分配' },
    { code: 'module_assignment.edit', name: '编辑我的分配' },
  ]},
  { name: '参与人权限', permissions: [
    { code: 'participant_type_permission.view', name: '查看参与人权限' },
    { code: 'participant_type_permission.edit', name: '编辑参与人权限' },
  ]},
])

const formatPermission = (perm) => {
  if (perm === '*') return '全部权限'
  for (const group of permissionGroups.value) {
    const found = group.permissions.find(p => p.code === perm)
    if (found) return found.name
  }
  return perm
}

const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      pageSize: pagination.pageSize
    }
    if (keyword.value) params.keyword = keyword.value

    const res = await request.get('/roles', { params })
    tableData.value = res.items || res || []
    pagination.total = res.total || tableData.value.length
  } catch (error) {
    console.error('Failed to fetch roles:', error)
    ElMessage.error('获取角色列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

const handleSizeChange = (size) => {
  pagination.pageSize = size
  pagination.page = 1
  fetchData()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchData()
}

const handleAdd = () => {
  dialogTitle.value = '新增角色'
  Object.assign(form, { id: null, name: '', code: '', description: '', permissions: [] })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑角色'
  Object.assign(form, { ...row })
  dialogVisible.value = true
}

const handlePermissions = (row) => {
  Object.assign(form, { ...row })
  selectedPermissions.value = [...(row.permissions || [])]
  permDialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (form.id) {
          await request.put(`/roles/${form.id}`, form)
          ElMessage.success('更新成功')
        } else {
          await request.post('/roles', form)
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

const handlePermSubmit = async () => {
  try {
    form.permissions = selectedPermissions.value
    await request.put(`/roles/${form.id}`, { permissions: form.permissions })
    ElMessage.success('权限更新成功')
    permDialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error('权限更新失败')
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除角色「${row.name}」吗？`,
      '确认删除',
      { confirmButtonText: '删除', cancelButtonText: '取消', type: 'warning' }
    )
    await request.delete(`/roles/${row.id}`)
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
.roles-page {
  padding: var(--spacing-lg);
}

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

.search-bar {
  margin-bottom: var(--spacing-lg);
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

.roles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.role-card {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  overflow: hidden;
  transition: all var(--transition-fast);
}

.role-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.role-card-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--color-border-light);
}

.role-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-hover));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 600;
}

.role-info {
  flex: 1;
}

.role-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 2px;
}

.role-code {
  font-size: 13px;
  color: var(--color-text-muted);
}

.role-users {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-bg-hover);
  border-radius: var(--radius-md);
}

.user-count {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-primary);
}

.user-label {
  font-size: 12px;
  color: var(--color-text-muted);
}

.role-card-body {
  padding: var(--spacing-lg);
}

.role-desc {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-md);
  line-height: 1.5;
}

.permissions-preview {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
}

.role-card-footer {
  display: flex;
  gap: var(--spacing-xs);
  padding: var(--spacing-md) var(--spacing-lg);
  background: var(--color-bg-hover);
  border-top: 1px solid var(--color-border-light);
}

.action-btn {
  flex: 1;
  padding: 6px 12px;
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

.action-btn.permission {
  color: var(--color-warning);
  background: var(--color-warning-bg);
}

.action-btn.permission:hover {
  background: var(--color-warning);
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

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  padding: var(--spacing-md) 0;
}

.role-dialog :deep(.el-dialog__header) {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--color-border-light);
}

.role-dialog :deep(.el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.role-dialog :deep(.el-dialog__body) {
  padding: var(--spacing-lg);
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

.perm-dialog :deep(.el-dialog__body) {
  padding: 0;
}

.permissions-panel {
  position: relative;
}

.perm-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-sm);
  padding: var(--spacing-lg);
}

.super-perm-hint {
  position: absolute;
  bottom: var(--spacing-lg);
  left: 50%;
  transform: translateX(-50%);
  padding: var(--spacing-sm) var(--spacing-lg);
  background: var(--color-danger-bg);
  color: var(--color-danger);
  border-radius: var(--radius-full);
  font-size: 13px;
}

@media (max-width: 768px) {
  .roles-grid {
    grid-template-columns: 1fr;
  }

  .perm-list {
    grid-template-columns: 1fr;
  }
}
</style>
