<template>
  <div class="labor-actions">
    <el-button type="primary" @click="emit('add-labor')">+ 添加人力工时</el-button>
  </div>

  <el-table :data="laborHours" border style="width: 100%; margin-top: 16px;">
    <el-table-column prop="labor_type" label="类型" width="100">
      <template #default="{ row }">
        <el-radio-group v-if="row._editing" v-model="row._labor_type" size="small">
          <el-radio-button
            v-for="t in laborTypeChoices"
            :key="t.value"
            :label="t.value"
            :title="t.label"
          >{{ t.label }}</el-radio-button>
        </el-radio-group>
        <el-tag v-else :color="getTypeColor(row.labor_type)" effect="dark" size="small" style="border: none; color: #fff;">
          {{ getTypeLabel(row.labor_type) }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column prop="name" label="名称" min-width="120">
      <template #default="{ row }">
        <el-input v-if="row._editing" :model-value="row._name" size="small" placeholder="工时名称" @update:model-value="(v) => emit('row-name-change', row, v)" />
        <span v-else>{{ row.name }}</span>
      </template>
    </el-table-column>
    <el-table-column prop="hours" label="工时 (h)" width="120">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" :model-value="row._hours" :min="0" :precision="1" size="small" controls-position="right" style="width: 100px;" @update:model-value="(v) => emit('row-hours-change', row, v)" />
        <span v-else>{{ row.hours }} h</span>
      </template>
    </el-table-column>
    <el-table-column prop="person_days" label="人天" width="120">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" :model-value="row._person_days" :min="0" :precision="2" size="small" controls-position="right" style="width: 100px;" @update:model-value="(v) => emit('row-person-days-change', row, v)" />
        <span v-else>{{ formatPersonDays(row.hours) }} 人天</span>
      </template>
    </el-table-column>
    <el-table-column prop="unit_price" label="单价 (元/h)" width="140">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" :model-value="row._unit_price" :min="0" :precision="2" size="small" controls-position="right" style="width: 110px;" @update:model-value="(v) => emit('row-unit-price-change', row, v)" />
        <span v-else>{{ row.unit_price.toFixed(2) }}</span>
      </template>
    </el-table-column>
    <el-table-column prop="total" label="合计" width="120">
      <template #default="{ row }">{{ (row.hours * row.unit_price).toFixed(2) }}</template>
    </el-table-column>
    <el-table-column label="操作" width="150" align="center">
      <template #default="{ row }">
        <template v-if="row._editing">
          <el-button size="small" type="primary" @click="emit('save-row', row)">保存</el-button>
          <el-button size="small" @click="emit('cancel-edit', row)">取消</el-button>
        </template>
        <template v-else>
          <el-button size="small" @click="emit('edit-row', row)">编辑</el-button>
          <el-button size="small" type="danger" @click="emit('delete-row', row.id)">删除</el-button>
        </template>
      </template>
    </el-table-column>
  </el-table>

  <div v-if="laborHours.length > 0" class="labor-total">
    人力费用合计：<strong>{{ laborTotal.toFixed(2) }} 元</strong>
    <span class="labor-total-days">（{{ formatPersonDays(laborHours.reduce((s, i) => s + (i.hours || 0), 0)) }} 人天）</span>
  </div>

  <!-- 添加工时弹窗 -->
  <el-dialog :model-value="dialogVisible" title="添加人力工时" width="500px" @update:model-value="(v) => emit('update:visible', v)" @close="emit('close-dialog')">
    <el-form :model="laborForm" label-width="100px">
      <el-form-item label="名称">
        <el-select :model-value="laborForm.name" placeholder="请选择工时名称" style="width: 100%;" filterable @update:model-value="(v) => emit('name-change', v)">
          <el-option v-for="n in laborNameChoices" :key="n.name" :label="n.name" :value="n.name" />
        </el-select>
      </el-form-item>
      <el-form-item label="工时类型">
        <el-radio-group :model-value="laborForm.labor_type" disabled>
          <el-radio-button
            v-for="t in laborTypeChoices"
            :key="t.value"
            :label="t.value"
          >{{ t.label }}</el-radio-button>
        </el-radio-group>
        <span class="form-hint">根据名称自动设置</span>
      </el-form-item>
      <el-form-item label="工时 (h)">
        <el-input-number :model-value="laborForm.hours" :min="0" :precision="1" style="width: 100%;" @update:model-value="(v) => emit('hours-change', v)" />
      </el-form-item>
      <el-form-item label="人天">
        <el-input-number :model-value="laborForm.person_days" :min="0" :precision="2" style="width: 100%;" @update:model-value="(v) => emit('person-days-change', v)" />
        <span class="form-hint">{{ hoursPerDay }} h = 1 人天</span>
      </el-form-item>
      <el-form-item label="单价 (元/h)">
        <el-input-number :model-value="laborForm.unit_price" :min="0" :precision="2" style="width: 100%;" @update:model-value="(v) => emit('unit-price-change', v)" />
      </el-form-item>
      <el-form-item label="合计">
        <span>{{ (laborForm.hours * laborForm.unit_price).toFixed(2) }} 元</span>
        <span class="form-hint">（{{ laborForm.hours }} h = {{ formatPersonDays(laborForm.hours) }} 人天）</span>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="emit('cancel-dialog')">取消</el-button>
      <el-button type="primary" @click="emit('confirm-add')">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
const props = defineProps({
  laborHours: { type: Array, required: true },
  laborTotal: { type: Number, default: 0 },
  laborForm: { type: Object, required: true },
  laborTypeChoices: { type: Array, required: true },
  laborNameChoices: { type: Array, required: true },
  hoursPerDay: { type: Number, default: 8 },
  dialogVisible: { type: Boolean, default: false },
})

const emit = defineEmits([
  'add-labor',
  'edit-row',
  'save-row',
  'cancel-edit',
  'delete-row',
  'confirm-add',
  'cancel-dialog',
  'close-dialog',
  'update:visible',
  'row-name-change',
  'row-hours-change',
  'row-person-days-change',
  'row-unit-price-change',
  'name-change',
  'hours-change',
  'person-days-change',
  'unit-price-change',
])

const formatPersonDays = (hours) => (Number(hours) || 0) / props.hoursPerDay
const getTypeColor = (value) => props.laborTypeChoices.find(t => t.value === value)?.color
const getTypeLabel = (value) => props.laborTypeChoices.find(t => t.value === value)?.label || '设计'
</script>