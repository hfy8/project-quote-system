<template>
  <div class="fee-actions">
    <el-button type="primary" @click="$emit('show-add')">添加费用</el-button>
  </div>

  <el-table :data="fees" border style="width: 100%; margin-top: 16px;">
    <el-table-column prop="fee_type" label="费用类型" />
    <el-table-column prop="location" label="位置">
      <template #default="{ row }">
        {{ getLocationLabel(row.location) }}
      </template>
    </el-table-column>
    <el-table-column prop="amount" label="金额" />
    <el-table-column prop="description" label="描述" />
    <el-table-column label="操作" width="180">
      <template #default="{ row }">
        <el-button size="small" @click="$emit('edit', row)">编辑</el-button>
        <el-button size="small" type="danger" @click="$emit('delete', row.id)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-dialog
    :model-value="dialogVisible"
    :title="dialogTitle"
    width="500px"
    @update:model-value="$emit('update:dialog-visible', $event)"
  >
    <el-form :model="formData" label-width="100px">
      <el-form-item label="费用类型">
        <el-select :model-value="formData.fee_type" placeholder="请选择费用类型" @update:model-value="$emit('update:fee-form', { ...formData, fee_type: $event })">
          <el-option v-for="ft in feeTypes" :key="ft.id" :label="ft.name" :value="ft.name" />
        </el-select>
      </el-form-item>
      <el-form-item label="位置">
        <el-select :model-value="formData.location" placeholder="请选择位置" disabled>
          <el-option label="厂内" value="internal" />
          <el-option label="厂外" value="external" />
        </el-select>
        <div class="form-tip">位置由费用类型自动带出</div>
      </el-form-item>
      <el-form-item label="金额">
        <el-input-number :model-value="formData.amount" :min="0" :precision="2" @update:model-value="$emit('update:fee-form', { ...formData, amount: $event })" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input :model-value="formData.description" type="textarea" rows="3" placeholder="请输入描述" @update:model-value="$emit('update:fee-form', { ...formData, description: $event })" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="$emit('update:dialog-visible', false)">取消</el-button>
      <el-button type="primary" @click="$emit('save')">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
const props = defineProps({
  fees: { type: Array, default: () => [] },
  dialogVisible: { type: Boolean, default: false },
  dialogTitle: { type: String, default: '添加费用' },
  formData: { type: Object, default: () => ({ fee_type: '', location: '', amount: 0, description: '' }) },
  feeTypes: { type: Array, default: () => [] },
})

defineEmits([
  'show-add',
  'edit',
  'delete',
  'save',
  'update:dialog-visible',
  'update:fee-form',
])

// 复制父级工具函数 (避免 props drilling 深度)
function getLocationLabel(loc) {
  return { internal: '厂内', external: '厂外' }[loc] || loc
}
</script>