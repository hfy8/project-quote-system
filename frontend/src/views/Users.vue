<template>
  <div class="users-page">
    <!-- 页面标题栏 -->
    <div class="page-header-bar">
      <div class="header-left">
        <h1 class="page-title">用户管理</h1>
        <span class="page-desc">共 {{ pagination.total }} 个用户</span>
      </div>
      <button class="btn btn-primary" :disabled="!canAddUser" @click="handleAdd">
        <span>+</span> 新增用户
      </button>
    </div>

    <!-- 搜索筛选区 -->
    <div class="filter-bar card">
      <div class="search-group">
        <el-input
          v-model="filters.keyword"
          placeholder="搜索姓名或工号"
          clearable
          @clear="handleSearch"
          @keyup.enter="handleSearch"
          class="search-input"
        >
          <template #prefix>
            <span class="search-icon">🔍</span>
          </template>
        </el-input>
        <button class="btn-search" @click="handleSearch">搜索</button>
      </div>
      <div class="role-tabs">
        <button
          class="role-tab"
          :class="{ active: filters.role === '' }"
          @click="handleRoleChange('')"
        >
          全部
        </button>
        <button
          v-for="r in roleList"
          :key="r.code"
          class="role-tab"
          :class="{ active: filters.role === r.code }"
          @click="handleRoleChange(r.code)"
        >
          {{ r.name }}
        </button>
      </div>
    </div>

    <!-- 数据表格 -->
    <div class="table-container card" style="flex:1;overflow:hidden;">
    <el-table
        :data="tableData"
        v-loading="loading"
        stripe
        class="users-table"
        style="width: 100%; min-width: 800px;"
        height="calc(-200px + 100vh)"
      >
        <el-table-column prop="username" label="工号">
          <template #default="{ row }">
            <div class="user-info">
              <div class="user-avatar">{{ getAvatar(row.username) }}</div>
              <span class="username">{{ row.username }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="real_name" label="姓名">
          <template #default="{ row }">
            <span class="real-name">{{ row.real_name || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="dept_name" label="部门">
          <template #default="{ row }">
            <span class="dept-name">{{ row.dept_name || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="position_name" label="职位">
          <template #default="{ row }">
            <span class="position-name">{{ row.position_name || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="role" label="角色">
          <template #default="{ row }">
            <span class="role-badge" :class="row.role">
              {{ getRoleName(row.role) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态">
          <template #default="{ row }">
            <span class="status-badge" :class="row.is_active ? 'active' : 'inactive'">
              {{ row.is_active ? '在职' : '离职' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间">
          <template #default="{ row }">
            <span class="date-text">{{ formatDate(row.created_at) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default="{ row }">
            <div class="action-buttons">
              <button class="action-btn edit" :disabled="!canEditUser(row)" @click="handleEdit(row)">编辑</button>
              <button class="action-btn reset" :disabled="!canResetPassword(row)" @click="handleResetPassword(row)">重置</button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.page_size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="480px" class="user-dialog">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px" class="dialog-form">
        <el-form-item label="工号" prop="username">
          <el-input v-model="form.username" placeholder="请输入工号" :disabled="!!form.id" />
        </el-form-item>
        <el-form-item label="姓名" prop="real_name">
          <el-input v-model="form.real_name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" placeholder="请选择角色" style="width: 100%;">
            <el-option v-for="r in roleList" :key="r.code" :label="r.name" :value="r.code" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="!form.id" label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
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
import { ref, reactive, computed, onMounted } from 'vue'
import { usersAPI, rolesAPI } from '../api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '../stores/auth'
import { usePermission } from '../composables/usePermission'

const authStore = useAuthStore()
const { can: hasPermission } = usePermission()

// 是否有用户管理权限
const canManageUser = computed(() => hasPermission('user.edit'))

// 是否有新增用户权限
const canAddUser = computed(() => hasPermission('user.create'))

// 是否有编辑用户权限
const canEditUser = (row) => {
  // 不能编辑自己（admin用户）
  if (row.role === 'admin') return false
  return authStore.userInfo?.role === 'admin' || hasPermission('user.edit')
}

// 是否有重置密码权限
const canResetPassword = (row) => {
  // 不能重置admin密码
  if (row.role === 'admin') return false
  return authStore.userInfo?.role === 'admin' || hasPermission('user.reset_password')
}

const loading = ref(false)
const tableData = ref([])
const roleList = ref([])
const pagination = reactive({
  page: 1,
  page_size: 20,
  total: 0
})
const filters = reactive({
  keyword: '',
  role: ''
})

const dialogVisible = ref(false)
const dialogTitle = ref('新增用户')
const formRef = ref(null)

const form = reactive({
  id: null,
  username: '',
  real_name: '',
  role: 'business',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入工号', trigger: 'blur' }],
  real_name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

const roleOptions = [
  { value: 'admin', label: '管理员' },
  { value: 'business', label: '业务员' },
  { value: 'purchaser', label: '采购' },
  { value: 'viewer', label: '普通用户' }
]

const roleNames = {
  admin: '管理员',
  business: '业务员',
  purchaser: '采购',
  viewer: '普通用户'
}

const getRoleName = (role) => {
  const found = roleList.value.find(r => r.code === role)
  if (found) return found.name
  return roleNames[role] || role
}

const getAvatar = (username) => {
  return username ? username.slice(0, 1).toUpperCase() : '?'
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size
    }
    if (filters.keyword) params.keyword = filters.keyword
    if (filters.role) params.role = filters.role

    const res = await usersAPI.getList(params)
    tableData.value = res.items || []
    pagination.total = res.total || 0
  } catch (error) {
    console.error('Failed to fetch users:', error)
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const loadRoles = async () => {
  try {
    const res = await rolesAPI.getList({ page: 1, pageSize: 100 })
    roleList.value = res.items || res || []
  } catch (e) {
    console.error('加载角色失败', e)
  }
}

const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

const handleRoleChange = (role) => {
  filters.role = role
  pagination.page = 1
  fetchData()
}

const handlePageChange = (page) => {
  pagination.page = page
  fetchData()
}

const handleSizeChange = (size) => {
  pagination.page_size = size
  pagination.page = 1
  fetchData()
}

const handleAdd = () => {
  dialogTitle.value = '新增用户'
  Object.assign(form, { id: null, username: '', real_name: '', role: 'business', password: '' })
  dialogVisible.value = true
}

const handleEdit = (row) => {
  dialogTitle.value = '编辑用户'
  const { password, ...rest } = row
  Object.assign(form, rest)
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (form.id) {
          await usersAPI.update(form.id, form)
          ElMessage.success('更新成功')
        } else {
          await usersAPI.create(form)
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

const handleResetPassword = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要重置用户「${row.username}」的密码吗？`,
      '确认重置',
      { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
    )
    await usersAPI.resetPassword(row.id)
    ElMessage.success('密码已重置为默认密码: 123456')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

onMounted(async () => {
  await Promise.all([fetchData(), loadRoles()])
})
</script>

<style scoped>
.users-page {
  padding: var(--spacing-lg);
  height: 100vh;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  overflow: hidden;
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

/* 搜索筛选区 */
.filter-bar {
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
  flex-shrink: 0;
}

.search-group {
  display: flex;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.search-input {
  width: 300px;
}

.search-icon {
  font-size: 14px;
}

.btn-search {
  padding: 8px 16px;
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
}

.role-tabs {
  display: flex;
  gap: var(--spacing-xs);
  flex-wrap: wrap;
}

.role-tab {
  padding: 6px 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-full);
  background: white;
  cursor: pointer;
  font-size: 13px;
  color: var(--color-text-secondary);
  transition: all 0.2s;
}

.role-tab:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.role-tab.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}

/* 数据表格 */
.table-container {
  flex: 1;
  overflow: auto;
  display: flex;
  flex-direction: column;
}

.users-table {
  --el-table-border-color: var(--color-border-light);
  flex: 1;
}

.user-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--color-primary) 0%, #0F766E 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
}

.username {
  font-weight: 500;
  color: var(--color-text-primary);
}

.real-name, .dept-name, .position-name {
  font-size: 14px;
  color: var(--color-text-secondary);
}

.role-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: 12px;
  font-weight: 500;
}

.role-badge.admin { background: var(--color-danger-bg); color: var(--color-danger); }
.role-badge.manager { background: #FEF3C7; color: #D97706; }
.role-badge.business { background: var(--color-primary-light); color: var(--color-primary); }
.role-badge.purchaser { background: #DBEAFE; color: #2563EB; }
.role-badge.viewer { background: var(--color-info-bg); color: var(--color-info); }

.status-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-size: 12px;
}
.status-badge.active { background: #D1FAE5; color: #059669; }
.status-badge.inactive { background: #FEE2E2; color: #DC2626; }

.date-text {
  font-size: 13px;
  color: var(--color-text-secondary);
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  padding: var(--spacing-md);
  border-top: 1px solid var(--color-border-light);
  flex-shrink: 0;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: var(--spacing-xs);
}

.action-btn {
  padding: 4px 10px;
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

.action-btn.reset {
  color: var(--color-warning);
  background: var(--color-warning-bg);
}

.action-btn.reset:hover {
  background: var(--color-warning);
  color: white;
}

/* 弹窗样式 */
.user-dialog :deep(.el-dialog__header) {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--color-border-light);
}

.user-dialog :deep(.el-dialog__title) {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.user-dialog :deep(.el-dialog__body) {
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
  border: 1px solid var(--color-border);
  background: white;
  cursor: pointer;
}

.confirm-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--radius-md);
  border: none;
  background: var(--color-primary);
  color: white;
  cursor: pointer;
}

.confirm-btn:hover {
  background: var(--color-primary-hover);
}
</style>
