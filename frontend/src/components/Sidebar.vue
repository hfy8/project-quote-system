<template>
  <nav class="sidebar-nav">
    <div class="nav-section">
      <div class="nav-section-title">主菜单</div>
      <router-link to="/dashboard" class="nav-item" :class="{ active: isActive('/dashboard') }">
        <span class="nav-icon">🏠</span>
        <span class="nav-text">首页</span>
      </router-link>
      <router-link to="/quotations" class="nav-item" :class="{ active: isActive('/quotations') }" v-if="canView('quotation.view')">
        <span class="nav-icon">📋</span>
        <span class="nav-text">报价单管理</span>
      </router-link>
      <router-link to="/materials" class="nav-item" :class="{ active: isActive('/materials') }" v-if="canView('material.view')">
        <span class="nav-icon">📦</span>
        <span class="nav-text">原材料库</span>
      </router-link>
      <router-link to="/fee-types" class="nav-item" :class="{ active: isActive('/fee-types') }" v-if="canView('fee_type.view')">
        <span class="nav-icon">💰</span>
        <span class="nav-text">费用类型</span>
      </router-link>
      <router-link to="/my-assignments" class="nav-item" :class="{ active: isActive('/my-assignments') }" v-if="canView('module_assignment.view')">
        <span class="nav-icon">📌</span>
        <span class="nav-text">我的分配</span>
      </router-link>
    </div>

    <div class="nav-section" v-if="canView('user.view') || canView('role.view') || canView('fee_rate.view') || canView('exchange_rate.view') || canView('log.view')">
      <div class="nav-section-title">系统管理</div>
      <router-link to="/users" class="nav-item" :class="{ active: isActive('/users') }" v-if="canView('user.view')">
        <span class="nav-icon">👤</span>
        <span class="nav-text">用户管理</span>
      </router-link>
      <router-link to="/roles" class="nav-item" :class="{ active: isActive('/roles') }" v-if="canView('role.view')">
        <span class="nav-icon">👥</span>
        <span class="nav-text">角色管理</span>
      </router-link>
      <router-link to="/fee-rates" class="nav-item" :class="{ active: isActive('/fee-rates') }" v-if="canView('fee_rate.view')">
        <span class="nav-icon">📊</span>
        <span class="nav-text">费用系数</span>
      </router-link>
      <router-link to="/exchange-rates" class="nav-item" :class="{ active: isActive('/exchange-rates') }" v-if="canView('exchange_rate.view')">
        <span class="nav-icon">💱</span>
        <span class="nav-text">汇率配置</span>
      </router-link>
      <router-link to="/logs" class="nav-item" :class="{ active: isActive('/logs') }" v-if="canView('log.view')">
        <span class="nav-icon">📝</span>
        <span class="nav-text">操作日志</span>
      </router-link>
      <router-link to="/travel-fee-config" class="nav-item" :class="{ active: isActive('/travel-fee-config') }" v-if="canView('fee_type.view')">
        <span class="nav-icon">🚚</span>
        <span class="nav-text">运输差旅配置</span>
      </router-link>
    </div>

    <div class="nav-section" v-if="canView('system.view') || canView('participant_type_permission.view')">
      <div class="nav-section-title">设置</div>
      <router-link to="/system" class="nav-item" :class="{ active: isActive('/system') }" v-if="canView('system.view')">
        <span class="nav-icon">⚙️</span>
        <span class="nav-text">系统设置</span>
      </router-link>
      <router-link to="/participant-type-permissions" class="nav-item" :class="{ active: isActive('/participant-type-permissions') }" v-if="canView('participant_type_permission.view')">
        <span class="nav-icon">🔐</span>
        <span class="nav-text">参与人权限</span>
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { hasPermission } from '../router'

const route = useRoute()
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
