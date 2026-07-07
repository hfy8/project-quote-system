<template>
  <el-table :data="versions" border style="width: 100%;">
    <el-table-column prop="version_no" label="版本号" width="80" />
    <el-table-column prop="created_at" label="创建时间" />
    <el-table-column prop="creator_name" label="创建人" />
    <el-table-column prop="operation_type" label="操作类型" />
    <el-table-column prop="remark" label="备注" show-overflow-tooltip />
    <el-table-column label="操作" width="120" fixed="right">
      <template #default="{ row }">
        <el-dropdown trigger="click" @command="(cmd) => emit('export-version', row, cmd)">
          <el-button size="small" type="warning">PDF ▾</el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="pdf_zh">中文 PDF</el-dropdown-item>
              <el-dropdown-item command="pdf_en">English PDF</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup>
defineProps({
  versions: { type: Array, required: true },
})

const emit = defineEmits(['export-version'])
</script>