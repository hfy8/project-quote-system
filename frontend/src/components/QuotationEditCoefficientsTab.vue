<template>
  <div class="coefficient-card">
    <div class="coefficient-header">
      <div class="coefficient-title">
        <span>费用系数配置</span>
      </div>
      <div class="coefficient-actions">
        <el-button size="small" @click="emit('reset')">重置为系统默认</el-button>
        <QuotationEditSaveBar label="费用系数" :saving="saving" @save="emit('save')" />
      </div>
    </div>
    <div class="coefficient-desc">
      费用系数用于调整大件、核心部件、其他件的成本计算系数，仅影响当前报价单
    </div>
    <div class="coefficient-items">
      <div class="coefficient-item">
        <div class="coefficient-item-icon large"><span>大</span></div>
        <div class="coefficient-item-content">
          <div class="coefficient-item-label">大件系数</div>
          <div class="coefficient-item-tip">大型设备/材料成本系数</div>
        </div>
        <el-input-number v-model="coefficients.large" :min="0" :max="10" :precision="2" :step="0.05" style="width: 140px;" />
      </div>
      <div class="coefficient-item">
        <div class="coefficient-item-icon standard"><span>通</span></div>
        <div class="coefficient-item-content">
          <div class="coefficient-item-label">核心部件系数</div>
          <div class="coefficient-item-tip">标准常规材料成本系数</div>
        </div>
        <el-input-number v-model="coefficients.standard" :min="0" :max="10" :precision="2" :step="0.05" style="width: 140px;" />
      </div>
      <div class="coefficient-item">
        <div class="coefficient-item-icon other"><span>其</span></div>
        <div class="coefficient-item-content">
          <div class="coefficient-item-label">其他件系数</div>
          <div class="coefficient-item-tip">配件耗材等材料成本系数</div>
        </div>
        <el-input-number v-model="coefficients.other" :min="0" :max="10" :precision="2" :step="0.05" style="width: 140px;" />
      </div>
    </div>
  </div>
</template>

<script setup>
import QuotationEditSaveBar from './QuotationEditSaveBar.vue'

const props = defineProps({
  coefficients: { type: Object, required: true },
  saving: { type: Boolean, default: false },
})

const emit = defineEmits(['save', 'reset'])
</script>