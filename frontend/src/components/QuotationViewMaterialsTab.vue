<template>
  <QuotationEditMaterials
    :is-edit="false"
    :is-archived="false"
    :module-materials="moduleMaterials"
    :grouped-materials="groupedMaterials"
    :all-materials-total="allMaterialsTotal"
    :selected-currency="selectedCurrency"
    :exchange-rates="exchangeRates"
    :module-types="moduleTypes"
    :dispatch-group-info="dispatchGroupInfo"
    :modules="modules"
    :pending-review-count="0"
    :available-materials="availableMaterials"
    :material-total="materialTotal"
    :has-key-fields="hasKeyFields"
    :material-has-key-params="materialHasKeyParams"
    :selected-module-filter="selectedModuleFilter"
    @update:selected-module-filter="$emit('update:selected-module-filter', $event)"
    @update-quantity="(id, qty) => $emit('update-quantity', id, qty)"
    @delete-material="(id) => $emit('delete-material', id)"
    @add-materials="(moduleId, materials) => $emit('add-materials', moduleId, materials)"
    @save-other-price="(form) => $emit('save-other-price', form)"
    @load-materials="(params) => $emit('load-materials', params)"
  />
</template>

<script setup>
import QuotationEditMaterials from '@/components/QuotationEditMaterials.vue'

defineProps({
  moduleMaterials: { type: Array, default: () => [] },
  groupedMaterials: { type: Array, default: () => [] },
  allMaterialsTotal: { type: Number, default: 0 },
  selectedCurrency: { type: String, default: '' },
  exchangeRates: { type: Object, default: () => ({}) },
  moduleTypes: { type: Array, default: () => [] },
  dispatchGroupInfo: { type: Object, default: () => ({}) },
  modules: { type: Array, default: () => [] },
  availableMaterials: { type: Array, default: () => [] },
  materialTotal: { type: Number, default: 0 },
  hasKeyFields: { type: Boolean, default: false },
  materialHasKeyParams: { type: Boolean, default: false },
  selectedModuleFilter: { type: [Number, String], default: null },
})

defineEmits([
  'update:selected-module-filter',
  'update-quantity', 'delete-material', 'add-materials', 'save-other-price', 'load-materials',
])
</script>