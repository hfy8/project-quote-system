import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Quotations from '../views/Quotations.vue'
import QuotationEdit from '../views/QuotationEdit.vue'
import QuotationView from '../views/QuotationView.vue'
import Materials from '../views/Materials.vue'
import FeeTypes from '../views/FeeTypes.vue'
import Logs from '../views/Logs.vue'
import Users from '../views/Users.vue'
import Roles from '../views/Roles.vue'
import SystemSettings from '../views/SystemSettings.vue'
import FeeRatesConfig from '../views/FeeRatesConfig.vue'
import ExchangeRatesConfig from '../views/ExchangeRatesConfig.vue'
import ModuleAssignments from '../views/ModuleAssignments.vue'
import ParticipantTypePermissions from '../views/ParticipantTypePermissions.vue'
import TravelFeeConfig from '../views/TravelFeeConfig.vue'
import Layout from '../components/Layout.vue'
import VersionCompare from '../views/VersionCompare.vue'
import AIChat from '../views/AIChat.vue'
import Trends from '../views/Trends.vue'
import Messages from '../views/Messages.vue'

// 路由权限映射 - 与后端权限码一致
const routePermissionMap = {
  'Dashboard': 'dashboard.view',
  'Quotations': 'quotation.view',
  'QuotationNew': 'quotation.create',
  'QuotationDetail': 'quotation.view',
  'Materials': 'material.view',
  'FeeTypes': 'fee_type.view',
  'Logs': 'log.view',
  'Users': 'user.view',
  'Roles': 'role.view',
  'SystemSettings': 'system.view',
  'FeeRatesConfig': 'fee_rate.view',
  'ExchangeRatesConfig': 'exchange_rate.view',
  'ModuleAssignments': null,         // 所有人可访问
  'QuotationAssignmentView': null,  // 所有人可访问
  'ParticipantTypePermissions': 'participant_type_permission.view',
  'TravelFeeConfig': 'fee_type.view',
  'ChangeRequests': 'quotation.view',
  'VersionCompare': 'version.view',
  'AIChat': 'ai.query',
  'Trends': 'quotation.view',  // 趋势页：能看报价单的人都能看趋势
}

// 权限检查函数 - 支持通配符匹配
function hasPermission(userPermissions, requiredPermission) {
  if (!requiredPermission) return true  // null 表示无需权限
  if (!userPermissions || userPermissions.length === 0) return false
  if (userPermissions.includes('*')) return true  // admin 有所有权限

  // 精确匹配
  if (userPermissions.includes(requiredPermission)) return true

  // 通配符匹配 (如 'quotation.*' 匹配 'quotation.create')
  const parts = requiredPermission.split('.')
  for (const perm of userPermissions) {
    if (perm.endsWith('.*')) {
      const prefix = perm.slice(0, -2)
      if (parts[0] === prefix) return true
    }
  }

  return false
}

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    redirect: '/dashboard',
    component: Layout,
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard
      },
      {
        path: 'quotations',
        name: 'Quotations',
        component: Quotations
      },
      {
        path: 'quotations/new',
        name: 'QuotationNew',
        component: QuotationEdit
      },
      {
        path: 'quotations/:id',
        name: 'QuotationDetail',
        component: QuotationEdit
      },
      {
        path: 'quotations/:id/view',
        name: 'QuotationView',
        component: QuotationView
      },
      {
        path: 'change-requests',
        name: 'ChangeRequests',
        component: () => import('../views/ChangeRequests.vue')
      },
      {
        path: 'materials',
        name: 'Materials',
        component: Materials
      },
      {
        path: 'fee-types',
        name: 'FeeTypes',
        component: FeeTypes
      },
      {
        path: 'logs',
        name: 'Logs',
        component: Logs
      },
      {
        path: 'users',
        name: 'Users',
        component: Users
      },
      {
        path: 'roles',
        name: 'Roles',
        component: Roles
      },
      {
        path: 'system',
        name: 'SystemSettings',
        component: SystemSettings
      },
      {
        path: 'fee-rates',
        name: 'FeeRatesConfig',
        component: FeeRatesConfig
      },
      {
        path: 'exchange-rates',
        name: 'ExchangeRatesConfig',
        component: ExchangeRatesConfig
      },
      {
        path: 'my-assignments',
        name: 'ModuleAssignments',
        component: ModuleAssignments,
        permission: null
      },
      {
        path: 'my-assignments/quotations/:id/view',
        name: 'QuotationAssignmentView',
        component: QuotationView
      },
      {
        path: 'participant-type-permissions',
        name: 'ParticipantTypePermissions',
        component: ParticipantTypePermissions
      },
      {
        path: 'travel-fee-config',
        name: 'TravelFeeConfig',
        component: TravelFeeConfig
      },
      {
        path: 'ai-chat',
        name: 'AIChat',
        component: AIChat
      },
      {
        path: 'trends',
        name: 'Trends',
        component: Trends
      },
      {
        path: 'messages',
        name: 'Messages',
        component: Messages,
        meta: { title: '我的消息' }
      },

    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('token')

  // 登录页可以直接访问
  if (to.path === '/login') {
    next()
    return
  }

  // 其他页面需要登录
  if (!token) {
    next('/login')
    return
  }

  // 刷新权限（确保角色权限变更实时生效）
  const authStore = useAuthStore()
  try {
    await authStore.getUserInfo()
  } catch (e) {
    // token 无效或过期，跳转登录
    authStore.clearAuth()
    next('/login')
    return
  }

  // 动态权限检查
  const userPermissions = authStore.userInfo?.permissions || []
  const routeName = to.name

  // 路由需要的权限（无 mapping 说明无需权限）
  const required = routePermissionMap[routeName]

  if (required && !hasPermission(userPermissions, required)) {
    // 无权限，重定向到首页
    next('/dashboard')
    return
  }

  next()
})

export { hasPermission }
export default router
