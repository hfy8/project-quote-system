<template>
  <el-form :model="quotation" :rules="formRules" label-width="120px">
    <el-form-item label="报价单名称">
      <el-input v-model="quotation.name" placeholder="请输入报价单名称" :disabled="isEdit" />
    </el-form-item>
    <el-form-item label="项目类型">
      <el-select v-model="quotation.type" placeholder="请选择类型" :disabled="isEdit">
        <el-option label="单机 (single)" value="single" />
        <el-option label="线体 (line)" value="line" />
      </el-select>
    </el-form-item>
    <el-form-item label="方案编号" prop="scheme_no">
      <el-input v-model="quotation.scheme_no" placeholder="请输入方案编号" :disabled="isEdit" />
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
    <el-form-item v-if="isEdit">
      <el-alert title="基本信息已保存，无法修改" type="info" :closable="false" show-icon />
    </el-form-item>
  </el-form>
</template>

<script setup>
defineProps({
  quotation: { type: Object, required: true },
  formRules: { type: Object, default: () => ({}) },
  isEdit: { type: Boolean, default: false },
  businessUsers: { type: Array, default: () => [] },
  currencyOptions: { type: Array, default: () => [] },
})
</script>