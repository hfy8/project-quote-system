<template>
  <div class="save-bar">
    <span class="save-bar-label">{{ label }}</span>
    <div class="save-bar-actions">
      <slot name="extra" />
      <el-button type="primary" :loading="saving" @click="handleSave">
        <slot name="button-text">保存</slot>
      </el-button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  label: { type: String, default: '' },
  saving: { type: Boolean, default: false },
})

const emit = defineEmits(['save'])

function handleSave() {
  emit('save')
}
</script>

<style>
.save-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background: var(--color-bg-primary, #fff);
  border-top: 1px solid var(--color-border, #e5e7eb);
  border-radius: 0 0 var(--radius-md) var(--radius-md);
  margin: 16px -24px -24px;
}
.save-bar-label {
  font-size: 14px;
  color: var(--color-text-muted, #6b7280);
}
.save-bar-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}
</style>
