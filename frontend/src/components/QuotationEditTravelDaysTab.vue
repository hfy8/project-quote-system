<template>
  <div class="packing-header">
    <el-button type="primary" @click="emit('add-entry')">+ 添加人天条目</el-button>
  </div>
  <el-table :data="entries" border style="width: 100%; margin-top: 16px;">
    <el-table-column prop="travel_category_name" label="差旅分类" width="160" />
    <el-table-column label="单价（元/人天）" width="180">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" :model-value="row._unit_price" :min="0" :precision="2" size="small" controls-position="right" style="width: 140px;" @update:model-value="(v) => emit('row-unit-price-change', row, v)" />
        <span v-else class="money">¥{{ row.unit_price.toFixed(2) }}</span>
      </template>
    </el-table-column>
    <el-table-column label="人天" width="180">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" :model-value="row._person_days" :min="0" :precision="2" size="small" controls-position="right" style="width: 130px;" @update:model-value="(v) => emit('row-person-days-change', row, v)" />
        <span v-else>{{ row.person_days }} 人天</span>
      </template>
    </el-table-column>
    <el-table-column label="小计" width="140">
      <template #default="{ row }"><span class="money">¥{{ (row._editing ? row._unit_price : row.unit_price) * (row._editing ? row._person_days : row.person_days) }}</span></template>
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
    差旅人天合计：<strong>¥{{ total.toFixed(2) }}</strong>
  </div>
  <el-dialog :model-value="dialogVisible" title="添加差旅人天" width="450px" @update:model-value="(v) => emit('update:visible', v)" @close="emit('close-dialog')">
    <el-form :model="form" label-width="120px">
      <el-form-item label="差旅分类" required>
        <el-select :model-value="form.travel_category_id" placeholder="请选择" @update:model-value="(v) => emit('category-change', v)">
          <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="单价">
        <span class="money">¥{{ form.unit_price.toFixed(2) }} / 人天</span>
      </el-form-item>
      <el-form-item label="人天">
        <el-input-number :model-value="form.person_days" :min="0" :precision="2" style="width: 100%;" @update:model-value="(v) => emit('person-days-change', v)" />
      </el-form-item>
      <el-form-item label="合计">
        <span class="money">¥{{ (form.unit_price * form.person_days).toFixed(2) }}</span>
      </el-form-item>
      <el-form-item label="备注">
        <el-input :model-value="form.remark" placeholder="可选" @update:model-value="(v) => emit('remark-change', v)" />
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
  entries: { type: Array, required: true },
  total: { type: Number, default: 0 },
  categories: { type: Array, required: true },
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
  'category-change',
  'person-days-change',
  'remark-change',
  'row-unit-price-change',
  'row-person-days-change',
])
</script>