import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

export function usePermission() {
  const authStore = useAuthStore()

  const permissions = computed(() => authStore.userInfo?.permissions || [])

  // 检查是否有某个权限
  const hasPermission = (permission) => {
    const perms = permissions.value
    if (perms.includes('*')) return true
    if (perms.includes(permission)) return true
    // 检查通配符权限
    const wildcard = permission.split('.')[0] + '.*'
    if (perms.includes(wildcard)) return true
    return false
  }

  // 检查是否有所有传入的权限
  const hasAllPermissions = (...perms) => {
    return perms.every(p => hasPermission(p))
  }

  // 检查是否有任意一个传入的权限
  const hasAnyPermission = (...perms) => {
    return perms.some(p => hasPermission(p))
  }

  return {
    permissions,
    hasPermission,
    hasAllPermissions,
    hasAnyPermission
  }
}
