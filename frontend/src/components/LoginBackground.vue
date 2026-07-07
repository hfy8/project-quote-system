<template>
  <div
    ref="containerRef"
    class="login-bg-abs"
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

    <!-- 鼠标在卡片上时的表面高光 -->
    <div class="card-shine" :style="shineStyle" v-if="isOnCard"></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const containerRef = ref(null)

const mouse = ref({ x: -1000, y: -1000 })
const isOnCard = ref(false)

function onMouseMove(e) {
  const rect = containerRef.value.getBoundingClientRect()
  mouse.value = {
    x: e.clientX - rect.left,
    y: e.clientY - rect.top
  }
  // 检测鼠标是否在卡片上
  const cardEl = document.querySelector('.login-wrapper')
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

// 鼠标光晕跟随
const glowStyle = computed(() => ({
  left: mouse.value.x + 'px',
  top: mouse.value.y + 'px'
}))

// Blob 视差
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

// 卡片表面高光
const shineStyle = computed(() => ({
  left: mouse.value.x + 'px',
  top: mouse.value.y + 'px'
}))
</script>

<style scoped>
.login-bg-abs {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: auto;
  cursor: crosshair;
}

.mouse-glow {
  position: absolute;
  width: 600px;
  height: 600px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(16, 185, 129, 0.12) 0%, rgba(16, 185, 129, 0.04) 40%, transparent 70%);
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 1;
  transition: left 0.2s ease-out, top 0.2s ease-out;
}

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

.grid-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
  z-index: 1;
}

.card-shine {
  position: absolute;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.08) 40%, transparent 70%);
  transform: translate(-50%, -50%);
  pointer-events: none;
  z-index: 10;
  transition: left 0.1s ease-out, top 0.1s ease-out;
  filter: blur(6px);
}

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
</style>
