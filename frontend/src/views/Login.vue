<template>
  <div
    class="login-container"
    ref="containerRef"
    @mousemove="onMouseMove"
    @mouseleave="onMouseLeave"
    @click="onClick"
  >
    <!-- 鼠标跟随大光晕 -->
    <div class="mouse-glow" :style="glowStyle"></div>

    <!-- 背景装饰 blob -->
    <div class="bg-decoration">
      <div class="blob blob-1" :style="blobStyle1"></div>
      <div class="blob blob-2" :style="blobStyle2"></div>
      <div class="blob blob-3" :style="blobStyle3"></div>
    </div>

    <!-- 网格线 -->
    <div class="grid-overlay"></div>

    <!-- 登录卡片 -->
    <div class="login-wrapper" :style="cardStyle">
      <!-- 左侧品牌区 -->
      <div class="brand-section">
        <div class="brand-content">
          <div class="brand-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h1 class="brand-title">项目报价系统</h1>
          <p class="brand-subtitle">高效、专业、便捷的报价管理解决方案</p>
          <div class="brand-features">
            <div class="feature-item">
              <span class="feature-icon">📊</span>
              <span>智能报价汇总</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">📦</span>
              <span>原材料管理</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">📑</span>
              <span>多版本追踪</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧登录表单区 -->
      <div class="form-section">
        <div class="login-card">
          <div class="login-header">
            <h2>欢迎回来</h2>
            <p>请登录您的账户继续</p>
          </div>

          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            class="login-form"
            @keyup.enter="handleLogin"
          >
            <el-form-item prop="username">
              <label class="form-label">用户名</label>
              <el-input
                v-model="form.username"
                placeholder="请输入用户名"
                size="large"
                :prefix-icon="User"
              />
            </el-form-item>

            <el-form-item prop="password">
              <label class="form-label">密码</label>
              <el-input
                v-model="form.password"
                type="password"
                placeholder="请输入密码"
                size="large"
                show-password
                :prefix-icon="Lock"
                @keyup.enter="handleLogin"
              />
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                size="large"
                :loading="loading"
                class="login-btn"
                @click="handleLogin"
              >
                {{ loading ? '登录中...' : '登 录' }}
              </el-button>
            </el-form-item>
          </el-form>

          <div class="login-footer">
            <p>默认账号: <span>admin</span> / <span>admin123</span></p>
          </div>
        </div>
      </div>
    </div>

    <!-- 鼠标在卡片上时的表面高光（放在 wrapper 外面，防止被 overflow:hidden 裁剪） -->
    <div class="card-shine" :style="shineStyle" v-if="isOnCard"></div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()
const containerRef = ref(null)

const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

// ========== 鼠标追踪 ==========
const mouse = ref({ x: -1000, y: -1000 })
const isOnCard = ref(false)

function onMouseMove(e) {
  const rect = containerRef.value.getBoundingClientRect()
  mouse.value = {
    x: e.clientX - rect.left,
    y: e.clientY - rect.top
  }
  // 检测鼠标是否在卡片上
  const cardEl = containerRef.value.querySelector('.login-wrapper')
  if (cardEl) {
    const cardRect = cardEl.getBoundingClientRect()
    isOnCard.value = (
      e.clientX >= cardRect.left &&
      e.clientX <= cardRect.right &&
      e.clientY >= cardRect.top &&
      e.clientY <= cardRect.bottom
    )
  }
}

function onMouseLeave() {
  mouse.value = { x: -1000, y: -1000 }
  isOnCard.value = false
}

function onClick(e) {
  const rect = containerRef.value.getBoundingClientRect()
  const ripple = document.createElement('div')
  ripple.className = 'ripple'
  ripple.style.left = (e.clientX - rect.left) + 'px'
  ripple.style.top = (e.clientY - rect.top) + 'px'
  containerRef.value.appendChild(ripple)
  setTimeout(() => ripple.remove(), 600)
}

// ========== 鼠标光晕跟随 ==========
const glowStyle = computed(() => ({
  left: mouse.value.x + 'px',
  top: mouse.value.y + 'px'
}))

// ========== Blob 视差 ==========
const blobOffset = computed(() => {
  const cx = (mouse.value.x / (containerRef.value?.offsetWidth || 1)) - 0.5
  const cy = (mouse.value.y / (containerRef.value?.offsetHeight || 1)) - 0.5
  return { x: cx, y: cy }
})

const blobStyle1 = computed(() => ({
  transform: `translate(${blobOffset.value.x * 80}px, ${blobOffset.value.y * 50}px)`,
  transition: 'transform 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94)'
}))
const blobStyle2 = computed(() => ({
  transform: `translate(${blobOffset.value.x * -60}px, ${blobOffset.value.y * 70}px)`,
  transition: 'transform 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94)'
}))
const blobStyle3 = computed(() => ({
  transform: `translate(${blobOffset.value.x * 40}px, ${blobOffset.value.y * -45}px)`,
  transition: 'transform 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94)'
}))

// ========== 卡片磁吸位移 + 阴影跟随 ==========
const cardStyle = computed(() => {
  const cx = blobOffset.value.x
  const cy = blobOffset.value.y
  const maxShift = 12
  return {
    transform: `translate(${cx * maxShift}px, ${cy * maxShift}px)`,
    boxShadow: `
      ${cx * 15}px ${cy * 15}px 50px rgba(0, 0, 0, 0.3),
      ${cx * 5}px ${cy * 5}px 20px rgba(0, 0, 0, 0.15)
    `,
    transition: 'transform 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94), box-shadow 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94)',
    willChange: 'transform, box-shadow'
  }
})

// ========== 卡片表面高光 ==========
const shineStyle = computed(() => ({
  left: mouse.value.x + 'px',
  top: mouse.value.y + 'px'
}))

const handleLogin = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        await authStore.login(form.username, form.password)
        ElMessage.success('登录成功')
        localStorage.setItem('just_logged_in', 'true')
        router.push('/dashboard')
      } catch (error) {
        ElMessage.error(error.message || '登录失败')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(160deg, #0D9488 0%, #14857F 25%, #0F766E 55%, #134E4A 100%);
  position: relative;
  overflow: hidden;
  cursor: crosshair;
}

/* ========== 鼠标跟随光晕 ========== */
.mouse-glow {
  position: absolute;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(16, 185, 129, 0.12) 0%,
    rgba(16, 185, 129, 0.04) 40%,
    transparent 70%
  );
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 1;
  transition: left 0.2s ease-out, top 0.2s ease-out;
}

/* ========== 背景 blob ========== */
.bg-decoration {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
}

.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
}

.blob-1 {
  width: 700px;
  height: 700px;
  background: radial-gradient(circle, rgba(16, 185, 129, 0.4) 0%, rgba(13, 148, 136, 0.15) 40%, transparent 70%);
  top: -250px;
  right: -150px;
  animation: pulse 8s ease-in-out infinite;
}

.blob-2 {
  width: 550px;
  height: 550px;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, rgba(79, 70, 229, 0.08) 40%, transparent 70%);
  bottom: -180px;
  left: -100px;
  animation: pulse 10s ease-in-out infinite reverse;
}

.blob-3 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(6, 182, 212, 0.22) 0%, rgba(8, 145, 178, 0.06) 40%, transparent 70%);
  top: 50%;
  left: 30%;
  transform: translate(-50%, -50%);
  animation: pulse 12s ease-in-out infinite;
  animation-delay: -4s;
}

@keyframes pulse {
  0%, 100% { opacity: 0.8; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.08); }
}

/* ========== 网格线 ========== */
.grid-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
  z-index: 0;
}

/* ========== 登录卡片 ========== */
.login-wrapper {
  display: flex;
  width: 900px;
  min-height: 560px;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.25);
  box-shadow:
    0 25px 60px rgba(0, 0, 0, 0.25),
    0 8px 20px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  position: relative;
  z-index: 2;
  overflow: hidden;
}

/* ========== 卡片表面高光 ========== */
.card-shine {
  position: absolute;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.25) 0%,
    rgba(255, 255, 255, 0.08) 40%,
    transparent 70%
  );
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 10;
  transition: left 0.1s ease-out, top 0.1s ease-out;
  filter: blur(6px);
}

/* ========== 点击涟漪 ========== */
:deep(.ripple) {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  width: 10px;
  height: 10px;
  transform: translate(-50%, -50%) scale(1);
  animation: ripple-anim 0.6s ease-out forwards;
  pointer-events: none;
  z-index: 10;
}

@keyframes ripple-anim {
  0% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
  100% { transform: translate(-50%, -50%) scale(40); opacity: 0; }
}

/* ========== 左侧品牌区 ========== */
.brand-section {
  flex: 1;
  background: transparent;
  border-right: 1px solid rgba(255, 255, 255, 0.15);
  padding: var(--spacing-2xl);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.brand-section::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%230D9488' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  opacity: 0.8;
}

.brand-content {
  position: relative;
  z-index: 1;
  text-align: center;
}

.brand-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto var(--spacing-lg);
  background: rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-xl);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-icon svg {
  width: 40px;
  height: 40px;
  color: rgba(255, 255, 255, 0.95);
}

.brand-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: var(--spacing-sm);
  letter-spacing: -0.5px;
  color: rgba(255, 255, 255, 0.95);
}

.brand-subtitle {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: var(--spacing-xl);
}

.brand-features {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.feature-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 14px;
  color: rgba(255, 255, 255, 0.65);
}

.feature-icon {
  font-size: 18px;
}

/* ========== 右侧表单区 ========== */
.form-section {
  flex: 1;
  background: rgba(255, 255, 255, 0.97);
  border-left: 1px solid rgba(255, 255, 255, 0.15);
  padding: var(--spacing-2xl);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
}

.login-card {
  width: 100%;
  max-width: 320px;
}

.login-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.login-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-xs);
}

.login-header p {
  font-size: 14px;
  color: var(--color-text-secondary);
}

.login-form {
  margin-top: var(--spacing-md);
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.login-form :deep(.el-input__wrapper) {
  padding: 4px 16px;
  border-radius: var(--radius-md);
  box-shadow: 0 0 0 1px var(--color-border);
  transition: box-shadow 0.3s ease;
}

.login-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 2px rgba(13, 148, 136, 0.3);
}

.login-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px rgba(13, 148, 136, 0.5) !important;
}

.login-form :deep(.el-input__inner) {
  font-size: 15px;
}

.login-btn {
  width: 100%;
  height: 44px;
  font-size: 16px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, #0D9488 0%, #14857F 100%);
  border: none;
  color: white;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
}

.login-btn:hover {
  background: linear-gradient(135deg, #14857F 0%, #0F766E 100%);
  box-shadow: 0 6px 20px rgba(13, 148, 136, 0.4);
  transform: translateY(-1px);
}

.login-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px rgba(13, 148, 136, 0.3);
}

.login-footer {
  margin-top: var(--spacing-lg);
  text-align: center;
}

.login-footer p {
  font-size: 12px;
  color: var(--color-text-secondary);
}

.login-footer span {
  color: var(--color-primary);
  font-weight: 500;
}
</style>
