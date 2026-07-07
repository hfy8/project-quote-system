<template>
  <div class="participant-actions">
    <el-button type="primary" @click="emit('add-participant')">+ 添加人员</el-button>
  </div>

  <el-table :data="participants" border style="width: 100%; margin-top: 16px;">
    <el-table-column prop="user.real_name" label="姓名" />
    <el-table-column prop="user.username" label="用户名" />
    <el-table-column label="参与类型" width="150">
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
  <el-dialog :model-value="dialogVisible" title="添加人员" width="500px" @update:model-value="(v) => emit('update:visible', v)" @close="emit('close-dialog')">
    <div class="add-participant-form">
      <el-form-item label="参与类型" style="margin-bottom: 16px;">
        <el-select :model-value="selectedParticipantType" placeholder="请选择参与类型" style="width: 100%;" @update:model-value="(v) => emit('update:type', v)">
          <el-option v-for="t in participantTypes" :key="t.type" :label="t.type_name + ' (' + t.type + ')'" :value="t.type" />
        </el-select>
      </el-form-item>
      <el-input :model-value="participantSearch" placeholder="搜索人员姓名或用户名" clearable style="width: 100%; margin-bottom: 16px;" @update:model-value="(v) => emit('update:search', v)" />
      <el-table :data="filteredUsers" v-loading="loading" border size="small" max-height="300" :row-key="(r) => r.id" @selection-change="(rows) => emit('update:selected', rows)">
        <el-table-column type="selection" width="50" :selectable="checkSelectable"></el-table-column>
        <el-table-column prop="real_name" label="姓名" />
        <el-table-column prop="username" label="用户名" />
      </el-table>
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

const checkSelectable = () => true
const onTypeChange = (row, v) => emit('type-change', row, v)
</script>