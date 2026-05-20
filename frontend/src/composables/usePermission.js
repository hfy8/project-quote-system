// 权限判断 composable
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { hasPermission } from '../router'

export function usePermission() {
  const authStore = useAuthStore()

  const permissions = computed(() => authStore.userInfo?.permissions || [])

  const can = (perm) => hasPermission(permissions.value, perm)
  const canAny = (...perms) => perms.some(p => can(p))

  return { can, canAny, permissions }
}
