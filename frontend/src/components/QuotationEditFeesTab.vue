<template>
  <div class="fee-actions">
    <el-button type="primary" @click="emit('add-fee')">添加费用</el-button>
  </div>

  <el-table :data="fees" border style="width: 100%; margin-top: 16px;">
    <el-table-column prop="fee_type" label="费用类型" />
    <el-table-column label="位置">
      <template #default="{ row }">
        {{ getLocationLabel(row.location) }}
      </template>
    </el-table-column>
    <el-table-column prop="amount" label="金额" />
    <el-table-column prop="description" label="描述" />
    <el-table-column label="操作" width="180">
      <template #default="{ row }">
        <el-button size="small" @click="emit('edit-fee', row)">编辑</el-button>
        <el-button size="small" type="danger" @click="emit('delete-fee', row.id)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <!-- 添加/编辑费用弹窗 -->
  <el-dialog :model-value="dialogVisible" :title="dialogTitle" width="500px" @update:model-value="(v) => emit('update:visible', v)" @close="emit('close-dialog')">
    <el-form :model="feeForm" label-width="100px">
      <el-form-item label="费用类型">
        <el-select v-model="feeForm.fee_type" placeholder="请选择费用类型">
          <el-option v-for="ft in feeTypes" :key="ft.id" :label="ft.name" :value="ft.name" />
        </el-select>
      </el-form-item>
      <el-form-item label="位置">
        <el-select v-model="feeForm.location" placeholder="请选择位置" disabled>
          <el-option label="厂内" value="internal" />
          <el-option label="厂外" value="external" />
        </el-select>
        <div class="form-tip">位置由费用类型自动带出</div>
      </el-form-item>
      <el-form-item label="金额">
        <el-input-number v-model="feeForm.amount" :min="0" :precision="2" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="feeForm.description" type="textarea" rows="3" placeholder="请输入描述" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="emit('cancel-dialog')">取消</el-button>
      <el-button type="primary" @click="emit('save-fee')">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
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

const getLocationLabel = (loc) => ({
  internal: '厂内',
  external: '厂外',
}[loc] || loc || '-')
</script>