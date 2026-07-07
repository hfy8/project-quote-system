<template>
  <div class="export-grid">
    <div class="export-item" @click="emit('export-file', 'word')">
      <span class="export-icon">📝</span>
      <span class="export-label">导出 Word</span>
    </div>
    <div class="export-item" @click="emit('export-file', 'excel')">
      <span class="export-icon">📊</span>
      <span class="export-label">导出 Excel</span>
    </div>
    <el-dropdown @command="(cmd) => emit('export-file', 'pdf', cmd)" trigger="click">
      <div class="export-item" style="cursor:pointer">
        <span class="export-icon">📄</span>
        <span class="export-label">导出 PDF ▾</span>
      </div>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item command="zh">🇨🇳 中文 PDF</el-dropdown-item>
          <el-dropdown-item command="en">🇺🇸 English PDF</el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <div class="export-item" @click="emit('export-summary-pdf')">
      <span class="export-icon">🖼️</span>
      <span class="export-label">导出汇总 PDF（按网页）</span>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['export-file', 'export-summary-pdf'])
</script>