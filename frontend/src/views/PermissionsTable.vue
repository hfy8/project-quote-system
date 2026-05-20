<template>
  <div class="permissions-table">
    <el-table :data="data" border stripe>
      <el-table-column prop="tab_label" label="Tab名称" width="140" />
      <el-table-column prop="tab_name" label="Tab标识" width="140">
        <template #default="{ row }">
          <code>{{ row.tab_name }}</code>
        </template>
      </el-table-column>
      <el-table-column label="启用" width="80" align="center">
        <template #default="{ row }">
          <el-switch
            :model-value="!row.is_disabled"
            @change="toggle(row, $event)"
          />
        </template>
      </el-table-column>
      <el-table-column label="说明">
        <template #default="{ row }">
          <el-input
            v-model="row.description"
            type="textarea"
            :rows="2"
            placeholder="请输入说明"
            @blur="saveDescription(row)"
          />
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ElMessage } from 'element-plus'
import request from '@/api/request'

const props = defineProps({
  type: String,
  data: Array
})

const emit = defineEmits(['update'])

async function toggle(row, enabled) {
  row.is_disabled = !enabled
  await save(row)
}

async function saveDescription(row) {
  await save(row)
}

async function save(row) {
  try {
    await request.put(`/participant-type-permissions/${row.id}`, {
      description: row.description,
      is_disabled: row.is_disabled
    })
    ElMessage.success('保存成功')
    emit('update')
  } catch (e) {
    ElMessage.error('保存失败')
  }
}
</script>

<style scoped>
.permissions-table {
  padding: 8px 0;
}
</style>
