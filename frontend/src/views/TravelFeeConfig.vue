<template>
  <div class="travel-fee-config-container">
    <div class="page-header">
      <h2>运输与差旅费用配置</h2>
      <p class="subtitle">配置运输包装类型、差旅分类、出行方式及各项单价</p>
    </div>

    <div class="card">
      <el-tabs v-model="activeTab" class="config-tabs">
        <!-- 1. 包装类型 -->
        <el-tab-pane label="运输包装类型" name="packing">
          <div class="tab-toolbar">
            <el-button type="primary" size="small" @click="showAddPacking">添加运输包装类型</el-button>
          </div>
          <el-table :data="packingTypes" border v-loading="loading" height="calc(-280px + 100vh)">
            <el-table-column prop="name" label="名称" width="150" />
            <el-table-column prop="unit_price" label="单价（元/个）" width="160">
              <template #default="{ row }">
                <span class="money">¥{{ row.unit_price.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="description" label="描述" />
            <el-table-column label="操作" width="140" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="editPacking(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteItem('packing', row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 2. 差旅分类 -->
        <el-tab-pane label="差旅分类" name="category">
          <div class="tab-toolbar">
            <el-button type="primary" size="small" @click="showAddCategory">添加分类</el-button>
          </div>
          <el-table :data="travelCategories" border v-loading="loading" height="calc(-280px + 100vh)">
            <el-table-column prop="sort_order" label="排序" width="80" />
            <el-table-column prop="name" label="分类名称" width="180" />
            <el-table-column prop="code" label="代码" width="140" />
            <el-table-column prop="description" label="描述" />
            <el-table-column label="操作" width="140" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="editCategory(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteItem('category', row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 3. 差旅人天单价 -->
        <el-tab-pane label="差旅人天单价" name="dayrate">
          <div class="tab-toolbar">
            <el-button type="primary" size="small" @click="showAddDayRate">添加人天单价</el-button>
          </div>
          <el-table :data="travelDayRates" border v-loading="loading" height="calc(-280px + 100vh)">
            <el-table-column prop="travel_category_name" label="差旅分类" width="160" />
            <el-table-column prop="unit_price" label="单价（元/人天）" width="180">
              <template #default="{ row }">
                <span class="money">¥{{ row.unit_price.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="currency" label="币种" width="80" />
            <el-table-column prop="description" label="描述" />
            <el-table-column label="操作" width="140" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="editDayRate(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteItem('dayrate', row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 4. 出行方式 -->
        <el-tab-pane label="出行方式" name="mode">
          <div class="tab-toolbar">
            <el-button type="primary" size="small" @click="showAddMode">添加出行方式</el-button>
          </div>
          <el-table :data="travelModes" border v-loading="loading" height="calc(-280px + 100vh)">
            <el-table-column prop="name" label="名称" width="120" />
            <el-table-column prop="code" label="代码" width="120" />
            <el-table-column prop="description" label="描述" />
            <el-table-column label="操作" width="140" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="editMode(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteItem('mode', row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <!-- 5. 差旅人次单价矩阵 -->
        <el-tab-pane label="差旅人次单价" name="triptfee">
          <div class="tab-toolbar">
            <el-button type="primary" size="small" @click="showAddTripFee">添加人次单价</el-button>
          </div>
          <el-table :data="personTripFees" border v-loading="loading" height="calc(-280px + 100vh)">
            <el-table-column prop="travel_category_name" label="差旅分类" width="140" />
            <el-table-column prop="travel_mode_name" label="出行方式" width="120" />
            <el-table-column prop="unit_price" label="交通单价（元/人次）" width="180">
              <template #default="{ row }">
                <span class="money">¥{{ row.unit_price.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="visa_fee" label="签证费（元/人次）" width="180">
              <template #default="{ row }">
                <span class="money">¥{{ row.visa_fee.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="currency" label="币种" width="80" />
            <el-table-column prop="description" label="描述" />
            <el-table-column label="操作" width="140" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="editTripFee(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteItem('tripfee', row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- ====== 弹窗 ====== -->

    <!-- 包装类型 -->
    <el-dialog v-model="packingDialog.visible" :title="packingDialog.title" width="480px">
      <el-form :model="packingDialog.form" label-width="110px">
        <el-form-item label="名称" required>
          <el-input v-model="packingDialog.form.name" placeholder="如：纸箱" />
        </el-form-item>
        <el-form-item label="英文名">
          <el-input v-model="packingDialog.form.name_en" placeholder="如：Carton" />
        </el-form-item>
        <el-form-item label="单价（元/个）" required>
          <el-input-number v-model="packingDialog.form.unit_price" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="packingDialog.form.description" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="packingDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="savePacking">确定</el-button>
      </template>
    </el-dialog>

    <!-- 差旅分类 -->
    <el-dialog v-model="categoryDialog.visible" :title="categoryDialog.title" width="480px">
      <el-form :model="categoryDialog.form" label-width="110px">
        <el-form-item label="分类名称" required>
          <el-input v-model="categoryDialog.form.name" placeholder="如：国内出差" />
        </el-form-item>
        <el-form-item label="代码" required>
          <el-input v-model="categoryDialog.form.code" placeholder="如：domestic" :disabled="categoryDialog.isEdit" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="categoryDialog.form.sort_order" :min="0" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="categoryDialog.form.description" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="categoryDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="saveCategory">确定</el-button>
      </template>
    </el-dialog>

    <!-- 差旅人天单价 -->
    <el-dialog v-model="dayRateDialog.visible" :title="dayRateDialog.title" width="480px">
      <el-form :model="dayRateDialog.form" label-width="120px">
        <el-form-item label="差旅分类" required>
          <el-select v-model="dayRateDialog.form.travel_category_id" placeholder="请选择" :disabled="dayRateDialog.isEdit">
            <el-option v-for="c in travelCategories" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="单价（元/人天）" required>
          <el-input-number v-model="dayRateDialog.form.unit_price" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="币种">
          <el-input v-model="dayRateDialog.form.currency" style="width:120px" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="dayRateDialog.form.description" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dayRateDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="saveDayRate">确定</el-button>
      </template>
    </el-dialog>

    <!-- 出行方式 -->
    <el-dialog v-model="modeDialog.visible" :title="modeDialog.title" width="480px">
      <el-form :model="modeDialog.form" label-width="110px">
        <el-form-item label="名称" required>
          <el-input v-model="modeDialog.form.name" placeholder="如：飞机" />
        </el-form-item>
        <el-form-item label="英文名">
          <el-input v-model="modeDialog.form.name_en" placeholder="如：Plane" />
        </el-form-item>
        <el-form-item label="代码" required>
          <el-input v-model="modeDialog.form.code" placeholder="如：plane" :disabled="modeDialog.isEdit" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="modeDialog.form.description" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="modeDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="saveMode">确定</el-button>
      </template>
    </el-dialog>

    <!-- 差旅人次单价 -->
    <el-dialog v-model="tripFeeDialog.visible" :title="tripFeeDialog.title" width="520px">
      <el-form :model="tripFeeDialog.form" label-width="120px">
        <el-form-item label="差旅分类" required>
          <el-select v-model="tripFeeDialog.form.travel_category_id" placeholder="请选择" :disabled="tripFeeDialog.isEdit">
            <el-option v-for="c in travelCategories" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="出行方式" required>
          <el-select v-model="tripFeeDialog.form.travel_mode_id" placeholder="请选择" :disabled="tripFeeDialog.isEdit">
            <el-option v-for="m in travelModes" :key="m.id" :label="m.name" :value="m.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="交通单价（元/人次）" required>
          <el-input-number v-model="tripFeeDialog.form.unit_price" :min="0" :precision="2" />
        </el-form-item>
        <el-form-item label="签证费（元/人次）">
          <el-input-number v-model="tripFeeDialog.form.visa_fee" :min="0" :precision="2" />
          <span class="form-hint">仅非国内出差需填写</span>
        </el-form-item>
        <el-form-item label="币种">
          <el-input v-model="tripFeeDialog.form.currency" style="width:120px" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="tripFeeDialog.form.description" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="tripFeeDialog.visible = false">取消</el-button>
        <el-button type="primary" @click="saveTripFee">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  packingTypeAPI,
  travelCategoryAPI,
  travelDayRateAPI,
  travelModeAPI,
  travelPersonTripFeeAPI,
} from '@/api'

const activeTab = ref('packing')
const loading = ref(false)

// 数据
const packingTypes = ref([])
const travelCategories = ref([])
const travelDayRates = ref([])
const travelModes = ref([])
const personTripFees = ref([])

// ====== 加载 ======
async function loadAll() {
  loading.value = true
  try {
    const [pt, tc, tdr, tm, tpf] = await Promise.all([
      packingTypeAPI.getList(),
      travelCategoryAPI.getList(),
      travelDayRateAPI.getList(),
      travelModeAPI.getList(),
      travelPersonTripFeeAPI.getList(),
    ])
    packingTypes.value = Array.isArray(pt) ? pt : (pt.items || [])
    travelCategories.value = Array.isArray(tc) ? tc : (tc.items || [])
    travelDayRates.value = Array.isArray(tdr) ? tdr : (tdr.items || [])
    travelModes.value = Array.isArray(tm) ? tm : (tm.items || [])
    personTripFees.value = Array.isArray(tpf) ? tpf : (tpf.items || [])
  } catch (e) {
    ElMessage.error('加载配置失败')
  } finally {
    loading.value = false
  }
}

// ====== 删除通用 ======
async function deleteItem(type, id) {
  try {
    await ElMessageBox.confirm('确定要删除吗？', '提示', { type: 'warning' })
    const apis = {
      packing: packingTypeAPI,
      category: travelCategoryAPI,
      dayrate: travelDayRateAPI,
      mode: travelModeAPI,
      tripfee: travelPersonTripFeeAPI,
    }
    await apis[type].delete(id)
    ElMessage.success('删除成功')
    loadAll()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

// ====== 运输包装类型 ======
const packingDialog = reactive({
  visible: false, title: '添加包装类型', isEdit: false,
  form: { id: null, name: '', name_en: '', unit_price: 0, description: '' },
})

function showAddPacking() {
  packingDialog.isEdit = false
  packingDialog.title = '添加运输包装类型'
  packingDialog.form = { id: null, name: '', name_en: '', unit_price: 0, description: '' }
  packingDialog.visible = true
}
function editPacking(row) {
  packingDialog.isEdit = true
  packingDialog.title = '编辑运输包装类型'
  packingDialog.form = { ...row }
  packingDialog.visible = true
}
async function savePacking() {
  const f = packingDialog.form
  if (!f.name) { ElMessage.warning('请输入名称'); return }
  try {
    if (packingDialog.isEdit) {
      await packingTypeAPI.update(f.id, { name: f.name, name_en: f.name_en, unit_price: f.unit_price, description: f.description })
    } else {
      await packingTypeAPI.create({ name: f.name, name_en: f.name_en, unit_price: f.unit_price, description: f.description })
    }
    ElMessage.success('保存成功')
    packingDialog.visible = false
    loadAll()
  } catch (e) { ElMessage.error('保存失败') }
}

// ====== 差旅分类 ======
const categoryDialog = reactive({
  visible: false, title: '添加差旅分类', isEdit: false,
  form: { id: null, name: '', code: '', sort_order: 0, description: '' },
})

function showAddCategory() {
  categoryDialog.isEdit = false
  categoryDialog.title = '添加差旅分类'
  categoryDialog.form = { id: null, name: '', code: '', sort_order: 0, description: '' }
  categoryDialog.visible = true
}
function editCategory(row) {
  categoryDialog.isEdit = true
  categoryDialog.title = '编辑差旅分类'
  categoryDialog.form = { ...row }
  categoryDialog.visible = true
}
async function saveCategory() {
  const f = categoryDialog.form
  if (!f.name || !f.code) { ElMessage.warning('请填写名称和代码'); return }
  try {
    if (categoryDialog.isEdit) {
      await travelCategoryAPI.update(f.id, { name: f.name, code: f.code, sort_order: f.sort_order, description: f.description })
    } else {
      await travelCategoryAPI.create({ name: f.name, code: f.code, sort_order: f.sort_order, description: f.description })
    }
    ElMessage.success('保存成功')
    categoryDialog.visible = false
    loadAll()
  } catch (e) { ElMessage.error('保存失败') }
}

// ====== 差旅人天单价 ======
const dayRateDialog = reactive({
  visible: false, title: '添加人天单价', isEdit: false,
  form: { id: null, travel_category_id: null, unit_price: 0, currency: 'CNY', description: '' },
})

function showAddDayRate() {
  dayRateDialog.isEdit = false
  dayRateDialog.title = '添加人天单价'
  dayRateDialog.form = { id: null, travel_category_id: null, unit_price: 0, currency: 'CNY', description: '' }
  dayRateDialog.visible = true
}
function editDayRate(row) {
  dayRateDialog.isEdit = true
  dayRateDialog.title = '编辑人天单价'
  dayRateDialog.form = { ...row }
  dayRateDialog.visible = true
}
async function saveDayRate() {
  const f = dayRateDialog.form
  if (!f.travel_category_id) { ElMessage.warning('请选择差旅分类'); return }
  try {
    if (dayRateDialog.isEdit) {
      await travelDayRateAPI.update(f.id, { travel_category_id: f.travel_category_id, unit_price: f.unit_price, currency: f.currency, description: f.description })
    } else {
      await travelDayRateAPI.create({ travel_category_id: f.travel_category_id, unit_price: f.unit_price, currency: f.currency, description: f.description })
    }
    ElMessage.success('保存成功')
    dayRateDialog.visible = false
    loadAll()
  } catch (e) { ElMessage.error('保存失败') }
}

// ====== 出行方式 ======
const modeDialog = reactive({
  visible: false, title: '添加出行方式', isEdit: false,
  form: { id: null, name: '', name_en: '', code: '', description: '' },
})

function showAddMode() {
  modeDialog.isEdit = false
  modeDialog.title = '添加出行方式'
  modeDialog.form = { id: null, name: '', name_en: '', code: '', description: '' }
  modeDialog.visible = true
}
function editMode(row) {
  modeDialog.isEdit = true
  modeDialog.title = '编辑出行方式'
  modeDialog.form = { ...row }
  modeDialog.visible = true
}
async function saveMode() {
  const f = modeDialog.form
  if (!f.name || !f.code) { ElMessage.warning('请填写名称和代码'); return }
  try {
    if (modeDialog.isEdit) {
      await travelModeAPI.update(f.id, { name: f.name, name_en: f.name_en, code: f.code, description: f.description })
    } else {
      await travelModeAPI.create({ name: f.name, name_en: f.name_en, code: f.code, description: f.description })
    }
    ElMessage.success('保存成功')
    modeDialog.visible = false
    loadAll()
  } catch (e) { ElMessage.error('保存失败') }
}

// ====== 差旅人次单价 ======
const tripFeeDialog = reactive({
  visible: false, title: '添加人次单价', isEdit: false,
  form: { id: null, travel_category_id: null, travel_mode_id: null, unit_price: 0, visa_fee: 0, currency: 'CNY', description: '' },
})

function showAddTripFee() {
  tripFeeDialog.isEdit = false
  tripFeeDialog.title = '添加人次单价'
  tripFeeDialog.form = { id: null, travel_category_id: null, travel_mode_id: null, unit_price: 0, visa_fee: 0, currency: 'CNY', description: '' }
  tripFeeDialog.visible = true
}
function editTripFee(row) {
  tripFeeDialog.isEdit = true
  tripFeeDialog.title = '编辑人次单价'
  tripFeeDialog.form = { ...row }
  tripFeeDialog.visible = true
}
async function saveTripFee() {
  const f = tripFeeDialog.form
  if (!f.travel_category_id || !f.travel_mode_id) { ElMessage.warning('请选择差旅分类和出行方式'); return }
  try {
    if (tripFeeDialog.isEdit) {
      await travelPersonTripFeeAPI.update(f.id, { unit_price: f.unit_price, visa_fee: f.visa_fee, currency: f.currency, description: f.description })
    } else {
      await travelPersonTripFeeAPI.create({ travel_category_id: f.travel_category_id, travel_mode_id: f.travel_mode_id, unit_price: f.unit_price, visa_fee: f.visa_fee, currency: f.currency, description: f.description })
    }
    ElMessage.success('保存成功')
    tripFeeDialog.visible = false
    loadAll()
  } catch (e) { ElMessage.error('保存失败') }
}

onMounted(loadAll)
</script>

<style scoped>
.travel-fee-config-container {
  padding: var(--spacing-lg);
  height: 100vh;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.page-header { margin-bottom: var(--spacing-lg); }
.page-header h2 { margin: 0 0 8px 0; color: var(--color-text-primary); }
.subtitle { color: var(--color-text-secondary); margin: 0; }

.card {
  background: var(--color-bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  border: 1px solid var(--color-border);
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}

.tab-toolbar { margin-bottom: var(--spacing-md); }
.money { font-weight: 600; color: var(--color-primary); }
.form-hint { margin-left: 12px; color: var(--color-text-muted); font-size: 13px; }
</style>
