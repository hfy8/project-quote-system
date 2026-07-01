<template>
  <div class="quotation-edit">
    <!-- 页面标题栏 -->
    <div class="page-header">
      <div class="page-header-left">
        <button class="back-btn" @click="goBack">←</button>
        <h1 class="page-title">{{ isEdit ? '编辑报价单' : '新建报价单' }}</h1>
        <span v-if="isEdit && quotation.name" class="page-title-sub">- {{ quotation.name }}</span>
      </div>
    </div>

    <!-- 主内容卡片 -->
    <div class="edit-card" v-loading="pageLoading" element-loading-text="页面加载中...">
      <el-tabs v-model="activeTab">
        <!-- 基本信息 -->
        <el-tab-pane label="基本信息" name="basic">
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
        </el-tab-pane>

        <!-- 模块管理 -->
        <el-tab-pane v-if="permissions.tabs?.includes('modules')" label="模块管理" name="modules">
          <div class="module-actions">
            <el-button type="primary" @click="showAddModule">添加模块</el-button>
            <el-button type="success" @click="showCopyModuleDialog">从其他报价单复制模块</el-button>
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
                <el-button size="small" @click="editModule(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteModule(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 添加/编辑模块弹窗 -->
          <el-dialog v-model="moduleDialogVisible" :title="moduleDialogTitle" width="500px">
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
                      v-for="t in MODULE_TYPES"
                      :key="t.value"
                      :value="t.value"
                    >
                      <span :style="{ color: t.color, fontWeight: 600 }">{{ t.label }}</span>
                    </el-radio-button>
                  </el-radio-group>
                  <el-button
                    v-if="currentParticipants.length > 0"
                    size="small"
                    @click="inferModuleType"
                    :title="`根据已选 ${currentParticipants.length} 个参与人员岗位自动推断`"
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
              <el-button @click="moduleDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="saveModule">确定</el-button>
            </template>
          </el-dialog>

          <!-- 复制模块弹窗 -->
          <el-dialog v-model="copyModuleDialogVisible" title="从其他报价单复制模块" width="800px" :close-on-click-modal="false">
            <el-form label-width="100px">
              <el-form-item label="选择报价单">
                <el-select
                  v-model="copyForm.sourceQuotationId"
                  placeholder="搜索报价单名称/方案号"
                  filterable
                  remote
                  :remote-method="searchQuotationsForCopy"
                  :loading="copyForm.searching"
                  style="width: 100%;"
                  @change="onCopySourceChange"
                >
                  <el-option
                    v-for="q in copyForm.quotationOptions"
                    :key="q.id"
                    :label="`#${q.id} ${q.name} (${q.scheme_no || '无方案号'})`"
                    :value="q.id"
                  />
                </el-select>
              </el-form-item>

              <el-form-item v-if="copyForm.sourceQuotationId" label="选择模块">
                <div style="width: 100%;">
                  <div style="margin-bottom: 8px;">
                    <el-button size="small" @click="selectAllCopyModules" :disabled="!copyForm.availableModules.length">
                      全选
                    </el-button>
                    <el-button size="small" @click="deselectAllCopyModules" :disabled="!copyForm.selectedModuleIds.length">
                      全不选
                    </el-button>
                    <span style="margin-left: 12px; color: #909399; font-size: 12px;">
                      已选 {{ copyForm.selectedModuleIds.length }} / {{ copyForm.availableModules.length }} 个模块
                    </span>
                  </div>
                  <el-table
                    :data="copyForm.availableModules"
                    border
                    max-height="300"
                    @selection-change="handleCopyModuleSelection"
                    v-loading="copyForm.loadingModules"
                  >
                    <el-table-column type="selection" width="50" />
                    <el-table-column prop="id" label="ID" width="60" />
                    <el-table-column prop="name" label="模块名称" />
                    <el-table-column prop="name_en" label="英文名称" />
                    <el-table-column label="物料数" width="80">
                      <template #default="{ row }">
                        {{ (row.materials || []).length }}
                      </template>
                    </el-table-column>
                    <el-table-column label="小计" width="100">
                      <template #default="{ row }">
                        ¥{{ Number(row.total || 0).toFixed(2) }}
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </el-form-item>

              <el-alert
                v-if="copyForm.sourceQuotationId"
                type="info"
                :closable="false"
                show-icon
                style="margin-top: 12px;"
              >
                <template #title>
                  <span style="font-size: 13px;">
                    确认后将复制所选模块到当前报价单
                    <strong style="color: #409EFF;">「{{ quotation?.name }}」</strong>
                    ，新模块将包含相同的名称和物料信息。
                  </span>
                </template>
              </el-alert>
            </el-form>

            <template #footer>
              <el-button @click="copyModuleDialogVisible = false">取消</el-button>
              <el-button
                type="primary"
                :disabled="!copyForm.selectedModuleIds.length"
                :loading="copyForm.submitting"
                @click="submitCopyModules"
              >
                确定复制 ({{ copyForm.selectedModuleIds.length }})
              </el-button>
            </template>
          </el-dialog>
        </el-tab-pane>

        <!-- 参与人员 -->
        <el-tab-pane v-if="permissions.tabs?.includes('participants')" label="参与人员" name="participants">
          <el-table :data="quotationParticipants" border style="width: 100%;">
            <el-table-column prop="user.real_name" label="姓名" />
            <el-table-column prop="user.username" label="用户名" />
            <el-table-column label="参与类型" width="150">
              <template #default="{ row }">
                <el-select v-model="row.participant_type" placeholder="选择类型" size="small" @change="updateParticipantType(row)">
                  <el-option label="项目" value="project" />
                  <el-option label="机构" value="agency" />
                  <el-option label="电气" value="electrical" />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100" align="center">
              <template #default="{ row }">
                <el-button size="small" type="danger" @click="removeQuotationParticipant(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 添加人员弹窗 -->
          <el-dialog v-model="addParticipantDialogVisible" title="添加人员" width="500px">
            <div class="add-participant-form">
              <el-input v-model="participantSearch" placeholder="搜索人员姓名或用户名" clearable style="width: 100%; margin-bottom: 16px;" />
              <el-table :data="filteredAvailableUsers" v-loading="participantLoading" border size="small" max-height="300" @selection-change="handleParticipantSelection">
                <el-table-column type="selection" width="50" :selectable="checkParticipantSelectable"></el-table-column>
                <el-table-column prop="real_name" label="姓名" />
                <el-table-column prop="username" label="用户名" />
              </el-table>
            </div>
            <template #footer>
              <el-button @click="addParticipantDialogVisible = false">取消</el-button>
              <el-button type="primary" :disabled="!selectedParticipantUsers.length" @click="addParticipantsConfirm">添加 ({{ selectedParticipantUsers.length }})</el-button>
            </template>
          </el-dialog>
        </el-tab-pane>

        <!-- 费用系数 -->
        <el-tab-pane v-if="permissions.tabs?.includes('coefficients')" label="费用系数" name="coefficients">
          <div class="coefficient-card">
            <div class="coefficient-header">
              <div class="coefficient-title">
                <span>费用系数配置</span>
              </div>
              <div class="coefficient-actions">
                <el-button size="small" @click="resetCoefficientsToDefault">重置为系统默认</el-button>
                <el-button type="primary" @click="saveCoefficients">保存配置</el-button>
              </div>
            </div>
            <div class="coefficient-desc">
              费用系数用于调整大件、核心部件、其他件的成本计算系数，仅影响当前报价单
            </div>
            <div class="coefficient-items">
              <div class="coefficient-item">
                <div class="coefficient-item-icon large"><span>大</span></div>
                <div class="coefficient-item-content">
                  <div class="coefficient-item-label">大件系数</div>
                  <div class="coefficient-item-tip">大型设备/材料成本系数</div>
                </div>
                <el-input-number v-model="quotation.coefficients.large" :min="0" :max="10" :precision="2" style="width: 140px;" />
              </div>
              <div class="coefficient-item">
                <div class="coefficient-item-icon standard"><span>通</span></div>
                <div class="coefficient-item-content">
                  <div class="coefficient-item-label">核心部件系数</div>
                  <div class="coefficient-item-tip">标准常规材料成本系数</div>
                </div>
                <el-input-number v-model="quotation.coefficients.standard" :min="0" :max="10" :precision="2" style="width: 140px;" />
              </div>
              <div class="coefficient-item">
                <div class="coefficient-item-icon other"><span>其</span></div>
                <div class="coefficient-item-content">
                  <div class="coefficient-item-label">其他件系数</div>
                  <div class="coefficient-item-tip">配件耗材等材料成本系数</div>
                </div>
                <el-input-number v-model="quotation.coefficients.other" :min="0" :max="10" :precision="2" style="width: 140px;" />
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- 物料清单 -->
        <el-tab-pane v-if="permissions.tabs?.includes('materials')" label="物料清单" name="materials">
          <!-- 已归档警告 -->
          <el-alert v-if="isArchived" title="报价单已归档，物料变更需要提交审核" type="warning" :closable="false" show-icon style="margin-bottom: 16px;">
            <template #default>
              您的物料变更申请将发送给报价单负责人审核，审核通过后才会生效。
              <el-button type="warning" size="small" style="margin-left: 16px;" @click="goToPendingReviews" v-if="pendingReviewCount > 0">
                查看待审核 ({{ pendingReviewCount }})
              </el-button>
            </template>
          </el-alert>
          
          <div class="material-actions">
            <el-select v-model="selectedModuleFilter" placeholder="全部模块" clearable style="width: 200px;">
              <el-option
                v-for="mod in modules"
                :key="mod.id"
                :label="mod.name"
                :value="mod.id"
              />
            </el-select>
          </div>

          <!-- 按模块分组显示物料 -->
          <div v-for="mod in filteredModuleGroups" :key="mod.id" class="module-group">
            <div class="module-group-header">
              <span class="module-name">{{ mod.name }}</span>
              <el-tag v-if="quotation.type === 'line' && mod.quotation_name" size="small" type="info" effect="plain" style="margin-left: 8px;">
                {{ mod.quotation_name }}
              </el-tag>
              <span class="module-material-count">{{ mod.materials.length }} 项物料</span>
              <span class="module-total">小计: {{ mod.total.toFixed(2) }} 元</span>
              <el-button type="primary" size="small" @click="showAddMaterialToModule(mod.id)">+ 添加物料</el-button>
            </div>
            <el-table :data="mod.materials" border style="width: 100%;" show-overflow-tooltip>
              <el-table-column prop="material_name" label="物料名称" min-width="100">
                <template #default="{ row }">{{ row.material_name || '-' }}</template>
              </el-table-column>
              <el-table-column prop="specification" label="规格" min-width="80">
                <template #default="{ row }">{{ row.specification || '-' }}</template>
              </el-table-column>
              <el-table-column prop="brand" label="品牌" width="70">
                <template #default="{ row }">{{ row.brand || '-' }}</template>
              </el-table-column>
              <el-table-column v-if="hasKeyFields" prop="param1" label="关键参数01" width="130">
                <template #default="{ row }"><span v-if="row.param1">{{ row.param1 }}</span></template>
              </el-table-column>
              <el-table-column v-if="hasKeyFields" prop="param2" label="关键参数02" width="130">
                <template #default="{ row }"><span v-if="row.param2">{{ row.param2 }}</span></template>
              </el-table-column>
              <el-table-column v-if="hasKeyFields" prop="param3" label="关键参数03" width="130">
                <template #default="{ row }"><span v-if="row.param3">{{ row.param3 }}</span></template>
              </el-table-column>
              <el-table-column prop="unit" label="单位" width="60">
                <template #default="{ row }">{{ row.unit || '-' }}</template>
              </el-table-column>
              <el-table-column prop="unit_price" label="单价" width="90">
                <template #default="{ row }">{{ (row.unit_price || 0).toFixed(2) }}</template>
              </el-table-column>
              <el-table-column label="数量" width="130">
                <template #default="{ row }">
                  <span v-if="row.is_other === true">{{ row.quantity }} {{ row.unit }} <span style="color:#999;font-size:12px">(不可改)</span></span>
                  <el-input-number
                    v-else
                    :model-value="row.quantity"
                    :min="1"
                    size="small"
                    controls-position="right"
                    @change="(val) => updateMaterialQuantity(row.id, val)"
                  />
                </template>
              </el-table-column>
              <el-table-column label="小计" width="100">
                <template #default="{ row }">
                  {{ ((row.unit_price || 0) * row.quantity).toFixed(2) }}
                </template>
              </el-table-column>
              <el-table-column label="添加人" width="80">
                <template #default="{ row }">
                  {{ row.selected_by_name || '-' }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="150" align="center">
                <template #default="{ row }">
                  <template v-if="row.is_other === true">
                    <el-button size="small" @click="editOtherMaterial(row)">改单价</el-button>
                    <el-button size="small" type="danger" @click="deleteModuleMaterial(row.id)">删除</el-button>
                  </template>
                  <el-button v-else size="small" type="danger" @click="deleteModuleMaterial(row.id)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>

          <!-- 全部模块合计 -->
          <div v-if="moduleMaterials.length > 0" class="material-summary total">
            <span>全部物料合计：{{ allMaterialsTotal.toFixed(2) }} 元</span>
          </div>

          <!-- 添加物料弹窗 -->
          <el-dialog v-model="materialDialogVisible" title="添加物料" width="1300px">
            <!-- 筛选栏 -->
            <div class="material-filter-bar">
              <el-input v-model="materialFilter.keyword" placeholder="搜索品名" clearable style="width: 140px;" />
              <el-select v-model="materialFilter.category" placeholder="分类" clearable style="width: 110px;">
                <el-option label="大件" value="large" />
                <el-option label="核心部件" value="standard" />
                <el-option label="其他件" value="other" />
              </el-select>
              <el-select v-model="materialFilter.brand" placeholder="品牌" clearable style="width: 110px;">
                <el-option v-for="b in availableBrands" :key="b" :label="b" :value="b" />
              </el-select>
            </div>

            <!-- 物料列表 -->
            <el-table
              :data="filteredAvailableMaterials"
              border
              style="width: 100%; margin-top: 12px;"
              max-height="400"
              show-overflow-tooltip
              @selection-change="handleMaterialSelection"
              ref="materialTableRef"
            >
              <el-table-column type="selection" width="45"></el-table-column>
              <el-table-column prop="name" label="品名" min-width="120" />
              <el-table-column prop="spec" label="规格" min-width="100" />
              <el-table-column prop="brand" label="品牌" width="70" />
              <el-table-column v-if="materialHasKeyParams" prop="param1" label="关键参数01" width="140">
                <template #default="{ row }"><span v-if="row.param1" class="key-param">{{ row.param1 }}</span></template>
              </el-table-column>
              <el-table-column v-if="materialHasKeyParams" prop="param2" label="关键参数02" width="140">
                <template #default="{ row }"><span v-if="row.param2" class="key-param">{{ row.param2 }}</span></template>
              </el-table-column>
              <el-table-column v-if="materialHasKeyParams" prop="param3" label="关键参数03" width="140">
                <template #default="{ row }"><span v-if="row.param3" class="key-param">{{ row.param3 }}</span></template>
              </el-table-column>
              <el-table-column prop="unit" label="单位" width="60" />
              <el-table-column prop="unit_price" label="单价" width="70" />
              <el-table-column label="分类" width="70">
                <template #default="{ row }">{{ getCategoryLabel(row.category) }}</template>
              </el-table-column>
              <el-table-column label="数量" width="120">
                <template #default="{ row }">
                  <span v-if="row.name === '其他'">1 <span style="color:#999;font-size:12px">(不可改)</span></span>
                  <el-input-number
                    v-else
                    v-model="row._quantity"
                    :min="1"
                    size="small"
                    controls-position="right"
                    :disabled="!selectedMaterials.includes(row)"
                  />
                </template>
              </el-table-column>
            </el-table>
            <template #footer>
              <el-button @click="materialDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="addMaterialsToModule">确定添加</el-button>
            </template>
          </el-dialog>

          <!-- 修改其他物料单价弹窗 -->
          <el-dialog v-model="otherPriceDialogVisible" title="修改其他物料单价" width="400px">
            <el-form :model="otherPriceForm" label-width="100px">
              <el-form-item label="物料名称">
                <el-input v-model="otherPriceForm.material_name" disabled />
              </el-form-item>
              <el-form-item label="单价">
                <el-input-number v-model="otherPriceForm.unit_price_override" :min="0" :precision="2" style="width: 100%;" />
              </el-form-item>
            </el-form>
            <template #footer>
              <el-button @click="otherPriceDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="saveOtherMaterialPrice">保存</el-button>
            </template>
          </el-dialog>
        </el-tab-pane>

        <!-- 费用 -->
        <el-tab-pane v-if="permissions.tabs?.includes('fees')" label="费用" name="fees">
          <div class="fee-actions">
            <el-button type="primary" @click="showAddFee">添加费用</el-button>
          </div>

          <el-table :data="fees" border style="width: 100%; margin-top: 16px;">
            <el-table-column prop="fee_type" label="费用类型" />
            <el-table-column prop="location" label="位置">
              <template #default="{ row }">
                {{ getLocationLabel(row.location) }}
              </template>
            </el-table-column>
            <el-table-column prop="amount" label="金额" />
            <el-table-column prop="description" label="描述" />
            <el-table-column label="操作" width="180">
              <template #default="{ row }">
                <el-button size="small" @click="editFee(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteFee(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 添加/编辑费用弹窗 -->
          <el-dialog v-model="feeDialogVisible" :title="feeDialogTitle" width="500px">
            <el-form :model="feeForm" label-width="100px">
              <el-form-item label="费用类型">
                <el-select v-model="feeForm.fee_type" placeholder="请选择费用类型">
                  <el-option v-for="ft in feeTypes" :key="ft.id" :label="ft.name" :value="ft.name" />
                </el-select>
              </el-form-item>
              <el-form-item label="位置">
                <el-select v-model="feeForm.location" placeholder="请选择位置" disabled>
                  <el-option label="厂内" value="internal" />
                  <el-option label="厂外" value="external" />
                </el-select>
                <div class="form-tip">位置由费用类型自动带出</div>
              </el-form-item>
              <el-form-item label="金额">
                <el-input-number v-model="feeForm.amount" :min="0" :precision="2" />
              </el-form-item>
              <el-form-item label="描述">
                <el-input v-model="feeForm.description" type="textarea" rows="3" placeholder="请输入描述" />
              </el-form-item>
            </el-form>
            <template #footer>
              <el-button @click="feeDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="saveFee">确定</el-button>
            </template>
          </el-dialog>
        </el-tab-pane>

        <!-- 人力工时 -->
        <el-tab-pane v-if="permissions.tabs?.includes('labor')" label="人力工时" name="labor">
          <div class="labor-header">
            <el-button type="primary" @click="showAddLabor">+ 添加工时</el-button>
          </div>

          <el-table :data="laborHours" border style="width: 100%; margin-top: 16px;">
            <el-table-column prop="name" label="名称" min-width="120">
              <template #default="{ row }">
                <el-input v-if="row._editing" v-model="row._name" size="small" placeholder="工时名称" />
                <span v-else>{{ row.name }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="hours" label="工时 (h)" width="120">
              <template #default="{ row }">
                <el-input-number v-if="row._editing" v-model="row._hours" :min="0" :precision="1" size="small" controls-position="right" style="width: 100px;" @change="onRowHoursChange(row)" />
                <span v-else>{{ row.hours }} h</span>
              </template>
            </el-table-column>
            <el-table-column prop="person_days" label="人天" width="120">
              <template #default="{ row }">
                <el-input-number v-if="row._editing" v-model="row._person_days" :min="0" :precision="2" size="small" controls-position="right" style="width: 100px;" @change="onRowPersonDaysChange(row)" />
                <span v-else>{{ formatPersonDays(row.hours) }} 人天</span>
              </template>
            </el-table-column>
            <el-table-column v-if="!isViewMode" prop="unit_price" label="单价 (元/h)" width="140">
              <template #default="{ row }">
                <el-input-number v-if="row._editing" v-model="row._unit_price" :min="0" :precision="2" size="small" controls-position="right" style="width: 110px;" />
                <span v-else>{{ row.unit_price.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column v-if="!isViewMode" prop="total" label="合计" width="120">
              <template #default="{ row }">{{ (row.hours * row.unit_price).toFixed(2) }}</template>
            </el-table-column>
            <el-table-column label="操作" width="150" align="center">
              <template #default="{ row }">
                <template v-if="row._editing">
                  <el-button size="small" type="primary" @click="saveLaborRow(row)">保存</el-button>
                  <el-button size="small" @click="cancelLaborEdit(row)">取消</el-button>
                </template>
                <template v-else>
                  <el-button size="small" @click="editLaborRow(row)">编辑</el-button>
                  <el-button size="small" type="danger" @click="deleteLabor(row.id)">删除</el-button>
                </template>
              </template>
            </el-table-column>
          </el-table>

          <div v-if="laborHours.length > 0 && !isViewMode" class="labor-total">
            人力费用合计：<strong>{{ laborTotal.toFixed(2) }} 元</strong>
            <span class="labor-total-days">（{{ formatPersonDays(laborHours.reduce((s, i) => s + (i.hours || 0), 0)) }} 人天）</span>
          </div>
          <div v-else-if="laborHours.length > 0 && isViewMode" class="labor-total">
            合计：<strong>{{ formatPersonDays(laborHours.reduce((s, i) => s + (i.hours || 0), 0)) }} 人天</strong>
          </div>

          <!-- 添加工时弹窗 -->
          <el-dialog v-model="laborDialogVisible" title="添加人力工时" width="500px">
            <el-form :model="laborForm" label-width="100px">
              <el-form-item label="名称">
                <el-input v-model="laborForm.name" placeholder="如：电气设计、现场调试" />
              </el-form-item>
              <el-form-item label="工时 (h)">
                <el-input-number v-model="laborForm.hours" :min="0" :precision="1" style="width: 100%;" @change="onHoursChange" />
              </el-form-item>
              <el-form-item label="人天">
                <el-input-number v-model="laborForm.person_days" :min="0" :precision="2" style="width: 100%;" @change="onPersonDaysChange" />
                <span class="form-hint">{{ HOURS_PER_DAY }} h = 1 人天</span>
              </el-form-item>
              <el-form-item label="单价 (元/h)" v-if="!isMyAssignments">
                <el-input-number v-model="laborForm.unit_price" :min="0" :precision="2" style="width: 100%;" />
              </el-form-item>
              <el-form-item label="合计" v-if="!isMyAssignments">
                <span>{{ (laborForm.hours * laborForm.unit_price).toFixed(2) }} 元</span>
                <span class="form-hint">（{{ laborForm.hours }} h = {{ formatPersonDays(laborForm.hours) }} 人天）</span>
              </el-form-item>
            </el-form>
            <template #footer>
              <el-button @click="laborDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="addLaborConfirm">确定</el-button>
            </template>
          </el-dialog>
        </el-tab-pane>


        <!-- 版本 -->
        <el-tab-pane v-if="permissions.tabs?.includes('versions')" label="版本" name="versions">
          <el-table :data="versions" border style="width: 100%;">
            <el-table-column prop="version_no" label="版本号" width="80" />
            <el-table-column prop="created_at" label="创建时间" />
            <el-table-column prop="creator_name" label="创建人" />
            <el-table-column prop="operation_type" label="操作类型" />
            <el-table-column prop="remark" label="备注" show-overflow-tooltip />
            <el-table-column label="操作" width="100" fixed="right">
              <template #default="{ row }">
                <el-button size="small" type="warning" @click="exportVersion(row, 'pdf')">PDF</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 运输包装 -->
        <el-tab-pane v-if="permissions.tabs?.includes('packing') && !isBoundChild" label="运输包装" name="packing">
          <div class="packing-header">
            <el-button type="primary" @click="showAddPackingEntry">+ 添加运输包装条目</el-button>
          </div>
          <el-table :data="packingEntries" border style="width: 100%; margin-top: 16px;">
                      <el-table-column prop="packing_type_name" label="运输包装类型" />
                      <el-table-column v-if="!isViewMode" prop="unit_price" label="单价（元/个）" width="150">
                        <template #default="{ row }">
                          <el-input-number v-if="row._editing" v-model="row._unit_price" :min="0" :precision="2" size="small" controls-position="right" style="width: 120px;" />
                          <span v-else class="money">¥{{ row.unit_price.toFixed(2) }}</span>
                        </template>
                      </el-table-column>
                      <el-table-column label="数量" width="160">
                        <template #default="{ row }">
                          <el-input-number v-if="row._editing" v-model="row._quantity" :min="0" :precision="2" size="small" controls-position="right" style="width: 120px;" />
                          <span v-else>{{ row.quantity }} {{ row.unit }}</span>
                        </template>
                      </el-table-column>
                      <el-table-column v-if="!isViewMode" label="小计" width="130">
                        <template #default="{ row }"><span class="money">¥{{ (row._editing ? row._unit_price : row.unit_price) * (row._editing ? row._quantity : row.quantity) }}</span></template>
                      </el-table-column>
                      <el-table-column prop="remark" label="备注" />
                      <el-table-column label="操作" width="150" align="center">
                        <template #default="{ row }">
                          <template v-if="row._editing">
                            <el-button size="small" type="primary" @click="savePackingRow(row)">保存</el-button>
                            <el-button size="small" @click="cancelPackingEdit(row)">取消</el-button>
                          </template>
                          <template v-else>
                            <el-button size="small" @click="editPackingRow(row)">编辑</el-button>
                                              <el-button size="small" type="danger" @click="deletePackingEntry(row.id)">删除</el-button>
                          </template>
                        </template>
                      </el-table-column>
                    </el-table>
          <div v-if="packingEntries.length > 0 && !isViewMode" class="labor-total">
            运输包装费用合计：<strong>¥{{ packingTotal.toFixed(2) }}</strong>
          </div>
          <el-dialog v-model="packingDialogVisible" title="添加运输包装条目" width="450px">
            <el-form :model="packingForm" label-width="110px">
              <el-form-item label="运输包装类型" required>
                <el-select v-model="packingForm.packing_type_id" placeholder="请选择" @change="onPackingTypeChange">
                  <el-option v-for="pt in packingTypes" :key="pt.id" :label="pt.name" :value="pt.id" />
                </el-select>
              </el-form-item>
              <el-form-item label="数量">
                <el-input-number v-model="packingForm.quantity" :min="0" :precision="2" style="width: 100%;" />
              </el-form-item>
              <el-form-item label="备注">
                <el-input v-model="packingForm.remark" placeholder="可选" />
              </el-form-item>
            </el-form>
            <template #footer>
              <el-button @click="packingDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="addPackingConfirm">确定</el-button>
            </template>
          </el-dialog>
        </el-tab-pane>

        <!-- 差旅人天 -->
        <el-tab-pane v-if="permissions.tabs?.includes('travel_person_days') && !isBoundChild" label="差旅人天" name="travel-days">
          <div class="packing-header">
            <el-button type="primary" @click="showAddTravelDaysEntry">+ 添加人天条目</el-button>
          </div>
          <el-table :data="travelPersonDays" border style="width: 100%; margin-top: 16px;">
            <el-table-column prop="travel_category_name" label="差旅分类" />
            <el-table-column v-if="!isViewMode" prop="unit_price" label="单价（元/人天）" width="150">
              <template #default="{ row }">
                <el-input-number v-if="row._editing" v-model="row._unit_price" :min="0" :precision="2" size="small" controls-position="right" style="width: 120px;" />
                <span v-else class="money">¥{{ row.unit_price.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="人天" width="160">
              <template #default="{ row }">
                <el-input-number v-if="row._editing" v-model="row._person_days" :min="0" :precision="2" size="small" controls-position="right" style="width: 120px;" />
                <span v-else>{{ row.person_days }} 人天</span>
              </template>
            </el-table-column>
            <el-table-column v-if="!isViewMode" label="小计" width="130">
              <template #default="{ row }"><span class="money">¥{{ (row._editing ? row._unit_price : row.unit_price) * (row._editing ? row._person_days : row.person_days) }}</span></template>
            </el-table-column>
            <el-table-column prop="remark" label="备注" />
            <el-table-column label="操作" width="150" align="center">
              <template #default="{ row }">
                <template v-if="row._editing">
                  <el-button size="small" type="primary" @click="saveTravelDaysRow(row)">保存</el-button>
                  <el-button size="small" @click="cancelTravelDaysEdit(row)">取消</el-button>
                </template>
                <template v-else>
                  <el-button size="small" @click="editTravelDaysRow(row)">编辑</el-button>
                  <el-button size="small" type="danger" @click="deleteTravelDaysEntry(row.id)">删除</el-button>
                </template>
              </template>
            </el-table-column>
          </el-table>
          <div v-if="travelPersonDays.length > 0 && !isViewMode" class="labor-total">
            差旅人天合计：<strong>¥{{ travelDaysTotal.toFixed(2) }}</strong>
          </div>
          <el-dialog v-model="travelDaysDialogVisible" title="添加差旅人天" width="450px">
            <el-form :model="travelDaysForm" label-width="120px">
              <el-form-item label="差旅分类" required>
                <el-select v-model="travelDaysForm.travel_category_id" placeholder="请选择" @change="onTravelCategoryChange">
                  <el-option v-for="c in travelCategories" :key="c.id" :label="c.name" :value="c.id" />
                </el-select>
              </el-form-item>
              <el-form-item label="人天">
                <el-input-number v-model="travelDaysForm.person_days" :min="0" :precision="2" style="width: 100%;" />
              </el-form-item>
              <el-form-item label="备注">
                <el-input v-model="travelDaysForm.remark" placeholder="可选" />
              </el-form-item>
            </el-form>
            <template #footer>
              <el-button @click="travelDaysDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="addTravelDaysConfirm">确定</el-button>
            </template>
          </el-dialog>
        </el-tab-pane>

        <!-- 差旅人次 -->
        <el-tab-pane v-if="permissions.tabs?.includes('travel_person_trips') && !isBoundChild" label="差旅人次" name="travel-trips">
          <div class="packing-header">
            <el-button type="primary" @click="showAddTravelTripEntry">+ 添加人次条目</el-button>
          </div>
          <el-table :data="travelPersonTrips" border style="width: 100%; margin-top: 16px;">
            <el-table-column prop="travel_category_name" label="差旅分类" />
            <el-table-column prop="travel_mode_name" label="出行方式" />
            <el-table-column v-if="!isViewMode" prop="unit_price" label="交通单价" width="130">
              <template #default="{ row }">
                <el-input-number v-if="row._editing" v-model="row._unit_price" :min="0" :precision="2" size="small" controls-position="right" style="width: 110px;" />
                <span v-else class="money">¥{{ row.unit_price.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column v-if="!isViewMode" prop="visa_fee" label="签证费" width="110">
              <template #default="{ row }">
                <el-input-number v-if="row._editing" v-model="row._visa_fee" :min="0" :precision="2" size="small" controls-position="right" style="width: 90px;" />
                <span v-else class="money">¥{{ row.visa_fee.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="人次" width="100">
              <template #default="{ row }">
                <el-input-number v-if="row._editing" v-model="row._person_count" :min="0" :precision="0" size="small" controls-position="right" style="width: 80px;" />
                <span v-else>{{ row.person_count }} 人</span>
              </template>
            </el-table-column>
            <el-table-column v-if="!isViewMode" label="小计" width="130">
              <template #default="{ row }"><span class="money">¥{{ ((row._editing ? row._unit_price : row.unit_price) + (row._editing ? row._visa_fee : row.visa_fee)) * (row._editing ? row._person_count : row.person_count) }}</span></template>
            </el-table-column>
            <el-table-column prop="remark" label="备注" />
            <el-table-column label="操作" width="150" align="center">
              <template #default="{ row }">
                <template v-if="row._editing">
                  <el-button size="small" type="primary" @click="saveTravelTripRow(row)">保存</el-button>
                  <el-button size="small" @click="cancelTravelTripEdit(row)">取消</el-button>
                </template>
                <template v-else>
                  <el-button size="small" @click="editTravelTripRow(row)">编辑</el-button>
                  <el-button size="small" type="danger" @click="deleteTravelTripEntry(row.id)">删除</el-button>
                </template>
              </template>
            </el-table-column>
          </el-table>
          <div v-if="travelPersonTrips.length > 0 && !isViewMode" class="labor-total">
            差旅人次合计：<strong>¥{{ travelTripsTotal.toFixed(2) }}</strong>
          </div>
          <el-dialog v-model="travelTripDialogVisible" title="添加差旅人次" width="500px">
            <el-form :model="travelTripForm" label-width="120px">
              <el-form-item label="差旅分类" required>
                <el-select v-model="travelTripForm.travel_category_id" placeholder="请选择" @change="onTripCategoryChange">
                  <el-option v-for="c in travelCategories" :key="c.id" :label="c.name" :value="c.id" />
                </el-select>
              </el-form-item>
              <el-form-item label="出行方式" required>
                <el-select v-model="travelTripForm.travel_mode_id" placeholder="请选择" @change="onTripModeChange">
                  <el-option v-for="m in travelModes" :key="m.id" :label="m.name" :value="m.id" />
                </el-select>
              </el-form-item>
              <el-form-item label="人次">
                <el-input-number v-model="travelTripForm.person_count" :min="0" :precision="0" style="width: 100%;" />
              </el-form-item>
              <el-form-item label="备注">
                <el-input v-model="travelTripForm.remark" placeholder="可选" />
              </el-form-item>
            </el-form>
            <template #footer>
              <el-button @click="travelTripDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="addTravelTripConfirm">确定</el-button>
            </template>
          </el-dialog>
        </el-tab-pane>
        <!-- 汇总 -->
        <el-tab-pane v-if="permissions.tabs?.includes('summary')" label="汇总" name="summary">
          <div v-loading="summaryLoading" ref="summaryRef" element-loading-text="页面加载中...">
            <div class="summary-header no-export">
              <div class="summary-currency">
                <span class="currency-label">显示货币：</span>
                <el-select v-model="selectedCurrency" style="width: 120px;">
                  <el-option v-for="rate in exchangeRates" :key="rate.currency" :label="rate.currency" :value="rate.currency" />
                </el-select>
                <span v-if="selectedCurrency !== 'CNY'" class="currency-note">
                  汇率：{{ getExchangeRate(selectedCurrency) }}，已转换
                </span>
              </div>
            </div>
            <div class="summary-layout" v-if="summary">
              <div class="summary-left">
                <div class="summary-card compact">
                  <div class="summary-label">物料合计</div>
                  <div class="summary-value">{{ summary.material_total?.toFixed(2) || '0.00' }}</div>
                </div>
                <div class="summary-card compact">
                  <div class="summary-label">物料合计(含系数)</div>
                  <div class="summary-value highlight">{{ summary.material_total_with_rates?.toFixed(2) || '0.00' }}</div>
                </div>
                <div class="summary-card compact">
                  <div class="summary-label">小计</div>
                  <div class="summary-value highlight">{{ summary.subtotal?.toFixed(2) || '0.00' }}</div>
                </div>
                <div class="summary-card compact">
                  <div class="summary-label">对外利润率</div>
                  <div class="summary-value">{{ ((summary.profit_rate || 0) * 100).toFixed(0) }}%</div>
                </div>
                <div class="summary-card compact">
                  <div class="summary-label">含利润小计</div>
                  <div class="summary-value">{{ summary.subtotal_with_profit?.toFixed(2) || '0.00' }}</div>
                </div>
                <div class="summary-card compact">
                  <div class="summary-label">实际利润</div>
                  <div class="summary-value highlight">
                    <span>{{ (summary.subtotal_with_profit - summary.material_total - summary.fees_total)?.toFixed(2) || '0.00' }}</span>
                    <span class="profit-pct">({{ (((summary.subtotal_with_profit - summary.material_total - summary.fees_total) / (summary.material_total + summary.fees_total)) * 100)?.toFixed(1) || '0.0' }}%)</span>
                  </div>
                </div>
                <div class="summary-card compact">
                  <div class="summary-label">税率</div>
                  <div class="summary-value">{{ (summary.tax_rate * 100)?.toFixed(0) || 0 }}%</div>
                </div>
                <div class="summary-card compact">
                  <div class="summary-label">税额</div>
                  <div class="summary-value">{{ summary.tax_amount?.toFixed(2) || '0.00' }}</div>
                </div>
              </div>
              <div class="summary-right">
                <div class="summary-card fees-card">
                  <div class="fees-card-header">
                    <span class="summary-label">费用合计</span>
                    <span class="fees-total highlight">{{ summary.fees_total?.toFixed(2) }}</span>
                  </div>
                  <div class="fees-list">
                    <div class="fees-row" v-if="summary.fee_total > 0">
                      <span>费用Tab</span>
                      <span>{{ summary.fee_total?.toFixed(2) }}</span>
                    </div>
                    <div class="fees-row" v-if="summary.labor_total > 0">
                      <span>人力合计</span>
                      <span>{{ summary.labor_total?.toFixed(2) }}</span>
                    </div>
                    <div class="fees-row" v-if="summary.packing_total > 0 && !isBoundChild">
                      <span>运输包装费</span>
                      <span>{{ summary.packing_total?.toFixed(2) }}</span>
                    </div>
                    <div class="fees-row" v-if="summary.travel_person_days_total > 0 && !isBoundChild">
                      <span>差旅住宿费</span>
                      <span>{{ summary.travel_person_days_total?.toFixed(2) }}</span>
                    </div>
                    <div class="fees-row" v-if="summary.travel_person_trips_total > 0 && !isBoundChild">
                      <span>差旅交通签证费</span>
                      <span>{{ summary.travel_person_trips_total?.toFixed(2) }}</span>
                    </div>
                  </div>
                </div>
                <div class="summary-card total">
                  <div class="summary-label">最终报价</div>
                  <div class="summary-value large">
                    {{ convertedSummary?.grand_total?.toFixed(2) || '0.00' }} {{ selectedCurrency }}
                  </div>
                </div>
              </div>
            </div>

            <!-- 占比分析 -->
            <div v-if="summary" class="breakdown-section">
              <h3 class="section-title">📊 占比分析（基于含利润小计）</h3>

              <div class="ratio-cards">
                <div class="ratio-card">
                  <div class="ratio-label">🔧 硬件成本</div>
                  <div class="ratio-value highlight">¥{{ summary.material_total_with_rates?.toFixed(2) || '0.00' }}</div>
                  <div class="ratio-percent">{{ getRatio(summary.material_total_with_rates) }}%</div>
                  <div class="ratio-bar">
                    <div class="ratio-bar-fill material" :style="{ width: getRatio(summary.material_total_with_rates) + '%' }"></div>
                  </div>
                </div>
                <div class="ratio-card">
                  <div class="ratio-label">👷 人力工时</div>
                  <div class="ratio-value highlight">¥{{ summary.labor_total?.toFixed(2) || '0.00' }}</div>
                  <div class="ratio-percent">{{ getRatio(summary.labor_total) }}%</div>
                  <div class="ratio-bar">
                    <div class="ratio-bar-fill labor" :style="{ width: getRatio(summary.labor_total) + '%' }"></div>
                  </div>
                </div>
                <div class="ratio-card">
                  <div class="ratio-label">✈️ 运输+差旅</div>
                  <div class="ratio-value highlight">¥{{ totalTravelAmount?.toFixed(2) || '0.00' }}</div>
                  <div class="ratio-percent">{{ getRatio(totalTravelAmount) }}%</div>
                  <div class="ratio-bar">
                    <div class="ratio-bar-fill travel" :style="{ width: getRatio(totalTravelAmount) + '%' }"></div>
                  </div>
                </div>
                <div class="ratio-card">
                  <div class="ratio-label">💰 利润</div>
                  <div class="ratio-value highlight">¥{{ summary.profit_amount?.toFixed(2) || ((summary.subtotal_with_profit || 0) - (summary.subtotal || 0)).toFixed(2) }}</div>
                  <div class="ratio-percent">{{ getRatio((summary.subtotal_with_profit || 0) - (summary.subtotal || 0)) }}%</div>
                  <div class="ratio-bar">
                    <div class="ratio-bar-fill profit" :style="{ width: getRatio((summary.subtotal_with_profit || 0) - (summary.subtotal || 0)) + '%' }"></div>
                  </div>
                </div>
                <div class="ratio-card">
                  <div class="ratio-label">🧾 税额</div>
                  <div class="ratio-value highlight">¥{{ summary.tax_amount?.toFixed(2) || '0.00' }}</div>
                  <div class="ratio-percent">{{ getRatio(summary.tax_amount) }}%</div>
                  <div class="ratio-bar">
                    <div class="ratio-bar-fill tax" :style="{ width: getRatio(summary.tax_amount) + '%' }"></div>
                  </div>
                </div>
              </div>

              <div v-if="summary.rate_details && summary.rate_details.length > 0" class="hardware-structure">
                <h4 class="section-subtitle">🔩 硬件成本结构</h4>
                <div class="hardware-cards">
                  <div
                    v-for="row in summary.rate_details"
                    :key="row.category"
                    class="hardware-card"
                    :class="'cat-' + row.category"
                  >
                    <div class="hardware-label">
                      <span class="dot"></span>
                      {{ getCategoryLabel(row.category) }}
                    </div>
                    <div class="hardware-amount">¥{{ row.with_rate?.toFixed(2) || '0.00' }}</div>
                    <div class="hardware-percent">
                      {{ getMaterialCategoryRatio(row.with_rate) }}% <span class="ratio-of">of 硬件</span>
                    </div>
                    <div class="hardware-bar">
                      <div class="hardware-bar-fill" :style="{ width: getMaterialCategoryRatio(row.with_rate) + '%' }"></div>
                    </div>
                    <div class="hardware-meta">系数 {{ row.rate }}x · 原价 ¥{{ row.base?.toFixed(2) }}</div>
                  </div>
                </div>
                <div class="hardware-stacked-bar">
                  <div
                    v-for="row in summary.rate_details"
                    :key="'stack-' + row.category"
                    class="stacked-segment"
                    :class="'cat-' + row.category"
                    :style="{ width: getMaterialCategoryRatio(row.with_rate) + '%' }"
                    :title="`${getCategoryLabel(row.category)}: ¥${row.with_rate?.toFixed(2)} (${getMaterialCategoryRatio(row.with_rate)}%)`"
                  ></div>
                </div>
              </div>
            </div>

            <!-- 费用系数详情 -->
            <div v-if="summary?.rate_details?.length > 0" class="rate-details">
              <h4>费用系数明细</h4>
              <el-table :data="summary.rate_details" border size="small">
                <el-table-column label="分类" width="100">
                  <template #default="{ row }">{{ getCategoryLabel(row.category) }}</template>
                </el-table-column>
                <el-table-column prop="rate" label="系数" width="80">
                  <template #default="{ row }">{{ row.rate }}x</template>
                </el-table-column>
                <el-table-column prop="base" label="原价" width="120">
                  <template #default="{ row }">{{ row.base?.toFixed(2) }}</template>
                </el-table-column>
                <el-table-column prop="with_rate" label="系数后">
                  <template #default="{ row }">{{ row.with_rate?.toFixed(2) }}</template>
                </el-table-column>
              </el-table>
            </div>

            <h3 style="margin-top: 24px;">模块汇总</h3>
            <el-table :data="summary?.modules" border style="width: 100%; margin-top: 8px;">
              <el-table-column prop="module_name" label="模块名称" />
              <el-table-column prop="material_count" label="物料数量" width="100" />
              <el-table-column label="物料小计" width="120">
                <template #default="{ row }">
                  {{ row.material_amount?.toFixed(2) || '0.00' }}
                </template>
              </el-table-column>
              <el-table-column label="含系数小计" width="130">
                <template #default="{ row }">
                  {{ row.material_amount_with_rate?.toFixed(2) || row.material_amount?.toFixed(2) || '0.00' }}
                </template>
              </el-table-column>
            </el-table>

            <h3 style="margin-top: 24px;">费用明细</h3>
            <el-table :data="summary?.fees" border style="width: 100%; margin-top: 8px;">
              <el-table-column prop="fee_type" label="费用类型" />
              <el-table-column prop="location" label="位置">
                <template #default="{ row }">{{ getLocationLabel(row.location) }}</template>
              </el-table-column>
              <el-table-column prop="amount" label="金额" />
              <el-table-column prop="description" label="描述" />
            </el-table>

            <div class="export-grid no-export" style="margin-top: 24px;">
              <div class="export-item" @click="exportSummaryAsPDF">
                <span class="export-icon">🖼️</span>
                <span class="export-label">导出汇总 PDF（按网页）</span>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- 导出 -->
        <el-tab-pane v-if="permissions.tabs?.includes('export')" label="导出" name="export">
          <div class="export-grid">
            <div class="export-item" @click="exportFile('word')">
              <span class="export-icon">📝</span>
              <span class="export-label">导出 Word</span>
            </div>
            <div class="export-item" @click="exportFile('excel')">
              <span class="export-icon">📊</span>
              <span class="export-label">导出 Excel</span>
            </div>
            <div class="export-item" @click="exportFile('pdf')">
              <span class="export-icon">📄</span>
              <span class="export-label">导出 PDF</span>
            </div>
            <div class="export-item" @click="exportSummaryAsPDF">
              <span class="export-icon">🖼️</span>
              <span class="export-label">导出汇总 PDF（按网页）</span>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../api/request'
import { openDownload } from '../utils/download'
import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'
import { feesAPI, packingTypeAPI, travelCategoryAPI, travelModeAPI, travelPersonTripFeeAPI } from '../api'
import { packingEntryAPI, travelPersonDaysAPI, travelPersonTripAPI } from '../api/travel_entries'
import changeRequestsAPI from '../api/changeRequests'

const route = useRoute()
const router = useRouter()
const isMyAssignments = computed(() => route.path.includes('/my-assignments/'))

console.log('Route params:', route.params)
console.log('Route path:', route.path)

// 判断是新建还是编辑
const isEdit = computed(() => !!route.params.id && route.params.id !== 'new')
const quotationId = ref(route.params.id || null)
console.log('isEdit:', isEdit.value, 'quotationId:', quotationId.value)
const activeTab = ref('basic')
const quotation = ref({})
const isViewMode = computed(() => route.path.includes('/my-assignments/'))
const isArchived = computed(() => quotation.value.status === 'approved')
const hasKeyFields = computed(() => {
  return modules.value.some(mod =>
    mod.materials && mod.materials.some(m => m.param1 || m.param2 || m.param3)
  )
})
const materialHasKeyParams = computed(() => {
  return availableMaterials.value.some(m => m.param1 || m.param2 || m.param3)
})
const pendingReviewCount = ref(0)
const permissions = ref({
  can_edit_coefficients: false,
  can_edit_participants: false,
  can_edit_materials: false,
  can_edit_modules: false,
  can_edit_fees: false,
  tabs: []
})
// 子报价单绑定了父报价单（parent_id 不为 null）
const isBoundChild = computed(() => !!quotation.value?.parent_id)
const modules = ref([])
const moduleMaterials = ref([])
const fees = ref([])
const summary = ref(null)
const versions = ref([])
const laborHours = ref([])
const users = ref([])
const businessUsers = ref([])
const feeTypes = ref([])
const availableMaterials = ref([])

const packingTypes = ref([])
const travelCategories = ref([])
const travelModes = ref([])
const packingEntries = ref([])
const travelPersonDays = ref([])
const travelPersonTrips = ref([])

const selectedModuleId = ref(null)
const pageLoading = ref(true)
const summaryLoading = ref(false)

// 货币切换 - 默认使用报价单币种
const selectedCurrency = ref('CNY')
const exchangeRates = ref([])

// 币种选项 - 来自汇率配置
const currencyOptions = computed(() => {
  const options = [{ label: '人民币 (CNY)', value: 'CNY' }]
  // 从汇率配置中添加其他币种
  const extraCurrencies = {
    'USD': '美元 (USD)',
    'EUR': '欧元 (EUR)',
    'HKD': '港元 (HKD)',
    'GBP': '英镑 (GBP)',
    'JPY': '日元 (JPY)',
  }
  exchangeRates.value.forEach(rate => {
    if (rate.currency !== 'CNY' && extraCurrencies[rate.currency]) {
      options.push({ label: extraCurrencies[rate.currency], value: rate.currency })
    }
  })
  return options
})
const currencyCache = ref({})

function getExchangeRate(currency) {
  if (currency === 'CNY') return 1
  const rate = exchangeRates.value.find(r => r.currency === currency)
  return rate ? rate.rate : 1
}

function convertCurrency(amount, fromCurrency = 'CNY') {
  if (fromCurrency === selectedCurrency.value) return amount
  const fromRate = fromCurrency === 'CNY' ? 1 : getExchangeRate(fromCurrency)
  const toRate = selectedCurrency.value === 'CNY' ? 1 : getExchangeRate(selectedCurrency.value)
  return amount / fromRate * toRate
}

const getCategoryLabel = (cat) => {
  const map = { large: '大件', standard: '核心部件', other: '其他件' }
  return map[cat] || cat || '-'
}

const getLocationLabel = (loc) => {
  const map = { internal: '厂内', external: '厂外' }
  return map[loc] || loc || '-'
}

// 汇率转换后的汇总计算（只转换最终报价，其他显示CNY原值）
const convertedSummary = computed(() => {
  if (!summary.value) return null
  const rate = getExchangeRate(selectedCurrency.value)
  // rate 是 "1 目标货币 = rate CNY"，所以转换是除以 rate
  // 例如 700 CNY，USD汇率 7（1 USD = 7 CNY），则 700/7 = $100
  const factor = selectedCurrency.value === 'CNY' ? 1 : 1 / rate

  return {
    ...summary.value,
    grand_total: summary.value.grand_total * factor
  }
})

async function loadExchangeRates(skipCurrencyInit = false) {
  try {
    const [ratesRes, baseRes] = await Promise.all([
      api.get('/exchange_rates'),
      api.get('/exchange_rates/base')
    ])
    exchangeRates.value = Array.isArray(ratesRes) ? ratesRes : (ratesRes.items || [])
    // 只有在未跳过货币初始化且当前未设置报价单币种时，才设置默认货币
    if (!skipCurrencyInit && !quotation.value?.currency) {
      selectedCurrency.value = baseRes.currency || 'CNY'
    }
  } catch (error) {
    console.error('加载汇率失败', error)
  }
}

// 表单验证规则
const formRules = {
  name: [{ required: true, message: '请输入报价单名称', trigger: 'blur' }],
  scheme_no: [{ required: true, message: '请输入方案编号', trigger: 'blur' }],
  type: [{ required: true, message: '请选择项目类型', trigger: 'change' }]
}

// 模块弹窗
const moduleDialogVisible = ref(false)
const moduleDialogTitle = ref('添加模块')
const MODULE_TYPES = [
  { value: 'mechanical', label: '机构', color: '#3b82f6' },
  { value: 'electrical', label: '电气', color: '#f59e0b' },
  { value: 'other', label: '其他', color: '#94a3b8' },
]
const moduleForm = reactive({
  id: null,
  name: '',
  name_en: '',
  description: '',
  module_type: 'other',
})

// ============== 复制模块弹窗 ==============
const copyModuleDialogVisible = ref(false)
const copyForm = reactive({
  sourceQuotationId: null,
  quotationOptions: [],   // 远程搜索结果
  availableModules: [],   // 源报价单的模块列表
  selectedModuleIds: [],  // 选中的模块 ID
  searching: false,        // 搜索报价单中
  loadingModules: false,   // 加载模块中
  submitting: false,       // 提交复制中
})

// 物料弹窗
const materialDialogVisible = ref(false)
const addMaterialQuantity = ref(1)
const selectedMaterials = ref([])
const materialTableRef = ref(null)
const materialFilter = reactive({
  keyword: '',
  category: '',
  brand: ''
})

// 改单价相关（其他物料）
const otherMaterial = computed(() => {
  return availableMaterials.value?.find(m => m.name === '其他')
})

const otherPriceDialogVisible = ref(false)
const otherPriceForm = reactive({
  id: null,
  material_name: '其他',
  unit_price_override: 0
})

// 计算属性：过滤后的可选物料
const filteredAvailableMaterials = computed(() => {
  let list = availableMaterials.value || []
  if (materialFilter.keyword) {
    list = list.filter(m => m.name && m.name.toLowerCase().includes(materialFilter.keyword.toLowerCase()))
  }
  if (materialFilter.category) {
    list = list.filter(m => m.category === materialFilter.category)
  }
  if (materialFilter.brand) {
    list = list.filter(m => m.brand === materialFilter.brand)
  }
  return list
})

// 计算属性：可选品牌列表
const availableBrands = computed(() => {
  const brands = new Set()
  availableMaterials.value.forEach(m => {
    if (m.brand) brands.add(m.brand)
  })
  return Array.from(brands).sort()
})

// 计算属性：模块物料合计
const moduleMaterialsTotal = computed(() => {
  return moduleMaterials.value.reduce((sum, m) => {
    return sum + (m.unit_price || 0) * m.quantity
  }, 0)
})

// 模块过滤
const selectedModuleFilter = ref(null)

// 计算属性：按模块分组的物料
const filteredModuleGroups = computed(() => {
  let mods = modules.value
  if (selectedModuleFilter.value) {
    mods = mods.filter(m => m.id === selectedModuleFilter.value)
  }
  return mods.map(mod => {
    const matList = moduleMaterials.value.filter(mm => mm.module_id === mod.id)
    return {
      id: mod.id,
      name: mod.name,
      quotation_name: mod.quotation_name || null,
      materials: matList,
      total: matList.reduce((sum, m) => sum + (m.unit_price || 0) * m.quantity, 0)
    }
  })
})

// 计算属性：全部物料总计
const allMaterialsTotal = computed(() => {
  return moduleMaterials.value.reduce((sum, m) => {
    return sum + (m.unit_price || 0) * m.quantity
  }, 0)
})

// 获取用户名
const getUserName = (userId) => {
  if (!userId) return '-'
  const user = users.value.find(u => u.id === userId)
  return user ? user.name : userId
}

// 参与人员管理
const participantDialogVisible = ref(false)
const addParticipantDialogVisible = ref(false)
const quotationParticipants = ref([])
const currentParticipants = ref([])
const selectedParticipantUsers = ref([])
const participantSearch = ref('')
const currentModuleId = ref(null)
const participantLoading = ref(false)

// 计算属性：返回已加载的用户（搜索后由后端返回）
const filteredAvailableUsers = computed(() => {
  const currentUserIds = currentParticipants.value.map(p => p.user_id)
  return users.value.filter(u => !currentUserIds.includes(u.id))
})

// 搜索用户（防抖）
let participantSearchTimer = null
watch(participantSearch, (newVal) => {
  if (participantSearchTimer) clearTimeout(participantSearchTimer)
  participantSearchTimer = setTimeout(() => {
    loadUsers()
  }, 300)
})

// 管理参与人员
async function manageParticipants(module) {
  currentModuleId.value = module.id
  participantSearch.value = ''
  selectedParticipantUsers.value = []
  try {
    const data = await api.get(`/modules/${module.id}/participants`)
    currentParticipants.value = data || []
    participantDialogVisible.value = true
  } catch (error) {
    ElMessage.error('加载参与人员失败')
  }
}

// 显示添加人员弹窗
async function showAddParticipantDialog() {
  participantSearch.value = ''
  selectedParticipantUsers.value = []
  // 加载报价单已有参与人
  if (quotationId.value) {
    try {
      const data = await api.get(`/quotations/${quotationId.value}/participants`)
      quotationParticipants.value = data || []
      currentParticipants.value = quotationParticipants.value
    } catch (error) {
      console.error('加载参与人员失败', error)
    }
  }
  await loadUsers()  // 加载用户列表
  addParticipantDialogVisible.value = true
}

// 检查用户是否可选择（已参与不可选）
function checkParticipantSelectable(row) {
  const currentUserIds = currentParticipants.value.map(p => p.user_id)
  return !currentUserIds.includes(row.id)
}

// 处理选择变化
function handleParticipantSelection(selection) {
  selectedParticipantUsers.value = selection
}

// 确认添加人员
async function addParticipantsConfirm() {
  if (!selectedParticipantUsers.value.length) return
  try {
    for (const user of selectedParticipantUsers.value) {
      await api.post(`/quotations/${quotationId.value}/participants`, {
        user_id: user.id,
        participant_type: 'project'
      })
    }
    ElMessage.success('添加成功')
    addParticipantDialogVisible.value = false
    // 重新加载参与人
    const data = await api.get(`/quotations/${quotationId.value}/participants`)
    quotationParticipants.value = data || []
    currentParticipants.value = quotationParticipants.value
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

// 更新参与人类型
async function updateParticipantType(row) {
  try {
    await api.put(`/quotations/${quotationId.value}/participants/${row.user_id}`, {
      participant_type: row.participant_type
    })
    ElMessage.success('类型已更新')
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

// 移除报价单参与人
async function removeQuotationParticipant(participantId) {
  try {
    const participant = quotationParticipants.value.find(p => p.id === participantId)
    if (!participant) return
    await api.delete(`/quotations/${quotationId.value}/participants/${participant.user_id}`)
    ElMessage.success('移除成功')
    quotationParticipants.value = quotationParticipants.value.filter(p => p.id !== participantId)
    currentParticipants.value = quotationParticipants.value
  } catch (error) {
    ElMessage.error('移除失败')
  }
}

// 保存费用系数
async function saveCoefficients() {
  try {
    await api.put(`/quotations/${quotationId.value}`, {
      coefficients: quotation.value.coefficients
    })
    ElMessage.success('费用系数已保存')
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 重置为系统默认系数
async function resetCoefficientsToDefault() {
  try {
    const data = await api.get('/fee_rates')
    const rates = {}
    ;(data || []).forEach(r => { rates[r.category] = r.rate })
    quotation.value.coefficients = {
      large: rates.large ?? 1.0,
      standard: rates.standard ?? 1.0,
      other: rates.other ?? 1.0
    }
    ElMessage.success('已恢复系统默认系数')
  } catch (error) {
    quotation.value.coefficients = { large: 1.0, standard: 1.0, other: 1.0 }
    ElMessage.warning('获取系统系数失败，已重置为1.0')
  }
}

// 人力工时
const laborDialogVisible = ref(false)
// 8 工时 = 1 人天 (标准 1 天 8 小时)
const HOURS_PER_DAY = 8
const laborForm = reactive({
  name: '',
  hours: 0,         // 工时 (实际存储)
  person_days: 0,   // 人天 (前端展示,双向换算)
  unit_price: 0,
})

const laborTotal = computed(() => {
  return laborHours.value.reduce((sum, item) => sum + (item.hours || 0) * (item.unit_price || 0), 0)
})

// 人天 ↔ 工时 双向换算
function formatPersonDays(hours) {
  if (!hours) return '0.00'
  return (hours / HOURS_PER_DAY).toFixed(2)
}
function onHoursChange(val) {
  if (val == null) val = 0
  laborForm.person_days = +(val / HOURS_PER_DAY).toFixed(2)
}
function onPersonDaysChange(val) {
  if (val == null) val = 0
  laborForm.hours = +(val * HOURS_PER_DAY).toFixed(1)
}
function onRowHoursChange(row) {
  if (row._hours == null) row._hours = 0
  row._person_days = +(row._hours / HOURS_PER_DAY).toFixed(2)
}
function onRowPersonDaysChange(row) {
  if (row._person_days == null) row._person_days = 0
  row._hours = +(row._person_days * HOURS_PER_DAY).toFixed(1)
}

// ===== 运输包装 =====
const packingDialogVisible = ref(false)
const packingForm = reactive({ packing_type_id: null, unit_price: 0, quantity: 0, remark: '' })

async function loadPackingTypes() {
  try {
    const res = await packingTypeAPI.getList()
    packingTypes.value = Array.isArray(res) ? res : (res.items || [])
  } catch (e) { console.error(e) }
}

function onPackingTypeChange(id) {
  const pt = packingTypes.value.find(p => p.id === id)
  packingForm.unit_price = pt ? (pt.unit_price || 0) : 0
}

function showAddPackingEntry() {
  packingForm.packing_type_id = null
  packingForm.unit_price = 0
  packingForm.quantity = 0
  packingForm.remark = ''
  packingDialogVisible.value = true
  loadPackingTypes()
}

async function addPackingConfirm() {
  if (!packingForm.packing_type_id || !packingForm.quantity) return
  try {
    await packingEntryAPI.create(quotationId.value, {
      packing_type_id: packingForm.packing_type_id,
      quantity: packingForm.quantity,
      unit_price: packingForm.unit_price,
      remark: packingForm.remark
    })
    ElMessage.success('添加成功')
    packingDialogVisible.value = false
    loadPackingEntries()
  } catch (e) { ElMessage.error('添加失败') }
}

async function loadPackingEntries() {
  if (!quotationId.value) return
  try {
    const data = await packingEntryAPI.getByQuotation(quotationId.value)
    packingEntries.value = (data || []).map(e => ({ ...e, _editing: false }))
  } catch (e) { console.error(e) }
}

function editPackingRow(row) { row._editing = true; row._quantity = row.quantity; row._unit_price = row.unit_price }
function cancelPackingEdit(row) { row._editing = false }
async function savePackingRow(row) {
  try {
    await packingEntryAPI.update(row.id, { quantity: row._quantity, unit_price: row._unit_price, remark: row.remark })
    ElMessage.success('保存成功')
    loadPackingEntries()
  } catch (e) { ElMessage.error('保存失败') }
}
async function deletePackingEntry(id) {
  try { await packingEntryAPI.delete(id); ElMessage.success('删除成功'); loadPackingEntries() } catch (e) { ElMessage.error('删除失败') }
}

const packingTotal = computed(() => packingEntries.value.reduce((s, r) => s + (r.subtotal || 0), 0))

// ===== 差旅人天 =====
const travelDaysDialogVisible = ref(false)
const travelDaysForm = reactive({ travel_category_id: null, unit_price: 0, person_days: 0, remark: '' })

async function loadTravelCategories() {
  try {
    const res = await travelCategoryAPI.getList()
    travelCategories.value = Array.isArray(res) ? res : (res.items || [])
  } catch (e) { console.error(e) }
}

function onTravelCategoryChange(id) {
  const c = travelCategories.value.find(x => x.id === id)
  travelDaysForm.unit_price = c ? (c.unit_price || 0) : 0
}

function showAddTravelDaysEntry() {
  travelDaysForm.travel_category_id = null
  travelDaysForm.unit_price = 0
  travelDaysForm.person_days = 0
  travelDaysForm.remark = ''
  travelDaysDialogVisible.value = true
  loadTravelCategories()
}

async function addTravelDaysConfirm() {
  if (!travelDaysForm.travel_category_id || !travelDaysForm.person_days) return
  try {
    await travelPersonDaysAPI.create(quotationId.value, {
      travel_category_id: travelDaysForm.travel_category_id,
      person_days: travelDaysForm.person_days,
      unit_price: travelDaysForm.unit_price,
      remark: travelDaysForm.remark
    })
    ElMessage.success('添加成功')
    travelDaysDialogVisible.value = false
    loadTravelPersonDays()
  } catch (e) { ElMessage.error('添加失败') }
}

async function loadTravelPersonDays() {
  if (!quotationId.value) return
  try {
    const data = await travelPersonDaysAPI.getByQuotation(quotationId.value)
    travelPersonDays.value = (data || []).map(e => ({ ...e, _editing: false }))
  } catch (e) { console.error(e) }
}

function editTravelDaysRow(row) { row._editing = true; row._person_days = row.person_days; row._unit_price = row.unit_price }
function cancelTravelDaysEdit(row) { row._editing = false }
async function saveTravelDaysRow(row) {
  try {
    await travelPersonDaysAPI.update(row.id, { person_days: row._person_days, unit_price: row._unit_price, remark: row.remark })
    ElMessage.success('保存成功')
    loadTravelPersonDays()
  } catch (e) { ElMessage.error('保存失败') }
}
async function deleteTravelDaysEntry(id) {
  try { await travelPersonDaysAPI.delete(id); ElMessage.success('删除成功'); loadTravelPersonDays() } catch (e) { ElMessage.error('删除失败') }
}

const travelDaysTotal = computed(() => travelPersonDays.value.reduce((s, r) => s + (r.subtotal || 0), 0))

// ===== 差旅人次 =====
const travelTripDialogVisible = ref(false)
const travelTripForm = reactive({ travel_category_id: null, travel_mode_id: null, unit_price: 0, visa_fee: 0, person_count: 0, remark: '', _subtotal: 0 })

async function loadTravelModes() {
  try {
    const res = await travelModeAPI.getList()
    travelModes.value = Array.isArray(res) ? res : (res.items || [])
  } catch (e) { console.error(e) }
}

function onTripCategoryChange(id) {
  const c = travelCategories.value.find(x => x.id === id)
  travelTripForm.unit_price = c ? (c.unit_price || 0) : 0
  travelTripForm.visa_fee = c ? (c.visa_fee || 0) : 0
  computeTripSubtotal()
}

function onTripModeChange(id) { computeTripSubtotal() }

function computeTripSubtotal() {
  travelTripForm._subtotal = (travelTripForm.unit_price + travelTripForm.visa_fee) * (travelTripForm.person_count || 0)
}

watch(() => [travelTripForm.person_count, travelTripForm.unit_price, travelTripForm.visa_fee], computeTripSubtotal)

Object.defineProperty(travelTripForm, 'subtotal', { get: () => travelTripForm._subtotal })

function showAddTravelTripEntry() {
  Object.assign(travelTripForm, { travel_category_id: null, travel_mode_id: null, unit_price: 0, visa_fee: 0, person_count: 0, remark: '', _subtotal: 0 })
  travelTripDialogVisible.value = true
  loadTravelCategories()
  loadTravelModes()
}

async function addTravelTripConfirm() {
  if (!travelTripForm.travel_category_id || !travelTripForm.travel_mode_id || !travelTripForm.person_count) return
  try {
    await travelPersonTripAPI.create(quotationId.value, {
      travel_category_id: travelTripForm.travel_category_id,
      travel_mode_id: travelTripForm.travel_mode_id,
      person_count: travelTripForm.person_count,
      unit_price: travelTripForm.unit_price,
      visa_fee: travelTripForm.visa_fee,
      remark: travelTripForm.remark
    })
    ElMessage.success('添加成功')
    travelTripDialogVisible.value = false
    loadTravelPersonTrips()
  } catch (e) { ElMessage.error('添加失败') }
}

async function loadTravelPersonTrips() {
  if (!quotationId.value) return
  try {
    const data = await travelPersonTripAPI.getByQuotation(quotationId.value)
    travelPersonTrips.value = (data || []).map(e => ({ ...e, _editing: false }))
  } catch (e) { console.error(e) }
}

function editTravelTripRow(row) { row._editing = true; row._person_count = row.person_count; row._unit_price = row.unit_price; row._visa_fee = row.visa_fee }
function cancelTravelTripEdit(row) { row._editing = false }
async function saveTravelTripRow(row) {
  try {
    await travelPersonTripAPI.update(row.id, { person_count: row._person_count, unit_price: row._unit_price, visa_fee: row._visa_fee, remark: row.remark })
    ElMessage.success('保存成功')
    loadTravelPersonTrips()
  } catch (e) { ElMessage.error('保存失败') }
}
async function deleteTravelTripEntry(id) {
  try { await travelPersonTripAPI.delete(id); ElMessage.success('删除成功'); loadTravelPersonTrips() } catch (e) { ElMessage.error('删除失败') }
}

const travelTripsTotal = computed(() => travelPersonTrips.value.reduce((s, r) => s + (r.subtotal || 0), 0))

// ===== 原有 refs =====
async function loadLaborHours() {
  if (!quotationId.value) return
  try {
    const data = await api.get(`/quotations/${quotationId.value}/labor-hours`)
    laborHours.value = data || []
  } catch (e) { console.error(e) }
}

function showAddLabor() {
  laborForm.name = ''
  laborForm.hours = 0
  laborForm.person_days = 0
  laborForm.unit_price = 0
  laborDialogVisible.value = true
}

async function addLaborConfirm() {
  if (!laborForm.name) { ElMessage.warning('请填写名称'); return }
  if (laborForm.hours <= 0) { ElMessage.warning('工时必须大于0'); return }
  try {
    await api.post(`/quotations/${quotationId.value}/labor-hours`, {
      name: laborForm.name,
      hours: laborForm.hours,
      unit_price: laborForm.unit_price
    })
    ElMessage.success('添加成功')
    laborDialogVisible.value = false
    await loadLaborHours()
  } catch (e) { ElMessage.error('添加失败') }
}

function editLaborRow(row) {
  row._editing = true
  row._name = row.name
  row._hours = row.hours
  row._person_days = +(row.hours / HOURS_PER_DAY).toFixed(2)
  row._unit_price = row.unit_price
}

function cancelLaborEdit(row) {
  row._editing = false
}

async function saveLaborRow(row) {
  try {
    await api.put(`/quotations/${quotationId.value}/labor-hours/${row.id}`, {
      name: row._name,
      hours: row._hours,
      unit_price: row._unit_price
    })
    ElMessage.success('保存成功')
    await loadLaborHours()
  } catch (e) { ElMessage.error('保存失败') }
}

async function deleteLabor(id) {
  try {
    await api.delete(`/quotations/${quotationId.value}/labor-hours/${id}`)
    ElMessage.success('删除成功')
    await loadLaborHours()
  } catch (e) { ElMessage.error('删除失败') }
}

// 费用弹窗
const feeDialogVisible = ref(false)
const feeDialogTitle = ref('添加费用')
const feeForm = reactive({
  id: null,
  fee_type: '',
  location: 'factory',
  amount: 0,
  description: ''
})

const api = request

// 加载报价单
async function loadQuotation() {
  console.log('loadQuotation called, id:', quotationId.value)
  if (!quotationId.value) {
    console.log('Skipping loadQuotation - no valid id')
    pageLoading.value = false
    return
  }
  try {
    const data = await api.get(`/quotations/${quotationId.value}`)
    // 已归档的报价单不允许编辑，重定向回列表
    if (data.status === 'approved') {
      ElMessage.warning('已归档的报价单无法编辑，如需修改请先撤销归档')
      router.push('/quotations')
      return
    }
    quotation.value = data
    // 加载用户操作权限
    try {
      const permData = await api.get(`/quotations/${quotationId.value}/permissions`)
      permissions.value = permData
      // 如果当前 tab 不在允许列表中，切换到第一个可用 tab
      if (!permissions.value.tabs.includes(activeTab.value)) {
        activeTab.value = permissions.value.tabs[0] || 'summary'
      }
    } catch (e) {
      console.error('加载权限失败', e)
    }
    // 确保系数有默认值（优先用报价单私有系数，没有则从系统读取）
    if (!quotation.value.coefficients) {
      // 尝试加载系统默认系数
      try {
        const rates = await api.get('/fee_rates')
        const r = {}
        ;(rates || []).forEach(rate => { r[rate.category] = rate.rate })
        quotation.value.coefficients = {
          large: r.large ?? 1.0,
          standard: r.standard ?? 1.0,
          other: r.other ?? 1.0
        }
      } catch {
        quotation.value.coefficients = { large: 1.0, standard: 1.0, other: 1.0 }
      }
    }
    // 设置默认显示货币为报价单币种
    selectedCurrency.value = data.currency || 'CNY'
    // 加载参与人员
    try {
      const participantsData = await api.get(`/quotations/${quotationId.value}/participants`)
      quotationParticipants.value = participantsData || []
      currentParticipants.value = quotationParticipants.value
    } catch (error) {
      console.error('加载参与人员失败', error)
    }
    console.log('Quotation loaded:', data)
  } catch (error) {
    console.error('Load quotation error:', error)
    ElMessage.error('加载报价单失败: ' + (error.message || '未知错误'))
  } finally {
    pageLoading.value = false
  }
}

// 加载待审核变更申请数量
async function loadPendingReviewCount() {
  try {
    const data = await changeRequestsAPI.getPending()
    pendingReviewCount.value = Array.isArray(data) ? data.length : (data.total || 0)
  } catch (error) {
    console.error('加载待审核数量失败', error)
  }
}

// 跳转到待审核页面
function goToPendingReviews() {
  router.push('/change-requests')
}

// 加载用户列表（支持分页搜索）
async function loadUsers() {
  try {
    participantLoading.value = true
    const params = new URLSearchParams()
    params.append('page_size', '50')  // 一次加载较多用户
    if (participantSearch.value) {
      params.append('keyword', participantSearch.value)
    }
    const data = await api.get(`/users?${params.toString()}`)
    // 处理分页格式 {items: [...], total: n} 或直接是数组
    users.value = Array.isArray(data) ? data : (data.items || [])
  } catch (error) {
    console.error('加载用户失败', error)
  } finally {
    participantLoading.value = false
  }
}

// 加载业务角色用户
async function loadBusinessUsers() {
  try {
    const res = await api.get('/users?role=business')
    businessUsers.value = res.items || res || []
  } catch (error) {
    console.error('加载业务用户失败', error)
  }
}

// 加载费用类型
async function loadFeeTypes() {
  try {
    const res = await feesAPI.getFeeTypes()
    feeTypes.value = Array.isArray(res) ? res : (res.items || [])
  } catch (error) {
    console.error('加载费用类型失败', error)
  }
}

// 保存基本信息
async function saveBasic() {
  // 表单验证
  if (!quotation.value.name) {
    ElMessage.warning('请输入报价单名称')
    return
  }
  if (!quotation.value.scheme_no) {
    ElMessage.warning('请输入方案编号')
    return
  }
  if (!quotation.value.type) {
    ElMessage.warning('请选择项目类型')
    return
  }

  console.log('saveBasic called', { isEdit: isEdit.value, quotation: quotation.value })
  try {
    // 清理 null 值
    const data = { ...quotation.value }
    Object.keys(data).forEach(key => {
      if (data[key] === null || data[key] === undefined || data[key] === '') {
        delete data[key]
      }
    })
    console.log('Data to save:', data)

    let result
    if (isEdit.value) {
      result = await api.put(`/quotations/${quotationId.value}`, data)
      ElMessage.success('保存成功')
    } else {
      result = await api.post('/quotations', data)
      console.log('Create result:', result)
      ElMessage.success('创建成功')
      // 跳转到编辑页面
      router.push(`/quotations/${result.id}`)
    }
  } catch (error) {
    console.error('Save error:', error)
    ElMessage.error('保存失败: ' + (error.message || '未知错误'))
  }
}

// 加载模块
async function loadModules() {
  try {
    let data
    if (quotation.value.type === 'line') {
      // 线体报价单：聚合所有子报价单的模块
      data = await api.get(`/quotations/${quotationId.value}/all-modules`)
    } else {
      data = await api.get(`/quotations/${quotationId.value}/modules`)
    }
    modules.value = data
  } catch (error) {
    ElMessage.error('加载模块失败')
  }
}

// 显示添加模块弹窗
function showAddModule() {
  moduleDialogTitle.value = '添加模块'
  moduleForm.id = null
  moduleForm.name = ''
  moduleForm.name_en = ''
  moduleForm.description = ''
  moduleForm.module_type = 'other'
  moduleDialogVisible.value = true
}

// 编辑模块
function editModule(module) {
  moduleDialogTitle.value = '编辑模块'
  moduleForm.id = module.id
  moduleForm.name = module.name || ''
  moduleForm.name_en = module.name_en || ''
  moduleForm.description = module.description || ''
  moduleForm.module_type = module.module_type || 'other'
  // 先关闭再打开, 强制 el-input 重新渲染
  moduleDialogVisible.value = false
  nextTick(() => {
    moduleDialogVisible.value = true
  })
}

// 自动推断模块类型 (根据当前已选参与人员的参与类型 participant_type)
// 规则 (与后端 infer_module_type_from_participant_types 一致):
//   - 全部 agency → mechanical (机构)
//   - 全部 electrical → electrical (电气)
//   - 混合 / project / 空 → other (其他)
function inferModuleType() {
  if (currentParticipants.value.length === 0) {
    ElMessage.warning('请先在"参与人员"tab 中添加参与人员')
    return
  }
  const types = new Set(
    currentParticipants.value
      .map(p => p.participant_type)
      .filter(t => t)
  )
  if (types.size === 0) {
    moduleForm.module_type = 'other'
    ElMessage.info('参与人员未设置参与类型, 默认"其他"')
    return
  }
  if (types.size === 1) {
    const only = [...types][0]
    if (only === 'agency') {
      moduleForm.module_type = 'mechanical'
      ElMessage.success('已根据参与人员类型推断为: 机构')
      return
    }
    if (only === 'electrical') {
      moduleForm.module_type = 'electrical'
      ElMessage.success('已根据参与人员类型推断为: 电气')
      return
    }
  }
  // 混合 / 含 project → 其他
  moduleForm.module_type = 'other'
  ElMessage.info('参与人员类型混合或为"项目", 默认为: 其他')
}

// 保存模块
async function saveModule() {
  try {
    const payload = {
      name: moduleForm.name,
      name_en: moduleForm.name_en,
      description: moduleForm.description,
      module_type: moduleForm.module_type,
    }
    if (moduleForm.id) {
      await api.put(`/modules/${moduleForm.id}`, payload)
      ElMessage.success('更新成功')
    } else {
      await api.post(`/quotations/${quotationId.value}/modules`, payload)
      ElMessage.success('添加成功')
    }
    moduleDialogVisible.value = false
    loadModules()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// ============== 复制模块 ==============
// 打开弹窗
function showCopyModuleDialog() {
  copyForm.sourceQuotationId = null
  copyForm.quotationOptions = []
  copyForm.availableModules = []
  copyForm.selectedModuleIds = []
  copyModuleDialogVisible.value = true
  // 预加载: 默认列出前 20 个草稿
  searchQuotationsForCopy('')
}

// 远程搜索报价单
async function searchQuotationsForCopy(keyword) {
  if (!keyword || keyword.length < 1) {
    // 默认加载前 20 个草稿
    keyword = ''
  }
  copyForm.searching = true
  try {
    const r = await api.get('/quotations', {
      params: { keyword, page: 1, page_size: 20, status: 'draft' }
    })
    // 过滤掉当前报价单
    copyForm.quotationOptions = (r.items || []).filter(q => q.id !== quotationId.value)
  } catch (e) {
    ElMessage.error('搜索报价单失败')
  } finally {
    copyForm.searching = false
  }
}

// 源报价单改变 → 加载它的模块
async function onCopySourceChange(quotationId) {
  copyForm.availableModules = []
  copyForm.selectedModuleIds = []
  if (!quotationId) return
  copyForm.loadingModules = true
  try {
    const modules = await api.get(`/quotations/${quotationId}/modules`)
    // 过滤掉 0 物料的（避免空模块）
    copyForm.availableModules = modules
  } catch (e) {
    ElMessage.error('加载源报价单模块失败')
  } finally {
    copyForm.loadingModules = false
  }
}

// 选择变化
function handleCopyModuleSelection(selections) {
  copyForm.selectedModuleIds = selections.map(m => m.id)
}

// 全选
function selectAllCopyModules() {
  copyForm.selectedModuleIds = copyForm.availableModules.map(m => m.id)
}

// 全不选
function deselectAllCopyModules() {
  copyForm.selectedModuleIds = []
}

// 提交复制
async function submitCopyModules() {
  if (!copyForm.sourceQuotationId || !copyForm.selectedModuleIds.length) return
  copyForm.submitting = true
  try {
    const r = await api.post(`/quotations/${quotationId.value}/copy-modules`, {
      source_quotation_id: copyForm.sourceQuotationId,
      module_ids: copyForm.selectedModuleIds,
    })
    const totalModules = r.total_copied
    const totalMaterials = r.total_materials
    ElMessage.success(`成功复制 ${totalModules} 个模块（含 ${totalMaterials} 项物料）`)
    copyModuleDialogVisible.value = false
    // 刷新模块列表 + 物料列表 (filteredModuleGroups 用 moduleMaterials)
    await loadModules()
    await loadModuleMaterials()
  } catch (e) {
    const msg = e?.response?.data?.error || e?.response?.data?.detail || '复制失败'
    ElMessage.error(msg)
  } finally {
    copyForm.submitting = false
  }
}

// 删除模块
async function deleteModule(id) {
  try {
    await ElMessageBox.confirm('确定要删除该模块吗？', '提示', {
      type: 'warning'
    })
    await api.delete(`/modules/${id}`)
    ElMessage.success('删除成功')
    loadModules()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 加载物料列表（所有可选物料）
async function loadAvailableMaterials() {
  try {
    const data = await api.get('/materials')
    availableMaterials.value = data.items || data || []
  } catch (error) {
    ElMessage.error('加载物料列表失败')
  }
}

// 加载模块物料
async function loadModuleMaterials() {
  // 加载所有模块的物料
  try {
    const allMaterials = []
    for (const mod of modules.value) {
      const data = await api.get(`/modules/${mod.id}/materials`)
      const items = data.items || data || []
      if (items.length > 0) {
        allMaterials.push(...items.map(m => ({ ...m, module_id: mod.id })))
      }
    }
    moduleMaterials.value = allMaterials
  } catch (error) {
    ElMessage.error('加载模块物料失败')
  }
}

// 监听选中模块变化
watch(selectedModuleId, () => {
  loadModuleMaterials()
})

// 费用类型选择后自动带出位置
watch(() => feeForm.fee_type, (newFeeType) => {
  if (newFeeType) {
    const selected = feeTypes.value.find(ft => ft.name === newFeeType)
    if (selected) {
      feeForm.location = selected.location
    }
  }
})

// 显示添加物料弹窗（指定模块）
async function showAddMaterialToModule(moduleId) {
  selectedModuleId.value = moduleId
  await loadAvailableMaterials()
  addMaterialQuantity.value = 1
  selectedMaterials.value = []
  materialDialogVisible.value = true
}

// 显示添加物料弹窗（兼容旧调用）
async function showAddMaterial() {
  if (modules.value.length === 0) {
    ElMessage.warning('请先添加模块')
    return
  }
  selectedModuleId.value = modules.value[0].id
  await loadAvailableMaterials()
  addMaterialQuantity.value = 1
  selectedMaterials.value = []
  materialDialogVisible.value = true
}

// 修改其他物料单价
function editOtherMaterial(row) {
  otherPriceForm.id = row.id
  otherPriceForm.material_name = row.material_name
  otherPriceForm.unit_price_override = row.unit_price_override || row.unit_price || 0
  otherPriceDialogVisible.value = true
}

// 保存其他物料单价
async function saveOtherMaterialPrice() {
  if (!otherPriceForm.unit_price_override || otherPriceForm.unit_price_override <= 0) {
    ElMessage.warning('请输入有效的单价')
    return
  }
  try {
    await api.put(`/module_materials/${otherPriceForm.id}`, {
      unit_price_override: otherPriceForm.unit_price_override
    })
    ElMessage.success('修改成功')
    otherPriceDialogVisible.value = false
    await loadModuleMaterials()
  } catch (error) {
    ElMessage.error('修改失败')
  }
}

// 选择物料
function handleMaterialSelection(selection) {
  selectedMaterials.value = selection
}

// 添加物料到模块
async function addMaterialsToModule() {
  if (selectedMaterials.value.length === 0) {
    ElMessage.warning('请选择物料')
    return
  }
  
  // 已归档报价单需要提交变更申请
  if (isArchived.value) {
    try {
      for (const material of selectedMaterials.value) {
        const qty = material._quantity || 1
        await changeRequestsAPI.create({
          quotation_id: quotationId.value,
          module_id: selectedModuleId.value,
          change_type: 'material_add',
          proposed_data: { material_id: material.id, quantity: qty },
          original_data: {}
        })
      }
      ElMessage.warning('报价单已归档，添加物料已提交审核')
      materialDialogVisible.value = false
      selectedMaterials.value.forEach(m => m._quantity = 1)
      selectedMaterials.value = []
    } catch (error) {
      ElMessage.error('提交变更申请失败')
    }
    return
  }
  
  try {
    // 检查是否重复物料
    const existingMaterialIds = moduleMaterials.value
      .filter(mm => mm.module_id === selectedModuleId.value)
      .map(mm => mm.material_id || mm.id)
    const duplicate = selectedMaterials.value.find(m => existingMaterialIds.includes(m.id))
    if (duplicate) {
      ElMessage.warning(`"${duplicate.name}" 已在该模块中，请修改数量`)
      return
    }

    for (const material of selectedMaterials.value) {
      const qty = material._quantity || 1
      await api.post(`/modules/${selectedModuleId.value}/materials`, {
        material_id: material.id,
        quantity: qty
      })
    }
    ElMessage.success('添加成功')
    materialDialogVisible.value = false
    // 重置选中物料的 _quantity
    selectedMaterials.value.forEach(m => m._quantity = 1)
    loadModuleMaterials()
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

// 更新模块物料数量
async function updateMaterialQuantity(id, quantity) {
  // 已归档报价单需要提交变更申请
  if (isArchived.value) {
    const row = moduleMaterials.value.find(m => m.id === id)
    try {
      await changeRequestsAPI.create({
        quotation_id: quotationId.value,
        module_id: row.module_id,
        change_type: 'material_update',
        proposed_data: { id, quantity },
        original_data: { id, quantity: row.quantity }
      })
      ElMessage.warning('报价单已归档，数量变更已提交审核')
      loadModuleMaterials() // 刷新显示原始数据
    } catch (error) {
      ElMessage.error('提交变更申请失败')
    }
    return
  }
  
  try {
    await api.put(`/module_materials/${id}`, { quantity })
    ElMessage.success('数量已更新')
    loadModuleMaterials()
  } catch (error) {
    ElMessage.error('更新数量失败')
  }
}

// 删除模块物料
async function deleteModuleMaterial(id) {
  // 已归档报价单需要提交变更申请
  if (isArchived.value) {
    const row = moduleMaterials.value.find(m => m.id === id)
    try {
      await changeRequestsAPI.create({
        quotation_id: quotationId.value,
        module_id: row.module_id,
        change_type: 'material_delete',
        proposed_data: {},
        original_data: { id: row.id, quantity: row.quantity }
      })
      ElMessage.warning('报价单已归档，删除物料已提交审核')
      loadModuleMaterials()
    } catch (error) {
      ElMessage.error('提交变更申请失败')
    }
    return
  }
  
  try {
    await ElMessageBox.confirm('确定要删除该物料吗？', '提示', {
      type: 'warning'
    })
    await api.delete(`/module_materials/${id}`)
    ElMessage.success('删除成功')
    loadModuleMaterials()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 加载费用
async function loadFees() {
  try {
    const data = await api.get(`/quotations/${quotationId.value}/fees`)
    fees.value = data
  } catch (error) {
    ElMessage.error('加载费用失败')
  }
}

// 显示添加费用弹窗
function showAddFee() {
  feeDialogTitle.value = '添加费用'
  feeForm.id = null
  feeForm.fee_type = ''
  feeForm.location = 'factory'
  feeForm.amount = 0
  feeForm.description = ''
  feeDialogVisible.value = true
}

// 编辑费用
function editFee(fee) {
  feeDialogTitle.value = '编辑费用'
  feeForm.id = fee.id
  feeForm.fee_type = fee.fee_type
  feeForm.location = fee.location
  feeForm.amount = fee.amount
  feeForm.description = fee.description || ''
  feeDialogVisible.value = true
}

// 保存费用
async function saveFee() {
  try {
    if (feeForm.id) {
      await api.put(`/fees/${feeForm.id}`, feeForm)
      ElMessage.success('更新成功')
    } else {
      await api.post(`/quotations/${quotationId.value}/fees`, feeForm)
      ElMessage.success('添加成功')
    }
    feeDialogVisible.value = false
    loadFees()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 删除费用
async function deleteFee(id) {
  try {
    await ElMessageBox.confirm('确定要删除该费用吗？', '提示', {
      type: 'warning'
    })
    await api.delete(`/fees/${id}`)
    ElMessage.success('删除成功')
    loadFees()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 加载汇总
async function loadSummary() {
  if (!quotationId.value) return
  summaryLoading.value = true
  try {
    const data = await api.get(`/quotations/${quotationId.value}/summary`)
    summary.value = data
  } catch (error) {
    ElMessage.error('加载汇总失败')
  } finally {
    summaryLoading.value = false
  }
}

// 加载版本
async function loadVersions() {
  if (!quotationId.value) return
  try {
    const data = await api.get(`/quotations/${quotationId.value}/versions`)
    versions.value = data
  } catch (error) {
    ElMessage.error('加载版本失败')
  }
}

// 查看版本
function viewVersion(version) {
  ElMessage.info(`查看版本 V${version.version} - ${version.remark || '无备注'}`)
  // TODO: 可以打开版本详情弹窗
}

// 导出特定版本
function exportVersion(version, format) {
  openDownload(`/api/quotations/${quotationId.value}/versions/${version.version_no}/export/${format}`)
}

// 导出文件
function exportFile(format) {
  // 始终传递当前选中的币种参数
  openDownload(`/api/quotations/${quotationId.value}/export/${format}?currency=${selectedCurrency.value}`)
}

// 汇总 tab DOM 引用（用于导出 PDF 截图）
const summaryRef = ref(null)

// 运输+差旅合计（运输包装 + 差旅人天 + 差旅人次）
const totalTravelAmount = computed(() => {
  if (!summary.value) return 0
  const packing = summary.value.packing_total || 0
  const days = summary.value.travel_person_days_total || 0
  const trips = summary.value.travel_person_trips_total || 0
  return packing + days + trips
})

// 占比计算：含利润小计为分母
function getRatio(amount) {
  if (!summary.value || !amount) return '0.0'
  const denom = summary.value.subtotal_with_profit || 0
  if (denom === 0) return '0.0'
  return ((amount / denom) * 100).toFixed(1)
}

// 硬件分类占比：material_total_with_rates 为分母
function getMaterialCategoryRatio(amount) {
  if (!summary.value || !amount) return '0.0'
  const denom = summary.value.material_total_with_rates || 0
  if (denom === 0) return '0.0'
  return ((amount / denom) * 100).toFixed(1)
}

// 导出汇总 tab 内容为 PDF（按网页显示样式截图）
async function exportSummaryAsPDF() {
  if (!summaryRef.value) {
    ElMessage.error('汇总内容未加载，请先切换到汇总 tab')
    return
  }
  if (!summary.value) {
    ElMessage.warning('汇总数据为空，请先加载汇总')
    return
  }

  // 切换到汇总 tab 确保内容渲染
  if (activeTab.value !== 'summary') {
    activeTab.value = 'summary'
    await nextTick()
    await new Promise(resolve => setTimeout(resolve, 300))
  }

  const loading = ElMessage({
    message: '正在生成 PDF...',
    type: 'info',
    duration: 0
  })

  try {
    // 截图前临时隐藏不需要导出的元素（如货币切换器）
    const hideElements = summaryRef.value.querySelectorAll('.no-export')
    const prevDisplays = []
    hideElements.forEach((el) => {
      prevDisplays.push(el.style.display)
      el.style.display = 'none'
    })

    // 截图：使用完整 DOM 高度（包含滚动不可见部分）
    const canvas = await html2canvas(summaryRef.value, {
      scale: 2,
      useCORS: true,
      backgroundColor: '#ffffff',
      logging: false,
      windowWidth: summaryRef.value.scrollWidth,
      windowHeight: summaryRef.value.scrollHeight
    })

    // 恢复隐藏元素
    hideElements.forEach((el, i) => {
      el.style.display = prevDisplays[i]
    })

    // A4 尺寸（毫米），左右上下各留 5mm 边距
    const pdfWidth = 210
    const pdfHeight = 297
    const margin = 5
    const contentWidth = pdfWidth - margin * 2
    const contentHeight = pdfHeight - margin * 2

    // 高度按比例缩放到内容区宽度
    const imgWidth = contentWidth
    const imgHeight = (canvas.height * imgWidth) / canvas.width

    const pdf = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    })

    // 如果内容总高度 <= A4 内容区，单页
    if (imgHeight <= contentHeight) {
      const imgData = canvas.toDataURL('image/png')
      pdf.addImage(imgData, 'PNG', margin, margin, imgWidth, imgHeight)
    } else {
      // 多页：按 A4 内容区高度切片
      const pageHeightInPx = (contentHeight * canvas.width) / imgWidth
      let position = 0
      let pageIndex = 0

      while (position < canvas.height) {
        const pageCanvas = document.createElement('canvas')
        pageCanvas.width = canvas.width
        const remainingHeight = canvas.height - position
        const currentPageHeight = Math.min(pageHeightInPx, remainingHeight)
        pageCanvas.height = currentPageHeight

        const ctx = pageCanvas.getContext('2d')
        ctx.fillStyle = '#ffffff'
        ctx.fillRect(0, 0, pageCanvas.width, pageCanvas.height)
        ctx.drawImage(
          canvas,
          0, position, canvas.width, currentPageHeight,
          0, 0, canvas.width, currentPageHeight
        )

        const pageImgData = pageCanvas.toDataURL('image/png')
        const pageImgHeight = (pageCanvas.height * imgWidth) / pageCanvas.width
        if (pageIndex > 0) pdf.addPage()
        pdf.addImage(pageImgData, 'PNG', margin, margin, imgWidth, pageImgHeight)

        position += currentPageHeight
        pageIndex += 1
      }
    }

    const fileName = `${quotation.value?.name || '报价单'}_汇总_${new Date().toISOString().slice(0, 10)}.pdf`
    pdf.save(fileName)
    ElMessage.success(`PDF 已生成：${fileName}`)
  } catch (err) {
    console.error('导出汇总 PDF 失败：', err)
    ElMessage.error('导出失败：' + (err.message || '未知错误'))
  } finally {
    loading.close()
  }
}

// 返回列表
function goBack() {
  router.push('/quotations')
}

// 监听 tab 变化
watch(activeTab, (tab) => {
  if (tab === 'summary') {
    loadSummary()
  } else if (tab === 'versions') {
    loadVersions()
  }
})

// 监听路由参数变化
watch(() => route.params.id, (newId) => {
  quotationId.value = newId || null
  if (newId && newId !== 'new') {
    loadQuotation()
    loadModules()
    loadFees()
    loadPackingEntries()
    loadTravelPersonDays()
    loadTravelPersonTrips()
  }
}, { immediate: false })

onMounted(async () => {
  await loadUsers()
  await loadBusinessUsers()
  await loadFeeTypes()
  if (isEdit.value) {
    await loadQuotation()  // 先加载报价单，获取币种
    await loadExchangeRates(true)  // 跳过货币初始化，使用报价单币种
    await loadModules()
    await loadModuleMaterials()
    await loadFees()
    await loadLaborHours()
    await loadPackingEntries()
    await loadTravelPersonDays()
    await loadTravelPersonTrips()
  } else {
    await loadExchangeRates()  // 新建模式，使用默认币种
  }
})
</script>

<style scoped>
.quotation-edit {
  padding: var(--spacing-lg);
}

/* 页面标题栏 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.page-header-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.back-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.back-btn:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.page-title-sub {
  font-size: 14px;
  color: var(--color-text-muted);
  margin-left: var(--spacing-sm);
}

/* 卡片容器 */
.edit-card {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: calc(100vh - 140px);
}

.edit-card :deep(.el-tabs) {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.edit-card :deep(.el-tabs__content) {
  flex: 1;
  overflow: auto;
}

.edit-card :deep(.el-tab-pane) {
  height: 100%;
  overflow: auto;
}

/* Tabs 样式 */
.edit-card :deep(.el-tabs__header) {
  margin: 0;
  padding: 0 var(--spacing-lg);
  background: var(--color-bg-hover);
  border-bottom: 1px solid var(--color-border-light);
}

.edit-card :deep(.el-tabs__nav-wrap::after) {
  display: none;
}

.edit-card :deep(.el-tabs__item) {
  height: 48px;
  line-height: 48px;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
  padding: 0 var(--spacing-lg);
}

.edit-card :deep(.el-tabs__item.is-active) {
  color: var(--color-primary);
}

.edit-card :deep(.el-tabs__active-bar) {
  height: 3px;
  background: var(--color-primary);
}

.edit-card :deep(.el-tabs__content) {
  padding: var(--spacing-lg);
}

/* 表单样式 */
.form-section {
  max-width: 600px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
}

.form-actions {
  display: flex;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--color-border-light);
}

.save-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-xl);
  background: var(--color-primary);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.save-btn:hover {
  background: var(--color-primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

/* 表格容器 */
.table-section {
  margin-top: var(--spacing-md);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}

.table-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.table-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-md);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  border: none;
}

.action-btn.primary {
  background: var(--color-primary);
  color: white;
}

.action-btn.primary:hover {
  background: var(--color-primary-hover);
}

.action-btn.secondary {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

.action-btn.secondary:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

/* 数据表格 */
.data-table {
  border-radius: var(--radius-md);
  overflow: hidden;
}

.data-table :deep(.el-table__header-wrapper th) {
  background: var(--color-bg-hover) !important;
  color: var(--color-text-primary);
  font-weight: 600;
  font-size: 13px;
  padding: 12px 0;
}

.data-table :deep(.el-table__body-wrapper tr) {
  transition: background var(--transition-fast);
}

.data-table :deep(.el-table__body-wrapper tr:hover) {
  background: var(--color-bg-hover);
}

/* 单元格操作按钮 */
.cell-btn {
  padding: 4px 12px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  border: none;
  background: none;
}

.cell-btn.edit {
  color: var(--color-primary);
  background: var(--color-primary-light);
}

.cell-btn.edit:hover {
  background: var(--color-primary);
  color: white;
}

.cell-btn.delete {
  color: var(--color-danger);
  background: var(--color-danger-bg);
}

.cell-btn.delete:hover {
  background: var(--color-danger);
  color: white;
}

/* 弹窗样式 */
.dialog-header {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text-primary);
}

.dialog-form {
  padding: var(--spacing-md) 0;
}

.dialog-form :deep(.el-form-item__label) {
  font-weight: 500;
  color: var(--color-text-primary);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-sm);
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--color-border-light);
}

.cancel-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--radius-md);
  font-size: 14px;
  background: var(--color-bg-card);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.cancel-btn:hover {
  background: var(--color-bg-hover);
}

.confirm-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--radius-md);
  font-size: 14px;
  background: var(--color-primary);
  color: white;
  border: none;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.confirm-btn:hover {
  background: var(--color-primary-hover);
}

.summary-header {
  margin-bottom: var(--spacing-md);
}

.summary-currency {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.currency-label {
  font-weight: 500;
  color: var(--color-text-secondary);
}

.currency-note {
  font-size: 12px;
  color: var(--color-primary);
}

/* 汇总布局 */
.summary-layout {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.summary-left {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-md);
  align-items: stretch;
}

.summary-right {
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.summary-card {
  background: var(--color-bg-hover);
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  text-align: center;
}

.summary-card.compact {
  padding: var(--spacing-md);
  min-height: 90px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.summary-card.total {
  background: var(--color-primary);
  color: white;
}

.summary-card.total .summary-label {
  color: rgba(255,255,255,0.8);
}

.summary-label {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-xs);
}

.summary-card.total .summary-label {
  color: rgba(255,255,255,0.75);
}

.summary-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-text-primary);
}

.summary-value.highlight {
  color: var(--color-primary);
}

.summary-card.total .summary-value {
  color: white;
}

.summary-value.large {
  font-size: 32px;
  color: #FFFFFF;
}

/* 费用卡片 */
.fees-card {
  background: var(--color-bg-hover);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  text-align: left;
  flex: 1;
}

.fees-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-sm);
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid rgba(0,0,0,0.08);
}

.fees-total {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-primary);
}

.fees-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.fees-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  padding: 3px 0;
  color: var(--color-text-secondary);
}

.fees-row span:last-child {
  font-weight: 500;
  color: var(--color-text-primary);
}

@media (max-width: 900px) {
  .summary-layout {
    flex-direction: column;
  }
  .summary-left {
    grid-template-columns: repeat(3, 1fr);
  }
  .summary-right {
    width: 100%;
  }
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: var(--spacing-2xl);
  color: var(--color-text-muted);
}

.empty-icon {
  font-size: 48px;
  opacity: 0.5;
  margin-bottom: var(--spacing-md);
  display: block;
}

.module-actions,
.material-actions,
.fee-actions,
.export-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.material-filter-bar {
  display: flex;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.participant-manager {
  padding: 8px 0;
}

.participant-section {
  margin-bottom: 8px;
}

.participant-section h4 {
  margin: 0 0 12px 0;
  color: var(--color-text-primary);
  font-size: 14px;
}

.participant-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.user-list {
  max-height: 250px;
  overflow-y: auto;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.user-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  border-bottom: 1px solid var(--color-border);
}

.user-item:last-child {
  border-bottom: none;
}

.user-item:hover {
  background: var(--color-bg-hover);
}

.empty-text {
  color: var(--color-text-secondary);
  text-align: center;
  padding: 20px;
}

.material-summary {
  margin-top: 16px;
  padding: 12px 16px;
  background: var(--color-primary-light);
  border-radius: var(--radius-md);
  text-align: right;
  font-weight: 600;
  color: var(--color-primary);
}

.material-summary.total {
  background: var(--color-primary);
  color: white;
}

.module-group {
  margin-bottom: 24px;
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.module-group-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  background: var(--color-bg-hover);
  border-bottom: 1px solid var(--color-border-light);
}

.module-name {
  font-weight: 600;
  color: var(--color-text-primary);
}

.module-material-count {
  color: var(--color-text-secondary);
  font-size: 13px;
}

.module-total {
  margin-left: auto;
  font-weight: 600;
  color: var(--color-primary);
}

/* 响应式 */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .summary-grid {
    grid-template-columns: 1fr;
  }
}

/* 费用系数卡片 */
.coefficient-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 24px;
  max-width: 560px;
}

.coefficient-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.coefficient-title {
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.coefficient-actions {
  display: flex;
  gap: 8px;
}

.coefficient-desc {
  color: #6b7280;
  font-size: 13px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f3f4f6;
}

.coefficient-items {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.coefficient-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 14px;
  background: #f9fafb;
  border-radius: 8px;
}

.coefficient-item-label {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.coefficient-item-tip {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 2px;
}

.coefficient-item-icon {
  width: 38px;
  height: 38px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
  background: #d1d5db;
}

.coefficient-item-icon.large { background: linear-gradient(135deg, #f97316, #ea580c); }
.coefficient-item-icon.standard { background: linear-gradient(135deg, #0D9488, #0f766e); }
.coefficient-item-icon.other { background: linear-gradient(135deg, #6366f1, #4f46e5); }

.labor-header {
  display: flex;
  gap: 8px;
}

.labor-total {
  margin-top: 16px;
  padding: 12px 16px;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
  color: #166534;
  font-size: 14px;
}
.labor-total-days {
  margin-left: 8px;
  color: #15803d;
  font-weight: 500;
}
.form-hint {
  margin-left: 12px;
  color: #94a3b8;
  font-size: 12px;
}

/* 占比卡片组（5个：硬件/人力/差旅/利润/税） */
.ratio-cards {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.ratio-card {
  background: #ffffff;
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  text-align: center;
  border: 1px solid rgba(0,0,0,0.06);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-fast);
}

.ratio-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.ratio-card .ratio-label {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-bottom: 6px;
}

.ratio-card .ratio-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1.2;
}

.ratio-card .ratio-percent {
  font-size: 16px;
  font-weight: 700;
  color: var(--color-primary);
  margin-top: 4px;
}

.ratio-bar {
  margin-top: 8px;
  height: 6px;
  background: rgba(0,0,0,0.06);
  border-radius: 3px;
  overflow: hidden;
}

.ratio-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.4s ease;
}

.ratio-bar-fill.material { background: linear-gradient(90deg, #0D9488, #14B8A6); }
.ratio-bar-fill.labor { background: linear-gradient(90deg, #6366F1, #818CF8); }
.ratio-bar-fill.travel { background: linear-gradient(90deg, #F59E0B, #FBBF24); }
.ratio-bar-fill.profit { background: linear-gradient(90deg, #10B981, #34D399); }
.ratio-bar-fill.tax { background: linear-gradient(90deg, #EF4444, #F87171); }

/* 硬件成本结构 */
.hardware-structure {
  margin-top: var(--spacing-lg);
}

.hardware-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.hardware-card {
  background: #ffffff;
  border-radius: var(--radius-md);
  padding: var(--spacing-lg);
  text-align: center;
  border: 1px solid rgba(0,0,0,0.06);
  box-shadow: var(--shadow-sm);
  position: relative;
}

.hardware-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.hardware-card .hardware-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-bottom: 6px;
}

.hardware-card .dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}

.hardware-card.cat-large .dot { background: #0D9488; }
.hardware-card.cat-standard .dot { background: #6366F1; }
.hardware-card.cat-other .dot { background: #F59E0B; }

.hardware-amount {
  font-size: 20px;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1.2;
}

.hardware-percent {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-primary);
  margin-top: 4px;
}

.hardware-percent .ratio-of {
  font-size: 11px;
  color: var(--color-text-secondary);
  font-weight: 400;
  margin-left: 2px;
}

.hardware-bar {
  margin-top: 8px;
  height: 5px;
  background: rgba(0,0,0,0.06);
  border-radius: 3px;
  overflow: hidden;
}

.hardware-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.4s ease;
}

.hardware-card.cat-large .hardware-bar-fill { background: #0D9488; }
.hardware-card.cat-standard .hardware-bar-fill { background: #6366F1; }
.hardware-card.cat-other .hardware-bar-fill { background: #F59E0B; }

.hardware-meta {
  font-size: 11px;
  color: var(--color-text-secondary);
  margin-top: 6px;
  text-align: center;
}

/* 堆叠条 */
.hardware-stacked-bar {
  display: flex;
  height: 14px;
  border-radius: 7px;
  overflow: hidden;
  background: rgba(0,0,0,0.04);
}

.stacked-segment {
  height: 100%;
  transition: width 0.4s ease;
}

.stacked-segment.cat-large { background: #0D9488; }
.stacked-segment.cat-standard { background: #6366F1; }
.stacked-segment.cat-other { background: #F59E0B; }

/* 导出按钮组（补全为与 QuotationEdit.vue 一致的卡片风格） */
.export-grid {
  display: flex;
  gap: var(--spacing-md);
}

.export-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xl);
  background: #ffffff;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
  border: 1px solid rgba(0,0,0,0.06);
  box-shadow: var(--shadow-sm);
}

.export-item:hover {
  border-color: var(--color-primary);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.export-icon {
  font-size: 32px;
}

.export-label {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
}
</style>
