<template>
  <div class="section-actions">
    <el-button type="primary" @click="emit('add-participant')">+ 添加人员</el-button>
  </div>

  <el-table :data="participants" border style="width: 100%; margin-top: 16px;">
    <el-table-column prop="user.real_name" label="姓名" />
    <el-table-column prop="user.username" label="用户名" />
    <el-table-column label="参与类型" width="180">
      <template #default="{ row }">
        <el-select :model-value="row.participant_type" placeholder="选择类型" size="small" @change="(v) => onTypeChange(row, v)">
          <el-option v-for="t in participantTypes" :key="t.type" :label="t.type_name + ' (' + t.type + ')'" :value="t.type" />
        </el-select>
      </template>
    </el-table-column>
    <el-table-column label="操作" width="100" align="center">
      <template #default="{ row }">
        <el-button size="small" type="danger" @click="emit('remove-participant', row.id)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <!-- 添加人员弹窗 -->
  <el-dialog v-model="dialogVisibleProxy" title="添加人员" width="560px" @close="emit('close-dialog')">
    <div class="add-participant-dialog">
      <div class="add-participant-row">
        <label class="add-participant-label">参与类型</label>
        <el-select :model-value="selectedParticipantType" placeholder="请选择参与类型" style="width: 100%;" @update:model-value="(v) => emit('update:type', v)">
          <el-option v-for="t in participantTypes" :key="t.type" :label="t.type_name + ' (' + t.type + ')'" :value="t.type" />
        </el-select>
      </div>
      <div class="add-participant-row">
        <label class="add-participant-label">搜索</label>
        <el-input :model-value="participantSearch" placeholder="搜索人员姓名或用户名" clearable @update:model-value="(v) => emit('update:search', v)" />
      </div>
      <div class="add-participant-row">
        <label class="add-participant-label">选择人员</label>
        <el-table
          :data="filteredUsers"
          v-loading="loading"
          border
          size="small"
          max-height="320"
          :row-key="(r) => r.id"
          @selection-change="(rows) => emit('update:selected', rows)"
          style="width: 100%;"
        >
          <el-table-column type="selection" width="55" :selectable="checkSelectable" />
          <el-table-column prop="real_name" label="姓名" />
          <el-table-column prop="username" label="用户名" />
        </el-table>
      </div>
    </div>
    <template #footer>
      <el-button @click="emit('cancel-dialog')">取消</el-button>
      <el-button type="primary" :disabled="!selectedCount || !selectedParticipantType" @click="emit('confirm-add')">添加 ({{ selectedCount }})</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  participants: { type: Array, required: true },
  participantTypes: { type: Array, required: true },
  dialogVisible: { type: Boolean, default: false },
  loading: { type: Boolean, default: false },
  availableUsers: { type: Array, default: () => [] },
  participantSearch: { type: String, default: '' },
  selectedParticipantType: { type: String, default: '' },
  selectedCount: { type: Number, default: 0 },
  checkSelectable: { type: Function, default: () => true },
})

const emit = defineEmits([
  'add-participant',
  'remove-participant',
  'confirm-add',
  'cancel-dialog',
  'close-dialog',
  'type-change',
  'update:visible',
  'update:search',
  'update:type',
  'update:selected',
])

const filteredUsers = computed(() => {
  const q = (props.participantSearch || '').toLowerCase().trim()
  if (!q) return props.availableUsers
  return props.availableUsers.filter(u =>
    (u.real_name && u.real_name.toLowerCase().includes(q)) ||
    (u.username && u.username.toLowerCase().includes(q))
  )
})

const checkSelectable = (row) => props.checkSelectable(row)
const onTypeChange = (row, v) => emit('type-change', row, v)

const dialogVisibleProxy = computed({
  get: () => props.dialogVisible,
  set: (v) => emit('update:visible', v),
})
</script>

<style scoped>
.add-participant-dialog {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.add-participant-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.add-participant-label {
  font-size: 13px;
  color: #606266;
  font-weight: 500;
}
</style>