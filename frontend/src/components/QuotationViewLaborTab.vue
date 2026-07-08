<template>
  <div class="labor-header">
    <el-button type="primary" @click="$emit('show-add')">+ 添加工时</el-button>
  </div>

  <el-table :data="laborHours" border style="width: 100%; margin-top: 16px;">
    <el-table-column prop="labor_type" label="工时类型" width="110">
      <template #default="{ row }">
        <el-radio-group v-if="row._editing && !isViewMode" v-model="row._labor_type" size="small">
          <el-radio-button
            v-for="t in LABOR_TYPE_CHOICES"
            :key="t.value"
            :label="t.value"
            :title="t.label"
          >{{ t.label }}</el-radio-button>
        </el-radio-group>
        <el-tag v-else :color="LABOR_TYPE_CHOICES.find(t => t.value === row.labor_type)?.color" effect="dark" size="small" style="border: none; color: #fff;">
          {{ LABOR_TYPE_CHOICES.find(t => t.value === row.labor_type)?.label || '设计' }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column prop="name" label="名称" min-width="120">
      <template #default="{ row }">
        <el-input v-if="row._editing" v-model="row._name" size="small" placeholder="工时名称" />
        <span v-else>{{ row.name }}</span>
      </template>
    </el-table-column>
    <el-table-column prop="hours" label="工时 (h)" width="120">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" v-model="row._hours" :min="0" :precision="1" size="small" controls-position="right" style="width: 100px;" @change="onRowHoursChange(row)" />
        <span v-else>{{ row.hours }} h</span>
      </template>
    </el-table-column>
    <el-table-column prop="person_days" label="人天" width="120">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" v-model="row._person_days" :min="0" :precision="2" size="small" controls-position="right" style="width: 100px;" @change="onRowPersonDaysChange(row)" />
        <span v-else>{{ formatPersonDays(row.hours) }} 人天</span>
      </template>
    </el-table-column>
    <el-table-column v-if="!isViewMode" prop="unit_price" label="单价 (元/h)" width="140">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" v-model="row._unit_price" :min="0" :precision="2" size="small" controls-position="right" style="width: 110px;" />
        <span v-else>{{ row.unit_price.toFixed(2) }}</span>
      </template>
    </el-table-column>
    <el-table-column v-if="!isViewMode" prop="total" label="合计" width="120">
      <template #default="{ row }">{{ (row.hours * row.unit_price).toFixed(2) }}</template>
    </el-table-column>
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

  <div v-if="laborHours.length > 0 && !isViewMode" class="labor-total">
    人力费用合计：<strong>{{ laborTotal.toFixed(2) }} 元</strong>
    <span class="labor-total-days">（{{ formatPersonDays(laborHours.reduce((s, i) => s + (i.hours || 0), 0)) }} 人天）</span>
  </div>
  <div v-else-if="laborHours.length > 0 && isViewMode" class="labor-total">
    合计：<strong>{{ formatPersonDays(laborHours.reduce((s, i) => s + (i.hours || 0), 0)) }} 人天</strong>
  </div>

  <!-- 添加工时弹窗 -->
  <el-dialog
    :model-value="dialogVisible"
    title="添加人力工时"
    width="500px"
    @update:model-value="$emit('update:dialog-visible', $event)"
  >
    <el-form :model="formData" label-width="100px">
      <el-form-item label="名称">
        <el-select :model-value="formData.name" placeholder="请选择工时名称" style="width: 100%;" filterable @change="onNameChange">
          <el-option v-for="n in LABOR_NAME_CHOICES" :key="n.name" :label="n.name" :value="n.name" />
        </el-select>
      </el-form-item>
      <el-form-item label="工时类型">
        <el-radio-group :model-value="formData.labor_type" disabled>
          <el-radio-button
            v-for="t in LABOR_TYPE_CHOICES"
            :key="t.value"
            :label="t.value"
          >{{ t.label }}</el-radio-button>
        </el-radio-group>
        <span class="form-hint">根据名称自动设置</span>
      </el-form-item>
      <el-form-item label="工时 (h)">
        <el-input-number :model-value="formData.hours" :min="0" :precision="1" style="width: 100%;" @update:model-value="onHoursChange" />
      </el-form-item>
      <el-form-item label="人天">
        <el-input-number :model-value="formData.person_days" :min="0" :precision="2" style="width: 100%;" @update:model-value="onPersonDaysChange" />
        <span class="form-hint">{{ HOURS_PER_DAY }} h = 1 人天</span>
      </el-form-item>
      <el-form-item label="单价 (元/h)" v-if="!isMyAssignments">
        <el-input-number :model-value="formData.unit_price" :min="0" :precision="2" style="width: 100%;" @update:model-value="updateFormField('unit_price', $event)" />
      </el-form-item>
      <el-form-item label="合计" v-if="!isMyAssignments">
        <span>{{ (formData.hours * formData.unit_price).toFixed(2) }} 元</span>
        <span class="form-hint">（{{ formData.hours }} h = {{ formatPersonDays(formData.hours) }} 人天）</span>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="$emit('update:dialog-visible', false)">取消</el-button>
      <el-button type="primary" @click="$emit('confirm-add')">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { LABOR_TYPE_CHOICES, LABOR_NAME_CHOICES, HOURS_PER_DAY, formatPersonDays, hoursToPersonDays, personDaysToHours } from '@/utils/labor.js'

const props = defineProps({
  laborHours: { type: Array, default: () => [] },
  laborTotal: { type: Number, default: 0 },
  isViewMode: { type: Boolean, default: false },
  isMyAssignments: { type: Boolean, default: false },
  dialogVisible: { type: Boolean, default: false },
  formData: { type: Object, default: () => ({ name: '', labor_type: 'design', hours: 0, person_days: 0, unit_price: 0 }) },
})

const emit = defineEmits([
  'show-add',
  'edit-row', 'save-row', 'cancel-edit', 'delete',
  'row-hours-change', 'row-person-days-change',
  'update:dialog-visible', 'update:form-data', 'confirm-add',
])

function updateFormField(field, value) {
  emit('update:form-data', { ...props.formData, [field]: value })
}

function onNameChange(name) {
  // 1) 同步 name
  emit('update:form-data', { ...props.formData, name })
  // 2) 自动设置 labor_type (业务逻辑保留在子组件,父级不感知)
  const choice = LABOR_NAME_CHOICES.find(n => n.name === name)
  if (choice) {
    emit('update:form-data', { ...props.formData, name, labor_type: choice.labor_type })
  }
}

function onHoursChange(val) {
  if (val == null) val = 0
  emit('update:form-data', { ...props.formData, hours: val, person_days: hoursToPersonDays(val) })
}
function onPersonDaysChange(val) {
  if (val == null) val = 0
  emit('update:form-data', { ...props.formData, hours: personDaysToHours(val), person_days: val })
}

function onRowHoursChange(row) {
  if (row._hours == null) row._hours = 0
  row._person_days = hoursToPersonDays(row._hours)
}
function onRowPersonDaysChange(row) {
  if (row._person_days == null) row._person_days = 0
  row._hours = personDaysToHours(row._person_days)
}
</script>