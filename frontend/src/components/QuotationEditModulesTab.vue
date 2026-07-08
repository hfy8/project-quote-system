<template>
  <div class="module-actions">
    <el-button type="primary" @click="emit('add-module')">添加模块</el-button>
  </div>

  <el-table :data="modules" border style="width: 100%; margin-top: 16px;">
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
    <el-table-column label="操作" width="180">
      <template #default="{ row }">
        <el-button size="small" @click="emit('edit-module', row)">编辑</el-button>
        <el-button size="small" type="danger" @click="emit('delete-module', row.id)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <!-- 添加/编辑模块弹窗 -->
  <el-dialog v-model="dialogVisibleProxy" :title="dialogTitle" width="500px" @close="emit('close-dialog')">
    <el-form :model="moduleForm" label-width="100px">
      <el-form-item label="模块名称">
        <el-input v-model="moduleForm.name" placeholder="请输入模块名称" />
      </el-form-item>
      <el-form-item label="英文名称">
        <el-input v-model="moduleForm.name_en" placeholder="English name (optional)" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="moduleForm.description" type="textarea" rows="3" placeholder="请输入描述" />
      </el-form-item>
      <el-form-item label="模块类型">
        <div style="display: flex; align-items: center; gap: 8px; width: 100%;">
          <el-radio-group v-model="moduleForm.module_type" style="flex: 1;">
            <el-radio-button
              v-for="t in moduleTypes"
              :key="t.value"
              :value="t.value"
            >
              <span :style="{ color: t.color, fontWeight: 600 }">{{ t.label }}</span>
            </el-radio-button>
          </el-radio-group>
          <el-button
            v-if="participantsCount > 0"
            size="small"
            @click="emit('infer-type')"
            :title="`根据已选 ${participantsCount} 个参与人员岗位自动推断`"
          >
            ✨ 自动推断
          </el-button>
        </div>
        <div class="form-hint">
          机构: 机械/装配/焊工/CNC/钳工等; 电气: 电气/电控/电工等; 其他: 混合或无明确技术方向
        </div>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="emit('cancel-dialog')">取消</el-button>
      <el-button type="primary" @click="emit('save-module')">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modules: { type: Array, required: true },
  moduleTypes: { type: Array, required: true },
  moduleForm: { type: Object, required: true },
  moduleDialogVisible: { type: Boolean, default: false },
  moduleDialogTitle: { type: String, default: '添加模块' },
  participantsCount: { type: Number, default: 0 },
})

const emit = defineEmits([
  'add-module',
  'edit-module',
  'delete-module',
  'save-module',
  'cancel-dialog',
  'close-dialog',
  'infer-type',
  'update:dialogVisible',
])

const dialogVisibleProxy = computed({
  get: () => props.moduleDialogVisible,
  set: (v) => emit('update:dialogVisible', v),
})
</script>