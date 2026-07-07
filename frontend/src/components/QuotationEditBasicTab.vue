<template>
  <el-form :model="quotation" :rules="formRules" label-width="120px">
    <!-- 方案编号放最上方：选完方案号会自动填名称 + 业务负责人等 -->
    <el-form-item label="方案编号" prop="scheme_no">
      <el-autocomplete
        v-model="quotation.scheme_no"
        :fetch-suggestions="querySchemeSuggestions"
        placeholder="请输入方案编号，输入字符后会从方案库推荐"
        :disabled="isEdit || !!parentId"
        clearable
        :trigger-on-focus="false"
        @select="handleSelectScheme"
        @input="onSchemeInput"
        @blur="validateSchemeLocally"
        style="width: 100%"
        value-key="schemeNo"
      >
        <template #default="{ item }">
          <div class="scheme-suggestion" :class="{ 'is-used': item.is_used_locally }">
            <span class="scheme-no">{{ item.schemeNo }}</span>
            <span class="scheme-name">{{ item.schemeName || '(无名称)' }}</span>
            <el-tag v-if="item.is_used_locally" type="danger" size="small">已被本系统使用</el-tag>
            <el-tag v-else-if="item.schemeStatus === 'IN_PROGRESS'" type="warning" size="small">进行中</el-tag>
            <el-tag v-else-if="item.schemeStatus === 'COMPLETED'" type="success" size="small">已完成</el-tag>
          </div>
        </template>
      </el-autocomplete>
      <span v-if="parentId" style="margin-left: 8px; color: #888; font-size: 12px;">自动生成，不可编辑</span>
      <span v-else-if="schemeHint" :class="['scheme-hint', schemeHintType]">{{ schemeHint }}</span>
    </el-form-item>
    <el-form-item label="报价单名称">
      <el-input v-model="quotation.name" placeholder="可手动填写；选完方案号会自动填入" :disabled="isEdit" />
    </el-form-item>
    <el-form-item label="项目类型">
      <el-select v-model="quotation.type" placeholder="请选择类型" :disabled="isEdit || !!parentId">
        <el-option label="单机 (single)" value="single" />
        <el-option label="线体 (line)" value="line" />
      </el-select>
      <span v-if="parentId" style="margin-left: 8px; color: #888; font-size: 12px;">子报价单（单机）</span>
    </el-form-item>
    <el-form-item label="状态">
      <el-select v-model="quotation.status" placeholder="请选择状态" :disabled="isEdit">
        <el-option label="草稿" value="draft" />
        <el-option label="已提交" value="submitted" />
        <el-option label="已批准" value="approved" />
        <el-option label="已拒绝" value="rejected" />
      </el-select>
    </el-form-item>
    <el-form-item label="业务负责人">
      <span v-if="isEdit && quotation.business_owner_name">{{ quotation.business_owner_name }}</span>
      <el-select v-else v-model="quotation.business_owner_id" placeholder="请选择业务负责人">
        <el-option
          v-for="user in businessUsers"
          :key="user.id"
          :label="user.real_name"
          :value="user.id"
        />
      </el-select>
    </el-form-item>
    <el-form-item label="币种">
      <el-select v-model="quotation.currency" placeholder="请选择币种" :disabled="isEdit">
        <el-option v-for="opt in currencyOptions" :key="opt.value" :label="opt.label" :value="opt.value" />
      </el-select>
    </el-form-item>
    <el-form-item label="税率">
      <el-select v-model="quotation.tax_rate" placeholder="请选择税率" :disabled="isEdit">
        <el-option label="不含税 (0%)" :value="0" />
        <el-option label="3%" :value="0.03" />
        <el-option label="6%" :value="0.06" />
        <el-option label="13%" :value="0.13" />
        <el-option label="17%" :value="0.17" />
      </el-select>
    </el-form-item>
    <el-form-item label="对外利润率">
      <el-input-number
        v-model="quotation.profit_rate"
        :precision="2" :step="0.01" :min="0" :max="10"
        placeholder="如 0.15 表示 15%"
        @change="isEdit && saveProfitRate()"
      />
    </el-form-item>
    <el-form-item v-if="!isEdit">
      <QuotationEditSaveBar label="基本信息" :saving="savingBasic" @save="saveBasic">
        <template #button-text>创建报价单</template>
      </QuotationEditSaveBar>
    </el-form-item>
    <el-form-item v-else>
      <el-alert title="基本信息已保存，无法修改" type="info" :closable="false" show-icon />
    </el-form-item>
  </el-form>
</template>

<script setup>
import QuotationEditSaveBar from './QuotationEditSaveBar.vue'

const props = defineProps({
  quotation: { type: Object, required: true },
  formRules: { type: Object, required: true },
  isEdit: { type: Boolean, default: false },
  parentId: { type: [Number, String, null], default: null },
  savingBasic: { type: Boolean, default: false },
  businessUsers: { type: Array, default: () => [] },
  currencyOptions: { type: Array, default: () => [] },
  schemeHint: { type: String, default: '' },
  schemeHintType: { type: String, default: 'info' },
})

const emit = defineEmits([
  'save-basic',
  'save-profit-rate',
  'query-scheme-suggestions',
  'select-scheme',
  'scheme-input',
  'validate-scheme',
])

const querySchemeSuggestions = (cb, prefix) => emit('query-scheme-suggestions', cb, prefix)
const handleSelectScheme = (item) => emit('select-scheme', item)
const onSchemeInput = (val) => emit('scheme-input', val)
const validateSchemeLocally = () => emit('validate-scheme')
const saveBasic = () => emit('save-basic')
const saveProfitRate = () => emit('save-profit-rate')
</script>