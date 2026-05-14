<template>
  <nav class="sidebar-nav">
    <div class="nav-section">
      <div class="nav-section-title">主菜单</div>
      <router-link to="/dashboard" class="nav-item" :class="{ active: isActive('/dashboard') }">
        <span class="nav-icon">🏠</span>
        <span class="nav-text">首页</span>
      </router-link>
      <router-link to="/quotations" class="nav-item" :class="{ active: isActive('/quotations') }">
        <span class="nav-icon">📋</span>
        <span class="nav-text">报价单管理</span>
      </router-link>
      <router-link to="/materials" class="nav-item" :class="{ active: isActive('/materials') }">
        <span class="nav-icon">📦</span>
        <span class="nav-text">原材料库</span>
      </router-link>
      <router-link to="/fee-types" class="nav-item" :class="{ active: isActive('/fee-types') }">
        <span class="nav-icon">💰</span>
        <span class="nav-text">费用类型</span>
      </router-link>
    </div>

    <div class="nav-section">
      <div class="nav-section-title">系统管理</div>
      <router-link to="/users" class="nav-item" :class="{ active: isActive('/users') }">
        <span class="nav-icon">👤</span>
        <span class="nav-text">用户管理</span>
      </router-link>
      <router-link to="/roles" class="nav-item" :class="{ active: isActive('/roles') }">
        <span class="nav-icon">👥</span>
        <span class="nav-text">角色管理</span>
      </router-link>
      <router-link to="/fee-rates" class="nav-item" :class="{ active: isActive('/fee-rates') }">
        <span class="nav-icon">📊</span>
        <span class="nav-text">费用系数</span>
      </router-link>
      <router-link to="/exchange-rates" class="nav-item" :class="{ active: isActive('/exchange-rates') }">
        <span class="nav-icon">💱</span>
        <span class="nav-text">汇率配置</span>
      </router-link>
      <router-link to="/logs" class="nav-item" :class="{ active: isActive('/logs') }">
        <span class="nav-icon">📝</span>
        <span class="nav-text">操作日志</span>
      </router-link>
    </div>

    <div class="nav-section">
      <div class="nav-section-title">设置</div>
      <router-link to="/system" class="nav-item" :class="{ active: isActive('/system') }">
        <span class="nav-icon">⚙️</span>
        <span class="nav-text">系统设置</span>
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

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
