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

  <!-- 复制模块弹窗（分页 table 选择一项） -->
  <el-dialog
    :model-value="copyDialogVisible"
    title="从其他报价单复制模块"
    width="900px"
    @update:model-value="$emit('update:copy-dialog-visible', $event)"
  >
    <div class="copy-search-bar">
      <el-input
        :model-value="copyKeyword"
        placeholder="搜索模块名 / 报价单名 / 方案号"
        clearable
        @update:model-value="$emit('update:copy-keyword', $event)"
        @keyup.enter="$emit('copy-search')"
      >
        <template #append>
          <el-button @click="$emit('copy-search')">搜索</el-button>
        </template>
      </el-input>
    </div>
    <el-table
      :data="copyModules"
      v-loading="copyLoading"
      highlight-current-row
      :current-row-key="copySelectedId"
      row-key="id"
      @current-change="$emit('update:copy-selected-id', ($event?.id ?? null))"
      style="width: 100%; cursor: pointer;"
      empty-text="暂无可复制模块"
    >
      <el-table-column type="index" label="#" width="60" :index="(i) => (copyPage - 1) * copyPageSize + i + 1" />
      <el-table-column prop="name" label="模块名称" min-width="160" show-overflow-tooltip />
      <el-table-column label="所属报价单" min-width="200" show-overflow-tooltip>
        <template #default="{ row }">
          {{ row.quotation_name || '—' }}
          <span v-if="row.quotation_scheme_no" class="scheme-no">({{ row.quotation_scheme_no }})</span>
        </template>
      </el-table-column>
      <el-table-column label="类型" width="90">
        <template #default="{ row }">
          <el-tag :type="row.module_type === 'mechanical' ? 'primary' : row.module_type === 'electrical' ? 'warning' : 'info'" size="small" disable-transitions>
            {{ row.module_type_label || '其他' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="物料数" width="90" align="right">
        <template #default="{ row }">
          {{ (row.materials || []).length }}
        </template>
      </el-table-column>
      <el-table-column label="报价单 ID" prop="quotation_id" width="100" />
    </el-table>
    <div class="copy-pagination">
      <el-pagination
        :current-page="copyPage"
        :page-size="copyPageSize"
        :total="copyTotal"
        :page-sizes="[10, 15, 30, 50]"
        layout="total, sizes, prev, pager, next"
        background
        @current-change="$emit('update:copy-page', $event)"
        @size-change="$emit('update:copy-page-size', $event)"
      />
    </div>
    <template #footer>
      <span class="copy-hint">选中一行后点击"复制选中模块"</span>
      <el-button @click="$emit('update:copy-dialog-visible', false)">取消</el-button>
      <el-button type="primary" :disabled="!copySelectedId" :loading="copyLoading" @click="$emit('confirm-copy')">
        复制选中模块
      </el-button>
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
  copyLoading: { type: Boolean, default: false },
  copyModules: { type: Array, default: () => [] },
  copyTotal: { type: Number, default: 0 },
  copyPage: { type: Number, default: 1 },
  copyPageSize: { type: Number, default: 15 },
  copyKeyword: { type: String, default: '' },
  copySelectedId: { type: [Number, null], default: null },
  moduleTypes: { type: Array, default: () => [] },
  currentParticipantsCount: { type: Number, default: 0 },
  inferHint: { type: String, default: '' },
})

const emit = defineEmits([
  'show-add', 'show-copy-dialog',
  'edit', 'delete', 'infer-type',
  'update:dialog-visible', 'update:form-data', 'confirm-save',
  'update:copy-dialog-visible',
  'update:copy-keyword', 'update:copy-page', 'update:copy-page-size',
  'update:copy-selected-id',
  'copy-search',
  'confirm-copy',
])

function updateField(field, value) {
  emit('update:form-data', { ...props.formData, [field]: value })
}
</script>

<style scoped>
.copy-search-bar {
  margin-bottom: 12px;
}
.copy-pagination {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}
.copy-hint {
  margin-right: 12px;
  color: var(--color-text-secondary, #909399);
  font-size: 12px;
}
.scheme-no {
  color: var(--color-text-secondary, #909399);
  font-size: 12px;
  margin-left: 4px;
}
.module-type-group {
  margin-bottom: 24px;
  border: 1px solid var(--color-border-light, #ebeef5);
  border-radius: var(--radius-md, 8px);
  overflow: hidden;
  background: var(--color-bg-card, #fff);
}
.module-type-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 18px;
  background: var(--color-bg-hover, #f5f7fa);
  border-bottom: 2px solid var(--color-border-light, #ebeef5);
}
.module-type-header.type-mechanical { border-bottom-color: #3b82f6; }
.module-type-header.type-electrical { border-bottom-color: #f59e0b; }
.module-type-header.type-other { border-bottom-color: #94a3b8; }
.module-type-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #fff;
  flex-shrink: 0;
}
.module-type-icon.type-mechanical { background: #3b82f6; }
.module-type-icon.type-electrical { background: #f59e0b; }
.module-type-icon.type-other { background: #94a3b8; }
.module-type-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary, #303133);
}
.module-type-count {
  padding: 2px 10px;
  border-radius: 12px;
  background: var(--color-bg-hover, #f5f7fa);
  color: var(--color-text-secondary, #606266);
  font-size: 12px;
  font-weight: 500;
}
.module-type-body { padding: 0; }
.module-type-empty {
  padding: 32px;
  text-align: center;
  color: var(--color-text-secondary, #606266);
  font-size: 13px;
  font-style: italic;
}
.module-type-body .module-card-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 18px;
  border-bottom: 1px solid var(--color-border-light, #ebeef5);
  transition: background 0.2s;
}
.module-type-body .module-card-item:hover {
  background: var(--color-bg-hover, #f5f7fa);
}
.module-type-body .module-card-item:last-child { border-bottom: none; }
.module-card-info { flex: 1; min-width: 0; }
.module-card-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-text-primary, #303133);
  margin-bottom: 4px;
}
.module-card-meta {
  font-size: 12px;
  color: var(--color-text-secondary, #606266);
}
.module-card-actions {
  display: flex;
  gap: 8px;
  margin-left: 12px;
}
.module-actions {
  margin-bottom: 16px;
  display: flex;
  gap: 8px;
}
</style>