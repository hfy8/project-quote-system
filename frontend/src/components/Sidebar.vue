<template>
  <nav class="sidebar-nav">
    <div v-for="section in NAV_SECTIONS" :key="section.title" class="nav-section" v-if="section.items.some(item => canView(item.perm))">
      <div class="nav-section-title">{{ section.title }}</div>
      <router-link
        v-for="item in section.items" :key="item.path"
        :to="item.path" class="nav-item" :class="{ active: isActive(item.path) }"
        v-if="canView(item.perm)"
      >
        <span class="nav-icon">{{ item.icon }}</span>
        <span class="nav-text">{{ item.text }}</span>
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { hasPermission } from '../router'

const NAV_SECTIONS = [
  {
    title: '主菜单',
    items: [
      { path: '/dashboard', icon: '🏠', text: '首页', perm: null },  // null = 总是可见
      { path: '/quotations', icon: '📋', text: '报价单管理', perm: 'quotation.view' },
      { path: '/materials', icon: '📦', text: '原材料库', perm: 'material.view' },
      { path: '/fee-types', icon: '💰', text: '费用类型', perm: 'fee_type.view' },
      { path: '/my-assignments', icon: '📌', text: '我的分配', perm: 'module_assignment.view' },
    ],
  },
  {
    title: '系统管理',
    items: [
      { path: '/users', icon: '👤', text: '用户管理', perm: 'user.view' },
      { path: '/roles', icon: '👥', text: '角色管理', perm: 'role.view' },
      { path: '/fee-rates', icon: '📊', text: '费用系数', perm: 'fee_rate.view' },
      { path: '/exchange-rates', icon: '💱', text: '汇率配置', perm: 'exchange_rate.view' },
      { path: '/logs', icon: '📝', text: '操作日志', perm: 'log.view' },
      { path: '/travel-fee-config', icon: '🚚', text: '运输差旅配置', perm: 'travel_fee_config.view' },
    ],
  },
  {
    title: '智能助手',
    items: [
      { path: '/ai-chat', icon: '🤖', text: 'AI 助手', perm: 'ai.query' },
    ],
  },
  {
    title: '设置',
    items: [
      { path: '/system', icon: '⚙️', text: '系统设置', perm: 'system.view' },
      { path: '/participant-type-permissions', icon: '🔐', text: '参与人权限', perm: 'participant_type_permission.view' },
    ],
  },
]

const canView = (perm) => {
  if (!perm) return true  // null perm = 总是可见
  return hasPermission(userPermissions.value, perm)
}
const authStore = useAuthStore()

const userPermissions = computed(() => authStore.userInfo?.permissions || [])

const canView = (perm) => hasPermission(userPermissions.value, perm)

const isActive = (path) => {
  if (path === '/dashboard') {
    return route.path === '/dashboard'
  }
  return route.path.startsWith(path)
}
</script>

<style scoped>
.sidebar-nav {
  padding: var(--spacing-sm) 0;
  height: 100%;
  overflow-y: auto;
}

.nav-section {
  margin-bottom: var(--spacing-lg);
}

.nav-section-title {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--color-text-muted);
  padding: var(--spacing-sm) var(--spacing-lg);
  letter-spacing: 0.5px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-lg);
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: all var(--transition-fast);
  margin: 2px var(--spacing-sm);
  border-radius: var(--radius-md);
}

.nav-item:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
}

.nav-item.active {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.nav-item.active .nav-icon {
  transform: scale(1.1);
}

.nav-icon {
  font-size: 18px;
  width: 24px;
  text-align: center;
  transition: transform var(--transition-fast);
}

.nav-text {
  font-size: 14px;
  font-weight: 500;
}
</style>
