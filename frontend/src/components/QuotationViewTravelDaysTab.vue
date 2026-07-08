<template>
  <div class="packing-header">
    <el-button type="primary" @click="$emit('show-add')">+ 添加人天条目</el-button>
  </div>
  <el-table :data="personDays" border style="width: 100%; margin-top: 16px;">
    <el-table-column prop="travel_category_name" label="差旅分类" />
    <el-table-column v-if="!isViewMode" prop="unit_price" label="单价（元/人天）" width="150">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" v-model="row._unit_price" :min="0" :precision="2" size="small" controls-position="right" style="width: 120px;" />
        <span v-else class="money">¥{{ row.unit_price.toFixed(2) }}</span>
      </template>
    </el-table-column>
    <el-table-column label="人天" width="160">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" v-model="row._person_days" :min="0" :precision="2" size="small" controls-position="right" style="width: 120px;" />
        <span v-else>{{ row.person_days }} 人天</span>
      </template>
    </el-table-column>
    <el-table-column v-if="!isViewMode" label="小计" width="130">
      <template #default="{ row }"><span class="money">¥{{ (row._editing ? row._unit_price : row.unit_price) * (row._editing ? row._person_days : row.person_days) }}</span></template>
    </el-table-column>
    <el-table-column prop="remark" label="备注" />
    <el-table-column label="操作" width="150" align="center">
      <template #default="{ row }">
        <template v-if="row._editing">
          <el-button size="small" type="primary" @click="$emit('save-row', row)">保存</el-button>
          <el-button size="small" @click="$emit('cancel-edit', row)">取消</el-button>
        </template>
        <template v-else>
          <el-button size="small" @click="$emit('edit-row', row)">编辑</el-button>
          <el-button size="small" type="danger" @click="$emit('delete', row.id)">删除</el-button>
        </template>
      </template>
    </el-table-column>
  </el-table>
  <div v-if="personDays.length > 0 && !isViewMode" class="labor-total">
    差旅人天合计：<strong>¥{{ daysTotal.toFixed(2) }}</strong>
  </div>
  <el-dialog
    :model-value="dialogVisible"
    title="添加差旅人天"
    width="450px"
    @update:model-value="$emit('update:dialog-visible', $event)"
  >
    <el-form :model="formData" label-width="120px">
      <el-form-item label="差旅分类" required>
        <el-select :model-value="formData.travel_category_id" placeholder="请选择" @update:model-value="onCategoryChange">
          <el-option v-for="c in travelCategories" :key="c.id" :label="c.name" :value="c.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="人天">
        <el-input-number :model-value="formData.person_days" :min="0" :precision="2" style="width: 100%;" @update:model-value="updateField('person_days', $event)" />
      </el-form-item>
      <el-form-item label="备注">
        <el-input :model-value="formData.remark" placeholder="可选" @update:model-value="updateField('remark', $event)" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="$emit('update:dialog-visible', false)">取消</el-button>
      <el-button type="primary" @click="$emit('confirm-add')">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
const props = defineProps({
  personDays: { type: Array, default: () => [] },
  daysTotal: { type: Number, default: 0 },
  isViewMode: { type: Boolean, default: false },
  dialogVisible: { type: Boolean, default: false },
  formData: { type: Object, default: () => ({ travel_category_id: null, person_days: 0, remark: '' }) },
  travelCategories: { type: Array, default: () => [] },
})

const emit = defineEmits([
  'show-add', 'edit-row', 'save-row', 'cancel-edit', 'delete',
  'update:dialog-visible', 'update:form-data', 'confirm-add', 'category-change',
])

function updateField(field, value) {
  emit('update:form-data', { ...props.formData, [field]: value })
}

function onCategoryChange(catId) {
  // 1) 同步 formData
  emit('update:form-data', { ...props.formData, travel_category_id: catId })
  // 2) 通知父级 (父级根据分类自动设置 unit_price)
  emit('category-change', catId)
}
</script>