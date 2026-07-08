<template>
  <div class="export-grid">
    <div class="export-item" @click="$emit('export-file', 'word')">
      <span class="export-icon">📝</span>
      <span class="export-label">导出 Word</span>
    </div>
    <div class="export-item" @click="$emit('export-file', 'excel')">
      <span class="export-icon">📊</span>
      <span class="export-label">导出 Excel</span>
    </div>
    <div class="export-item" @click="$emit('export-file', 'pdf')">
      <span class="export-icon">📄</span>
      <span class="export-label">导出 PDF</span>
    </div>
    <div class="export-item" @click="$emit('export-summary-pdf')">
      <span class="export-icon">🖼️</span>
      <span class="export-label">导出汇总 PDF（按网页）</span>
    </div>
  </div>
</template>

<script setup>
defineEmits(['export-file', 'export-summary-pdf'])
</script>