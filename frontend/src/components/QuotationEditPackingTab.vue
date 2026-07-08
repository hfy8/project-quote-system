<template>
  <div class="section-actions">
    <el-button type="primary" @click="emit('add-entry')">+ 添加运输包装条目</el-button>
  </div>

  <el-table :data="entries" border style="width: 100%; margin-top: 16px;">
    <el-table-column prop="packing_type_name" label="运输包装类型" />
    <el-table-column label="单价（元/个）" width="160">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" :model-value="row._unit_price" :min="0" :precision="2" size="small" controls-position="right" style="width: 120px;" @update:model-value="(v) => emit('row-unit-price-change', row, v)" />
        <span v-else class="money">¥{{ Number(row.unit_price || 0).toFixed(2) }}</span>
      </template>
    </el-table-column>
    <el-table-column label="数量" width="180">
      <template #default="{ row }">
        <el-input-number v-if="row._editing && !row.is_other" :model-value="row._quantity" :min="0" :precision="0" size="small" controls-position="right" style="width: 130px;" @update:model-value="(v) => emit('row-quantity-change', row, v)" />
        <span v-else-if="row.is_other === true">{{ row.quantity }} {{ row.unit }} <span style="color:#999;font-size:12px">(不可改)</span></span>
        <span v-else>{{ row.quantity }} {{ row.unit }}</span>
      </template>
    </el-table-column>
    <el-table-column label="小计" width="140">
      <template #default="{ row }"><span class="money">¥{{ ((row._editing ? row._unit_price : row.unit_price) || 0) * ((row._editing ? row._quantity : row.quantity) || 0) }}</span></template>
    </el-table-column>
    <el-table-column prop="remark" label="备注" />
    <el-table-column label="操作" width="150" align="center">
      <template #default="{ row }">
        <template v-if="row._editing">
          <el-button size="small" type="primary" @click="emit('save-row', row)">保存</el-button>
          <el-button size="small" @click="emit('cancel-edit', row)">取消</el-button>
        </template>
        <template v-else>
          <el-button size="small" @click="emit('edit-row', row)">编辑</el-button>
          <el-button size="small" type="danger" @click="emit('delete-entry', row.id)">删除</el-button>
        </template>
      </template>
    </el-table-column>
  </el-table>
  <div v-if="entries.length > 0" class="labor-total">
    运输包装费用合计：<strong>¥{{ total.toFixed(2) }}</strong>
  </div>

  <!-- 添加包装条目弹窗 -->
  <el-dialog v-model="dialogVisibleProxy" title="添加运输包装条目" width="450px" @close="emit('close-dialog')">
    <el-form :model="localForm" label-width="110px">
      <el-form-item label="运输包装类型" required>
        <el-select v-model="localForm.packing_type_id" placeholder="请选择" @change="emit('type-change', localForm.packing_type_id)">
          <el-option v-for="pt in packingTypes" :key="pt.id" :label="pt.name" :value="pt.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="单价">
        <span class="money">¥{{ Number(localForm.unit_price || 0).toFixed(2) }} / 个</span>
      </el-form-item>
      <el-form-item label="数量">
        <el-input-number v-model="localForm.quantity" :min="0" :precision="2" style="width: 100%;" @change="emit('quantity-change', localForm.quantity)" />
      </el-form-item>
      <el-form-item label="合计">
        <span class="money">¥{{ Number(localSubtotal).toFixed(2) }}</span>
      </el-form-item>
      <el-form-item label="备注">
        <el-input v-model="localForm.remark" placeholder="可选" @input="emit('remark-change', localForm.remark)" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="emit('cancel-dialog')">取消</el-button>
      <el-button type="primary" @click="syncAndConfirm">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  entries: { type: Array, required: true },
  total: { type: Number, default: 0 },
  packingTypes: { type: Array, required: true },
  form: { type: Object, required: true },
  dialogVisible: { type: Boolean, default: false },
})

const emit = defineEmits([
  'add-entry',
  'edit-row',
  'save-row',
  'cancel-edit',
  'delete-entry',
  'confirm-add',
  'cancel-dialog',
  'close-dialog',
  'update:visible',
  'type-change',
  'quantity-change',
  'remark-change',
  'row-unit-price-change',
  'row-quantity-change',
])

const dialogVisibleProxy = computed({
  get: () => props.dialogVisible,
  set: (v) => emit('update:visible', v),
})

const localForm = ref({
  packing_type_id: null,
  unit_price: 0,
  quantity: 0,
  remark: '',
})

watch(() => props.dialogVisible, (visible) => {
  if (visible) {
    localForm.value = {
      packing_type_id: props.form.packing_type_id ?? null,
      unit_price: Number(props.form.unit_price || 0),
      quantity: Number(props.form.quantity || 0),
      remark: props.form.remark || '',
    }
  }
}, { immediate: true })

watch(dialogVisibleProxy, (visible) => {
  if (!visible) {
    Object.assign(props.form, {
      packing_type_id: localForm.value.packing_type_id,
      unit_price: localForm.value.unit_price,
      quantity: localForm.value.quantity,
      remark: localForm.value.remark,
    })
  }
})

const syncAndConfirm = () => {
  Object.assign(props.form, {
    packing_type_id: localForm.value.packing_type_id,
    unit_price: localForm.value.unit_price,
    quantity: localForm.value.quantity,
    remark: localForm.value.remark,
  })
  emit('confirm-add')
}

const localSubtotal = computed(() =>
  Number(localForm.value.unit_price || 0) * Number(localForm.value.quantity || 0)
)
</script>