<template>
  <div v-loading="summaryLoading" ref="summaryRef" element-loading-text="页面加载中...">
    <QuotationEditSummary
      :summary="summary"
      :summary-loading="summaryLoading"
      :selected-currency="selectedCurrency"
      :exchange-rates="exchangeRates"
      :exchange-rate-symbol="exchangeRateSymbol"
      :grouped-summary-modules-by-type="groupedViewSummaryModulesByType"
      :all-modules-count="allModulesCount"
      @update:selected-currency="$emit('update:selected-currency', $event)"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import QuotationEditSummary from '@/components/QuotationEditSummary.vue'

defineProps({
  summary: { type: Object, default: null },
  summaryLoading: { type: Boolean, default: false },
  selectedCurrency: { type: String, default: 'CNY' },
  exchangeRates: { type: Array, default: () => [] },
  exchangeRateSymbol: { type: String, default: '' },
  groupedViewSummaryModulesByType: { type: Array, default: () => [] },
  allModulesCount: { type: Number, default: 0 },
})

defineEmits(['update:selected-currency'])

// Template ref 透传给父级 (PDF 导出用)
const summaryRef = ref(null)
defineExpose({ summaryRef })
</script>