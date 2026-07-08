<template>
  <div class="section-actions">
    <el-button type="primary" @click="emit('add-fee')">添加费用</el-button>
  </div>

  <el-table :data="fees" border style="width: 100%; margin-top: 16px;">
    <el-table-column prop="fee_type" label="费用类型" />
    <el-table-column label="位置">
      <template #default="{ row }">
        {{ getLocationLabel(row.location) }}
      </template>
    </el-table-column>
    <el-table-column prop="amount" label="金额">
      <template #default="{ row }">¥{{ Number(row.amount || 0).toFixed(2) }}</template>
    </el-table-column>
    <el-table-column prop="description" label="描述" />
    <el-table-column label="操作" width="180">
      <template #default="{ row }">
        <el-button size="small" @click="emit('edit-fee', row)">编辑</el-button>
        <el-button size="small" type="danger" @click="emit('delete-fee', row.id)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <!-- 添加/编辑费用弹窗 -->
  <el-dialog v-model="dialogVisibleProxy" :title="dialogTitle" width="500px" @close="emit('close-dialog')">
    <el-form :model="localForm" label-width="100px">
      <el-form-item label="费用类型">
        <el-select v-model="localForm.fee_type" placeholder="请选择费用类型" @change="onFeeTypeChange">
          <el-option v-for="ft in feeTypes" :key="ft.id" :label="ft.name" :value="ft.name" />
        </el-select>
      </el-form-item>
      <el-form-item label="位置">
        <el-select v-model="localForm.location" placeholder="请选择位置" disabled>
          <el-option label="厂内" value="internal" />
          <el-option label="厂外" value="external" />
        </el-select>
        <div class="form-tip">位置由费用类型自动带出</div>
      </el-form-item>
      <el-form-item label="金额">
        <el-input-number v-model="localForm.amount" :min="0" :precision="2" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="localForm.description" type="textarea" rows="3" placeholder="请输入描述" />
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
  fees: { type: Array, required: true },
  feeTypes: { type: Array, required: true },
  feeForm: { type: Object, required: true },
  dialogVisible: { type: Boolean, default: false },
  dialogTitle: { type: String, default: '添加费用' },
})

const emit = defineEmits([
  'add-fee',
  'edit-fee',
  'delete-fee',
  'save-fee',
  'cancel-dialog',
  'close-dialog',
  'update:visible',
])

const dialogVisibleProxy = computed({
  get: () => props.dialogVisible,
  set: (v) => emit('update:visible', v),
})

const localForm = ref({
  fee_type: '',
  location: 'internal',
  amount: 0,
  description: '',
})

watch(() => props.dialogVisible, (visible) => {
  if (visible) {
    localForm.value = {
      fee_type: props.feeForm.fee_type || '',
      location: props.feeForm.location || 'internal',
      amount: Number(props.feeForm.amount || 0),
      description: props.feeForm.description || '',
    }
  }
}, { immediate: true })

watch(dialogVisibleProxy, (visible) => {
  if (!visible) {
    Object.assign(props.feeForm, {
      fee_type: localForm.value.fee_type,
      location: localForm.value.location,
      amount: localForm.value.amount,
      description: localForm.value.description,
    })
  }
})

const syncAndConfirm = () => {
  Object.assign(props.feeForm, {
    fee_type: localForm.value.fee_type,
    location: localForm.value.location,
    amount: localForm.value.amount,
    description: localForm.value.description,
  })
  emit('save-fee')
}

const onFeeTypeChange = (name) => {
  const ft = props.feeTypes.find(t => t.name === name)
  if (ft) {
    localForm.value.location = ft.location || 'internal'
  }
}

const getLocationLabel = (loc) => ({
  internal: '厂内',
  external: '厂外',
}[loc] || loc || '-')
</script>