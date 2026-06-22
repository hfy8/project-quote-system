<template>
  <div class="my-assignments">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>我的分配</span>
          <el-radio-group v-model="filterType" size="small">
            <el-radio-button value="">全部</el-radio-button>
            <el-radio-button value="project">项目</el-radio-button>
            <el-radio-button value="agency">机构</el-radio-button>
            <el-radio-button value="electrical">电气</el-radio-button>
          </el-radio-group>
        </div>
      </template>

      <el-table
        :data="filteredAssignments"
        v-loading="loading"
        stripe
        style="width: 100%;"
        max-height="100%"
      >
        <el-table-column prop="quotation_name" label="报价单名称" min-width="180" />
        <el-table-column prop="quotation_scheme_no" label="方案号" width="150" />
        <el-table-column label="参与类型" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getTypeTag(row.participant_type)" size="small">
              {{ getTypeLabel(row.participant_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="business_owner_name" label="业务负责人" width="100" />
        <el-table-column prop="module_count" label="模块数" width="80" align="center" />
        <el-table-column prop="material_count" label="物料数" width="80" align="center" />
        <el-table-column label="报价单状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTag(row.quotation_status)" size="small">
              {{ formatStatus(row.quotation_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="160">
          <template #default="{ row }">
            {{ row.created_at ? formatDate(row.created_at) : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewQuotation(row)">
              查看
            </el-button>
          </template>
        </el-table-column>
        <template #empty>
          <el-empty description="您还没有被分配的报价单" />
        </template>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper" v-if="pagination.total > pagination.pageSize">
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
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '@/api/request'

const router = useRouter()
const assignments = ref([])
const loading = ref(false)
const filterType = ref('')
const pagination = ref({ page: 1, pageSize: 20, total: 0 })

const filteredAssignments = computed(() => {
  if (!filterType.value) return assignments.value
  return assignments.value.filter(a => a.participant_type === filterType.value)
})

function getStatusTag(status) {
  const map = { draft: 'info', submitted: 'warning', approved: 'success', archived: 'success', cancelled: 'danger', rejected: 'danger' }
  return map[status] || 'info'
}

function formatStatus(status) {
  const map = { draft: '草稿', submitted: '待审核', approved: '已归档', archived: '已归档', cancelled: '已取消', rejected: '已驳回' }
  return map[status] || status
}

function getTypeLabel(type) {
  return typeNameMap.value[type] || type
}

function getTypeTag(type) {
  const map = { project: '', agency: 'warning', electrical: 'danger', enginee: 'success' }
  return map[type] || 'info'
}

const typeNameMap = ref({})

async function loadParticipantTypes() {
  try {
    const res = await request.get('/participant-type-permissions')
    const list = res || []
    const m = {}
    for (const p of list) {
      if (p.type_name && !m[p.participant_type]) {
        m[p.participant_type] = p.type_name
      }
    }
    typeNameMap.value = m
  } catch (e) {
    console.error('加载参与类型失败', e)
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return d.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

function viewQuotation(row) {
  router.push(`/my-assignments/quotations/${row.quotation_id}/view`)
}

const handleSizeChange = (size) => {
  pagination.value.pageSize = size
  pagination.value.page = 1
  fetchAssignments()
}

const handlePageChange = (page) => {
  pagination.value.page = page
  fetchAssignments()
}

async function fetchAssignments() {
  loading.value = true
  try {
    const res = await request.get('/quotations/my-assignments', {
      params: { page: pagination.value.page, page_size: pagination.value.pageSize }
    })
    assignments.value = res.items || res.data || res || []
    pagination.value.total = res.total || assignments.value.length
  } catch (error) {
    console.error('获取分配失败:', error)
    assignments.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadParticipantTypes()
  fetchAssignments()
})
</script>

<style scoped>
.my-assignments {
  padding: 16px;
  height: calc(100vh - 60px);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.my-assignments :deep(.el-card) {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.my-assignments :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 16px;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination-wrapper {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
</style>
