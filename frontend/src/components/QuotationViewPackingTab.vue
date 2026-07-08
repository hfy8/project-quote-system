<template>
  <div class="packing-header">
    <el-button type="primary" @click="openAddDialog">+ 添加运输包装条目</el-button>
  </div>
  <el-table :data="entries" border style="width: 100%; margin-top: 16px;">
    <el-table-column prop="packing_type_name" label="运输包装类型" />
    <el-table-column v-if="!isViewMode" prop="unit_price" label="单价（元/个）" width="150">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" v-model="row._unit_price" :min="0" :precision="2" size="small" controls-position="right" style="width: 120px;" />
        <span v-else class="money">¥{{ row.unit_price.toFixed(2) }}</span>
      </template>
    </el-table-column>
    <el-table-column label="数量" width="160">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" v-model="row._quantity" :min="0" :precision="2" size="small" controls-position="right" style="width: 120px;" />
        <span v-else>{{ row.quantity }} {{ row.unit }}</span>
      </template>
    </el-table-column>
    <el-table-column v-if="!isViewMode" label="小计" width="130">
      <template #default="{ row }">
        <span class="money">¥{{ (row._editing ? row._unit_price : row.unit_price) * (row._editing ? row._quantity : row.quantity) }}</span>
      </template>
    </el-table-column>
    <el-table-column prop="remark" label="备注" />
    <el-table-column label="操作" width="150" align="center">
      <template #default="{ row }">
        <template v-if="row._editing">
          <el-button size="small" type="primary" @click="$emit('save', row)">保存</el-button>
          <el-button size="small" @click="$emit('cancel', row)">取消</el-button>
        </template>
        <template v-else>
          <el-button size="small" @click="$emit('edit', row)">编辑</el-button>
          <el-button size="small" type="danger" @click="$emit('delete', row.id)">删除</el-button>
        </template>
      </template>
    </el-table-column>
  </el-table>
  <div v-if="entries.length > 0 && !isViewMode" class="labor-total">
    运输包装费用合计：<strong>¥{{ total.toFixed(2) }}</strong>
  </div>

  <el-dialog v-model="addDialogVisible" title="添加运输包装条目" width="450px">
    <el-form :model="addForm" label-width="110px">
      <el-form-item label="运输包装类型" required>
        <el-select v-model="addForm.packing_type_id" placeholder="请选择" @change="$emit('type-change', addForm.packing_type_id)">
          <el-option v-for="pt in packingTypes" :key="pt.id" :label="pt.name" :value="pt.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="数量">
        <el-input-number v-model="addForm.quantity" :min="0" :precision="2" style="width: 100%;" />
      </el-form-item>
      <el-form-item label="备注">
        <el-input v-model="addForm.remark" placeholder="可选" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="addDialogVisible = false">取消</el-button>
      <el-button type="primary" @click="confirmAdd">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive } from 'vue'

const props = defineProps({
  entries: { type: Array, default: () => [] },
  total: { type: Number, default: 0 },
  packingTypes: { type: Array, default: () => [] },
  isViewMode: { type: Boolean, default: false },
})

const emit = defineEmits(['edit', 'save', 'cancel', 'delete', 'confirm-add', 'type-change', 'load-types'])

const addDialogVisible = ref(false)
const addForm = reactive({ packing_type_id: null, quantity: 0, remark: '' })

function openAddDialog() {
  // 重置 form
  addForm.packing_type_id = null
  addForm.quantity = 0
  addForm.remark = ''
  addDialogVisible.value = true
  // 通知父级加载 packingTypes (如果还没加载)
  emit('load-types')
}

function confirmAdd() {
  emit('confirm-add', { ...addForm })
  addDialogVisible.value = false
}
</script>