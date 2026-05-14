<template>
  <div class="system-settings">
    <el-card>
      <template #header>
        <span>系统设置</span>
      </template>
      
      <el-tabs v-model="activeTab">
        <el-tab-pane label="基本设置" name="basic">
          <el-form label-width="120px" style="max-width: 600px;">
            <el-form-item label="系统名称">
              <el-input v-model="settings.systemName" placeholder="请输入系统名称" />
            </el-form-item>
            <el-form-item label="公司名称">
              <el-input v-model="settings.companyName" placeholder="请输入公司名称" />
            </el-form-item>
            <el-form-item label="联系电话">
              <el-input v-model="settings.contactPhone" placeholder="请输入联系电话" />
            </el-form-item>
            <el-form-item label="电子邮箱">
              <el-input v-model="settings.contactEmail" placeholder="请输入电子邮箱" />
            </el-form-item>
            <el-form-item label="公司地址">
              <el-input v-model="settings.address" type="textarea" :rows="3" placeholder="请输入公司地址" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSaveBasic">保存</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="报价设置" name="quote">
          <el-form label-width="120px" style="max-width: 600px;">
            <el-form-item label="默认税率">
              <el-input-number v-model="settings.defaultTaxRate" :min="0" :max="100" :precision="2" />
              <span style="margin-left: 8px;">%</span>
            </el-form-item>
            <el-form-item label="利润率">
              <el-input-number v-model="settings.defaultProfitRate" :min="0" :max="100" :precision="2" />
              <span style="margin-left: 8px;">%</span>
            </el-form-item>
            <el-form-item label="最低报价">
              <el-input-number v-model="settings.minQuoteAmount" :min="0" :precision="2" />
            </el-form-item>
            <el-form-item label="货币单位">
              <el-select v-model="settings.currency" style="width: 200px;">
                <el-option label="人民币 (¥)" value="CNY" />
                <el-option label="美元 ($)" value="USD" />
                <el-option label="欧元 (€)" value="EUR" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSaveQuote">保存</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="外观设置" name="appearance">
          <el-form label-width="120px" style="max-width: 600px;">
            <el-form-item label="主题颜色">
              <el-color-picker v-model="settings.themeColor" />
            </el-form-item>
            <el-form-item label="侧边栏主题">
              <el-radio-group v-model="settings.sidebarTheme">
                <el-radio label="dark">深色</el-radio>
                <el-radio label="light">浅色</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="紧凑模式">
              <el-switch v-model="settings.compactMode" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSaveAppearance">保存</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="数据管理" name="data">
          <el-form label-width="120px" style="max-width: 600px;">
            <el-form-item label="数据备份">
              <el-button @click="handleBackup">创建备份</el-button>
              <el-button @click="handleExportData">导出数据</el-button>
            </el-form-item>
            <el-form-item label="数据恢复">
              <el-upload :auto-upload="false" :limit="1">
                <el-button>选择备份文件</el-button>
              </el-upload>
              <el-button type="warning" style="margin-left: 10px;">恢复数据</el-button>
            </el-form-item>
            <el-form-item label="清空数据">
              <el-button type="danger" @click="handleClearData">清空所有数据</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const activeTab = ref('basic')

const settings = reactive({
  systemName: '项目报价系统',
  companyName: '示例公司',
  contactPhone: '400-123-4567',
  contactEmail: 'contact@example.com',
  address: '',
  defaultTaxRate: 13,
  defaultProfitRate: 15,
  minQuoteAmount: 1000,
  currency: 'CNY',
  themeColor: '#409eff',
  sidebarTheme: 'dark',
  compactMode: false
})

const handleSaveBasic = () => {
  ElMessage.success('基本设置已保存')
}

const handleSaveQuote = () => {
  ElMessage.success('报价设置已保存')
}

const handleSaveAppearance = () => {
  ElMessage.success('外观设置已保存')
}

const handleBackup = () => {
  ElMessage.info('创建备份功能')
}

const handleExportData = () => {
  ElMessage.info('导出数据功能')
}

const handleClearData = async () => {
  try {
    await ElMessageBox.confirm('确定要清空所有数据吗？此操作不可恢复！', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    ElMessage.info('清空数据功能')
  } catch (error) {
    // 用户取消
  }
}
</script>

<style scoped>
.system-settings {
  padding: 16px;
}
</style>
