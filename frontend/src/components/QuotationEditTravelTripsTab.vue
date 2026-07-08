<template>
  <div class="section-actions">
    <el-button type="primary" @click="emit('add-entry')">+ 添加差旅人次</el-button>
  </div>

  <el-table :data="entries" border style="width: 100%; margin-top: 16px;">
    <el-table-column prop="travel_category_name" label="差旅分类" min-width="120" />
    <el-table-column prop="travel_mode_name" label="出行方式" min-width="120" />
    <el-table-column prop="unit_price" label="交通单价" width="120" align="right">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" :model-value="row._unit_price" :min="0" :precision="2" size="small" controls-position="right" style="width: 110px;" @update:model-value="(v) => emit('row-unit-price-change', row, v)" />
        <span v-else>¥{{ Number(row.unit_price || 0).toFixed(2) }}</span>
      </template>
    </el-table-column>
    <el-table-column prop="visa_fee" label="签证费" width="100" align="right">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" :model-value="row._visa_fee" :min="0" :precision="2" size="small" controls-position="right" style="width: 90px;" @update:model-value="(v) => emit('row-visa-fee-change', row, v)" />
        <span v-else>¥{{ Number(row.visa_fee || 0).toFixed(2) }}</span>
      </template>
    </el-table-column>
    <el-table-column label="人次" width="120">
      <template #default="{ row }">
        <el-input-number v-if="row._editing" :model-value="row._person_count" :min="0" :precision="0" size="small" controls-position="right" style="width: 90px;" @update:model-value="(v) => emit('row-person-count-change', row, v)" />
        <span v-else>{{ row.person_count }} 人</span>
      </template>
    </el-table-column>
    <el-table-column label="小计" width="140" align="right">
      <template #default="{ row }"><span class="money">¥{{ ((row._editing ? row._unit_price : row.unit_price) || 0) * ((row._editing ? row._person_count : row.person_count) || 0) }}</span></template>
    </el-table-column>
    <el-table-column prop="remark" label="备注" />
    <el-table-column label="操作" width="180" align="center">
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
    差旅人次合计：<strong>¥{{ total.toFixed(2) }}</strong>
  </div>

  <el-dialog v-model="dialogVisibleProxy" title="添加差旅人次" width="500px" @close="emit('close-dialog')">
    <el-form :model="localForm" label-width="120px">
      <el-form-item label="差旅分类" required>
        <el-select v-model="localForm.travel_category_id" placeholder="请选择" @change="emit('category-change', localForm.travel_category_id)">
          <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="出行方式" required>
        <el-select v-model="localForm.travel_mode_id" placeholder="请选择" @change="emit('mode-change', localForm.travel_mode_id)">
          <el-option v-for="m in modes" :key="m.id" :label="m.name" :value="m.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="交通单价">
        <span class="money">¥{{ Number(localForm.unit_price || 0).toFixed(2) }} / 人次</span>
      </el-form-item>
      <el-form-item v-if="localForm.visa_fee > 0" label="签证费">
        <span class="money">¥{{ Number(localForm.visa_fee || 0).toFixed(2) }} / 人次（非国内出差）</span>
      </el-form-item>
      <el-form-item label="人次">
        <el-input-number v-model="localForm.person_count" :min="0" :precision="0" style="width: 100%;" @change="emit('person-count-change', localForm.person_count)" />
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
  categories: { type: Array, required: true },
  modes: { type: Array, required: true },
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
  'mode-change',
  'person-count-change',
  'remark-change',
  'row-unit-price-change',
  'row-visa-fee-change',
  'row-person-count-change',
])

const dialogVisibleProxy = computed({
  get: () => props.dialogVisible,
  set: (v) => emit('update:visible', v),
})

// 本地 form 镜像: 打开弹窗时从 props.form 复制, 关闭时回写 (避开父级 reactive 双向同步坑)
const localForm = ref({
  travel_category_id: null,
  travel_mode_id: null,
  unit_price: 0,
  visa_fee: 0,
  person_count: 0,
  remark: '',
})

watch(() => props.dialogVisible, (visible) => {
  if (visible) {
    localForm.value = {
      travel_category_id: props.form.travel_category_id ?? null,
      travel_mode_id: props.form.travel_mode_id ?? null,
      unit_price: Number(props.form.unit_price || 0),
      visa_fee: Number(props.form.visa_fee || 0),
      person_count: Number(props.form.person_count || 0),
      remark: props.form.remark || '',
    }
  }
}, { immediate: true })

watch(dialogVisibleProxy, (visible) => {
  if (!visible) {
    Object.assign(props.form, {
      travel_category_id: localForm.value.travel_category_id,
      travel_mode_id: localForm.value.travel_mode_id,
      unit_price: localForm.value.unit_price,
      visa_fee: localForm.value.visa_fee,
      person_count: localForm.value.person_count,
      remark: localForm.value.remark,
    })
  }
})

const syncAndConfirm = () => {
  // 把本地 form 立即同步到父级 form (让父级 confirm 函数能读到)
  Object.assign(props.form, {
    travel_category_id: localForm.value.travel_category_id,
    travel_mode_id: localForm.value.travel_mode_id,
    unit_price: localForm.value.unit_price,
    visa_fee: localForm.value.visa_fee,
    person_count: localForm.value.person_count,
    remark: localForm.value.remark,
  })
  emit('confirm-add')
}

const localSubtotal = computed(() =>
  (Number(localForm.value.unit_price || 0) + Number(localForm.value.visa_fee || 0)) *
  Number(localForm.value.person_count || 0)
)
</script>