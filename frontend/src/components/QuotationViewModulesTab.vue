<template>
  <div class="module-actions">
    <el-button type="primary" @click="$emit('show-add')">添加模块</el-button>
    <el-button type="success" @click="$emit('show-copy-dialog')">从其他报价单复制模块</el-button>
  </div>

  <!-- 按模块类型分组卡片展示 -->
  <div v-for="group in groupedViewModulesByType" :key="group.value" class="module-type-group">
    <div class="module-type-header" :class="'type-' + group.value">
      <div class="module-type-icon" :class="'type-' + group.value">
        <span v-if="group.value === 'mechanical'">🔧</span>
        <span v-else-if="group.value === 'electrical'">⚡</span>
        <span v-else>📦</span>
      </div>
      <span class="module-type-title">{{ group.label }}模块</span>
      <span class="module-type-count">{{ group.group_module_count }} 个</span>
    </div>
    <div class="module-type-body">
      <div v-if="group.module_list.length === 0" class="module-type-empty">
        该类型暂无模块
      </div>
      <div v-for="row in group.module_list" :key="row.id" class="module-card-item">
        <div class="module-card-info">
          <div class="module-card-name">{{ row.name }}</div>
          <div class="module-card-meta">
            <span v-if="row.name_en">{{ row.name_en }} · </span>
            {{ row.description || '暂无描述' }}
          </div>
        </div>
        <div class="module-card-actions">
          <el-button size="small" @click="$emit('edit', row)">编辑</el-button>
          <el-button size="small" type="danger" @click="$emit('delete', row.id)">删除</el-button>
        </div>
      </div>
    </div>
  </div>

  <!-- 兼容旧数据: 后端未返 module_type 时降级 -->
  <el-table v-if="groupedViewModulesByType.length === 0 && modules.length > 0" :data="modules" border style="width: 100%; margin-top: 16px;">
    <el-table-column prop="name" label="模块名称" />
    <el-table-column prop="name_en" label="英文名称" />
    <el-table-column prop="description" label="描述" />
    <el-table-column label="模块类型" width="120">
      <template #default="{ row }">
        <el-tag
          :type="row.module_type === 'mechanical' ? 'primary' : row.module_type === 'electrical' ? 'warning' : 'info'"
          effect="light"
          disable-transitions
        >
          {{ row.module_type_label || '其他' }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column label="操作" width="160" align="center">
      <template #default="{ row }">
        <el-button size="small" @click="$emit('edit', row)">编辑</el-button>
        <el-button size="small" type="danger" @click="$emit('delete', row.id)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <!-- 添加/编辑模块弹窗 -->
  <el-dialog
    :model-value="dialogVisible"
    :title="dialogTitle"
    width="500px"
    @update:model-value="$emit('update:dialog-visible', $event)"
  >
    <el-form :model="formData" label-width="100px">
      <el-form-item label="模块名称" required>
        <el-input :model-value="formData.name" placeholder="请输入模块名称" @update:model-value="updateField('name', $event)" />
      </el-form-item>
      <el-form-item label="英文名称">
        <el-input :model-value="formData.name_en" placeholder="可选" @update:model-value="updateField('name_en', $event)" />
      </el-form-item>
      <el-form-item label="模块类型">
        <div style="display: flex; align-items: center; gap: 8px; width: 100%;">
          <el-radio-group :model-value="formData.module_type" style="flex: 1;" @update:model-value="updateField('module_type', $event)">
            <el-radio-button
              v-for="t in moduleTypes"
              :key="t.value"
              :value="t.value"
            >
              <span :style="{ color: t.color, fontWeight: 600 }">{{ t.label }}</span>
            </el-radio-button>
          </el-radio-group>
          <el-button
            v-if="currentParticipantsCount > 0"
            size="small"
            @click="$emit('infer-type')"
            :title="`根据已选 ${currentParticipantsCount} 个参与人员岗位自动推断`"
          >
            ✨ 自动推断
          </el-button>
        </div>
        <div class="form-hint" v-if="inferHint">{{ inferHint }}</div>
      </el-form-item>
      <el-form-item label="描述">
        <el-input :model-value="formData.description" type="textarea" :rows="3" placeholder="可选" @update:model-value="updateField('description', $event)" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="$emit('update:dialog-visible', false)">取消</el-button>
      <el-button type="primary" @click="$emit('confirm-save')">确定</el-button>
    </template>
  </el-dialog>

  <!-- 复制模块弹窗 -->
  <el-dialog
    :model-value="copyDialogVisible"
    title="从其他报价单复制模块"
    width="500px"
    @update:model-value="$emit('update:copy-dialog-visible', $event)"
  >
    <el-form label-width="100px">
      <el-form-item label="源报价单">
        <el-select :model-value="copySourceId" placeholder="请选择源报价单" filterable style="width: 100%;" @update:model-value="$emit('update:copy-source-id', $event)">
          <el-option v-for="q in copySourceQuotations" :key="q.id" :label="q.name" :value="q.id" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="$emit('update:copy-dialog-visible', false)">取消</el-button>
      <el-button type="primary" :loading="copyLoading" @click="$emit('confirm-copy')">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
const props = defineProps({
  modules: { type: Array, default: () => [] },
  groupedViewModulesByType: { type: Array, default: () => [] },
  dialogVisible: { type: Boolean, default: false },
  dialogTitle: { type: String, default: '添加模块' },
  formData: { type: Object, default: () => ({ id: null, name: '', name_en: '', module_type: '', description: '' }) },
  copyDialogVisible: { type: Boolean, default: false },
  copySourceId: { type: [Number, String, null], default: null },
  copySourceQuotations: { type: Array, default: () => [] },
  copyLoading: { type: Boolean, default: false },
  moduleTypes: { type: Array, default: () => [] },
  currentParticipantsCount: { type: Number, default: 0 },
  inferHint: { type: String, default: '' },
})

const emit = defineEmits([
  'show-add', 'show-copy-dialog',
  'edit', 'delete', 'infer-type',
  'update:dialog-visible', 'update:form-data', 'confirm-save',
  'update:copy-dialog-visible', 'update:copy-source-id', 'confirm-copy',
])

function updateField(field, value) {
  emit('update:form-data', { ...props.formData, [field]: value })
}
</script>