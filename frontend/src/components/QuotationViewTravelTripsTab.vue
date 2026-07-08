<template>
  <div class="packing-header">
    <el-button type="primary" @click="$emit('show-add')">+ 添加人次条目</el-button>
  </div>
  <el-table :data="personTrips" border style="width: 100%; margin-top: 16px;">
    <el-table-column prop="travel_category_name" label="差旅分类" />
    <el-table-column prop="travel_mode_name" label="出行方式" />
    <el-table-column v-if="!isViewMode" prop="unit_price" label="交通单价" width="130">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" v-model="row._unit_price" :min="0" :precision="2" size="small" controls-position="right" style="width: 110px;" />
        <span v-else class="money">¥{{ row.unit_price.toFixed(2) }}</span>
      </template>
    </el-table-column>
    <el-table-column v-if="!isViewMode" prop="visa_fee" label="签证费" width="110">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" v-model="row._visa_fee" :min="0" :precision="2" size="small" controls-position="right" style="width: 90px;" />
        <span v-else class="money">¥{{ row.visa_fee.toFixed(2) }}</span>
      </template>
    </el-table-column>
    <el-table-column label="人次" width="100">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" v-model="row._person_count" :min="0" :precision="0" size="small" controls-position="right" style="width: 80px;" />
        <span v-else>{{ row.person_count }} 人</span>
      </template>
    </el-table-column>
    <el-table-column v-if="!isViewMode" label="小计" width="130">
      <template #default="{ row }"><span class="money">¥{{ ((row._editing ? row._unit_price : row.unit_price) + (row._editing ? row._visa_fee : row.visa_fee)) * (row._editing ? row._person_count : row.person_count) }}</span></template>
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
  <div v-if="personTrips.length > 0 && !isViewMode" class="labor-total">
    差旅人次合计：<strong>¥{{ tripsTotal.toFixed(2) }}</strong>
  </div>
  <el-dialog
    :model-value="dialogVisible"
    title="添加差旅人次"
    width="500px"
    @update:model-value="$emit('update:dialog-visible', $event)"
  >
    <el-form :model="formData" label-width="120px">
      <el-form-item label="差旅分类" required>
        <el-select :model-value="formData.travel_category_id" placeholder="请选择" @update:model-value="onCategoryChange">
          <el-option v-for="c in travelCategories" :key="c.id" :label="c.name" :value="c.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="出行方式" required>
        <el-select :model-value="formData.travel_mode_id" placeholder="请选择" @update:model-value="onModeChange">
          <el-option v-for="m in travelModes" :key="m.id" :label="m.name" :value="m.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="人次">
        <el-input-number :model-value="formData.person_count" :min="0" :precision="0" style="width: 100%;" @update:model-value="updateField('person_count', $event)" />
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
  personTrips: { type: Array, default: () => [] },
  tripsTotal: { type: Number, default: 0 },
  isViewMode: { type: Boolean, default: false },
  dialogVisible: { type: Boolean, default: false },
  formData: { type: Object, default: () => ({ travel_category_id: null, travel_mode_id: null, person_count: 0, remark: '' }) },
  travelCategories: { type: Array, default: () => [] },
  travelModes: { type: Array, default: () => [] },
})

const emit = defineEmits([
  'show-add', 'edit-row', 'save-row', 'cancel-edit', 'delete',
  'update:dialog-visible', 'update:form-data', 'confirm-add', 'category-change', 'mode-change',
])

function updateField(field, value) {
  emit('update:form-data', { ...props.formData, [field]: value })
}

function onCategoryChange(catId) {
  emit('update:form-data', { ...props.formData, travel_category_id: catId })
  emit('category-change', catId)
}
function onModeChange(modeId) {
  emit('update:form-data', { ...props.formData, travel_mode_id: modeId })
  emit('mode-change', modeId)
}
</script>