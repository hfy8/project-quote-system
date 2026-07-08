<template>
  <el-button type="primary" @click="$emit('open-add-dialog')" style="margin-bottom: 16px;">添加人员</el-button>
  <el-table :data="participants" border style="width: 100%">
    <el-table-column prop="user.real_name" label="姓名" />
    <el-table-column prop="user.username" label="用户名" />
    <el-table-column label="参与类型" width="150">
      <template #default="{ row }">
        <el-select v-model="row.participant_type" placeholder="选择类型" size="small" @change="$emit('update-type', row)">
          <el-option label="项目" value="project" />
          <el-option label="机构" value="agency" />
          <el-option label="电气" value="electrical" />
        </el-select>
      </template>
    </el-table-column>
    <el-table-column label="操作" width="100" align="center">
      <template #default="{ row }">
        <el-button size="small" type="danger" @click="$emit('remove', row.id)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-dialog
    :model-value="addDialogVisible"
    title="添加人员"
    width="500px"
    @update:model-value="$emit('update:add-dialog-visible', $event)"
  >
    <div class="add-participant-form">
      <el-input :model-value="searchKeyword" placeholder="搜索人员姓名或用户名" clearable style="width: 100%; margin-bottom: 16px;" @update:model-value="$emit('update:search-keyword', $event)" />
      <el-table :data="filteredUsers" v-loading="loading" border size="small" max-height="300" @selection-change="$emit('selection-change', $event)">
        <el-table-column type="selection" width="50" :selectable="checkSelectable"></el-table-column>
        <el-table-column prop="real_name" label="姓名" />
        <el-table-column prop="username" label="用户名" />
      </el-table>
    </div>
    <template #footer>
      <el-button @click="$emit('cancel-add')">取消</el-button>
      <el-button type="primary" :disabled="!selectedCount" @click="$emit('confirm-add')">添加 ({{ selectedCount }})</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
defineProps({
  participants: { type: Array, default: () => [] },
  addDialogVisible: { type: Boolean, default: false },
  searchKeyword: { type: String, default: '' },
  filteredUsers: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  selectedCount: { type: Number, default: 0 },
  checkSelectable: { type: Function, default: () => true },
})

defineEmits([
  'open-add-dialog',
  'update-type',
  'remove',
  'update:add-dialog-visible',
  'update:search-keyword',
  'selection-change',
  'cancel-add',
  'confirm-add',
])
</script>