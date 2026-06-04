<template>
  <div class="ptp-page">
    <el-alert type="info" :closable="false" style="margin-bottom: 16px;">
      为不同参与类型配置可访问的 Tab 页面。权限控制仅对"我的分配"中的报价单查看页面生效。
    </el-alert>

    <!-- 分类卡片列表 -->
    <div class="type-grid">
      <div v-for="type in types" :key="type.type" class="type-card">
        <!-- 分类头部 -->
        <div class="type-card-header">
          <div class="type-info">
            <el-input v-if="type.editing" v-model="type.type_name" size="small" style="width: 120px;" @blur="saveTypeName(type)" @keyup.enter="saveTypeName(type)" />
            <span v-else class="type-name" @click="type.editing = true">{{ type.type_name || type.type }}</span>
            <el-tag size="small" type="info" style="margin-left: 8px;">{{ type.type }}</el-tag>
          </div>
          <div class="type-actions">
            <el-button size="small" link type="primary" @click="addTab(type)">+ 添加 Tab</el-button>
            <el-popconfirm title="确定删除该分类？" @confirm="deleteType(type)">
              <template #reference>
                <el-button size="small" link type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </div>
        </div>

        <!-- Tab 列表 -->
        <div class="tab-list">
          <div v-for="tab in type.tabs" :key="tab.id" class="tab-item">
            <div class="tab-info">
              <span class="tab-label">{{ tab.tab_label }}</span>
              <span class="tab-name">({{ tab.tab_name }})</span>
            </div>
            <div class="tab-controls">
              <el-switch
                v-model="tab._enabled"
                :active-text="'启用'"
                :inactive-text="'禁用'"
                size="small"
                @change="toggleTab(tab)"
              />
              <el-button size="small" link type="danger" @click="deleteTab(tab, type)">删除</el-button>
            </div>
          </div>
          <el-empty v-if="!type.tabs || type.tabs.length === 0" description="暂无 Tab，请添加" :image-size="60" />
        </div>
      </div>

      <!-- 添加分类卡片 -->
      <div class="type-card add-card" @click="showAddTypeDialog">
        <el-icon class="add-icon"><Plus /></el-icon>
        <span>添加分类</span>
      </div>
    </div>

    <!-- 添加分类对话框 -->
    <el-dialog v-model="addTypeDialogVisible" title="添加参与人员分类" width="400px">
      <el-form :model="newType" label-width="100px">
        <el-form-item label="分类标识">
          <el-input v-model="newType.type" placeholder="如: supplier" />
        </el-form-item>
        <el-form-item label="分类名称">
          <el-input v-model="newType.name" placeholder="如: 供应商" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="addTypeDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="createType">确认添加</el-button>
      </template>
    </el-dialog>

    <!-- 添加 Tab 对话框 -->
    <el-dialog v-model="addTabDialogVisible" title="添加 Tab" width="400px">
      <el-form :model="newTab" label-width="100px">
        <el-form-item label="Tab 标识">
          <el-select v-model="newTab.tab_name" placeholder="选择 Tab" style="width: 100%;">
            <el-option v-for="t in availableTabs" :key="t.value" :label="t.label + ' (' + t.value + ')'" :value="t.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="显示名称">
          <el-input v-model="newTab.tab_label" placeholder="如: 物料清单" />
        </el-form-item>
        <el-form-item label="说明">
          <el-input v-model="newTab.description" type="textarea" placeholder="可选说明" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="addTabDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmAddTab">确认添加</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import request from '@/api/request'

const types = ref([])

const addTypeDialogVisible = ref(false)
const newType = reactive({ type: '', name: '' })

const addTabDialogVisible = ref(false)
const newTab = reactive({ type: '', tab_name: '', tab_label: '', description: '' })

const availableTabs = [
  { value: 'modules', label: '模块管理' },
  { value: 'participants', label: '参与人员' },
  { value: 'materials', label: '物料清单' },
  { value: 'fees', label: '费用' },
  { value: 'labor', label: '人力工时' },
  { value: 'summary', label: '汇总' },
  { value: 'coefficients', label: '费用系数' },
  { value: 'export', label: '导出' },
  { value: 'packing', label: '运输包装' },
  { value: 'travel_person_days', label: '差旅人天' },
  { value: 'travel_person_trips', label: '差旅人次' },
]

async function loadAll() {
  try {
    const res = await request.get('/participant-type-permissions')
    const list = res || []

    // 按 type 分组
    const grouped = {}
    // 第一步：遍历所有记录，收集每个类型的 type_name，并创建类型条目
    for (const item of list) {
      const pt = item.participant_type
      if (!grouped[pt]) {
        grouped[pt] = {
          type: pt,
          type_name: item.type_name || pt,
          editing: false,
          tabs: []
        }
      }
    }
    // 第二步：再次遍历，把非 __type__ 的记录加入对应类型的 tabs
    for (const item of list) {
      if (item.tab_name === '__type__') continue  // 跳过类型标记记录
      item._enabled = !item.is_disabled  // 初始化 switch 状态
      grouped[item.participant_type].tabs.push({ ...item, editing: false })
    }
    types.value = Object.values(grouped)
  } catch (e) {
    console.error('加载失败', e)
  }
}

async function showAddTypeDialog() {
  newType.type = ''
  newType.name = ''
  addTypeDialogVisible.value = true
}

async function createType() {
  if (!newType.type) {
    ElMessage.warning('请输入分类标识')
    return
  }
  try {
    await request.post('/participant-type-permissions/types', {
      participant_type: newType.type,
      type_name: newType.name || newType.type
    })
    ElMessage.success('添加成功')
    addTypeDialogVisible.value = false
    loadAll()
  } catch (e) {
    ElMessage.error('添加失败')
  }
}

async function saveTypeName(type) {
  type.editing = false
  try {
    // 更新该类型所有记录的第一条（存储 type_name）
    await request.put(`/participant-type-permissions/${type.tabs[0].id}`, {
      type_name: type.type_name
    })
    // 同步更新该类型所有 Tab 的 type_name
    for (const tab of type.tabs) {
      tab.type_name = type.type_name
    }
  } catch (e) {
    console.error('保存失败', e)
  }
}

async function deleteType(type) {
  try {
    await request.delete(`/participant-type-permissions/types/${type.type}`)
    loadAll()
  } catch (e) {
    ElMessage.error('删除失败')
  }
}

function addTab(type) {
  newTab.type = type.type
  newTab.tab_name = ''
  newTab.tab_label = ''
  newTab.description = ''
  addTabDialogVisible.value = true
}

async function confirmAddTab() {
  if (!newTab.tab_name || !newTab.tab_label) {
    ElMessage.warning('请填写完整')
    return
  }
  // 从卡片对应的类型对象获取 type_name
  const typeObj = types.value.find(t => t.type === newTab.type)
  const type_name = typeObj?.type_name || newTab.type
  try {
    await request.post('/participant-type-permissions', {
      participant_type: newTab.type,
      tab_name: newTab.tab_name,
      tab_label: newTab.tab_label,
      description: newTab.description,
      type_name: type_name,
      is_disabled: false,
      sort_order: 0
    })
    ElMessage.success('添加成功')
    addTabDialogVisible.value = false
    loadAll()
  } catch (e) {
    ElMessage.error('添加失败')
  }
}

async function toggleTab(tab) {
  try {
    await request.put(`/participant-type-permissions/${tab.id}`, {
      is_disabled: !tab._enabled
    })
    ElMessage.success(tab._enabled ? '已启用' : '已禁用')
  } catch (e) {
    tab._enabled = !tab._enabled
    ElMessage.error('更新失败')
  }
}

async function deleteTab(tab, type) {
  try {
    await request.delete(`/participant-type-permissions/${tab.id}`)
    loadAll()
  } catch (e) {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  loadAll()
})
</script>

<style scoped>
.ptp-page {
  padding: 16px;
}
.type-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 16px;
}
.type-card {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  overflow: hidden;
  background: #fff;
}
.type-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f5f7fa;
  border-bottom: 1px solid #e4e7ed;
}
.type-info {
  display: flex;
  align-items: center;
}
.type-name {
  font-weight: 600;
  font-size: 15px;
  cursor: pointer;
}
.type-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}
.tab-list {
  padding: 8px 16px;
  min-height: 120px;
}
.tab-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}
.tab-item:last-child {
  border-bottom: none;
}
.tab-info {
  display: flex;
  align-items: center;
  gap: 4px;
}
.tab-label {
  font-size: 14px;
  color: #303133;
}
.tab-name {
  font-size: 12px;
  color: #909399;
}
.tab-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}
.add-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 160px;
  cursor: pointer;
  border-style: dashed;
  color: #909399;
  gap: 8px;
  transition: all 0.2s;
}
.add-card:hover {
  border-color: #0d9488;
  color: #0d9488;
}
.add-icon {
  font-size: 28px;
}
</style>
