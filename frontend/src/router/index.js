import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Quotations from '../views/Quotations.vue'
import QuotationEdit from '../views/QuotationEdit.vue'
import Materials from '../views/Materials.vue'
import FeeTypes from '../views/FeeTypes.vue'
import Logs from '../views/Logs.vue'
import Users from '../views/Users.vue'
import Roles from '../views/Roles.vue'
import SystemSettings from '../views/SystemSettings.vue'
import FeeRatesConfig from '../views/FeeRatesConfig.vue'
import ExchangeRatesConfig from '../views/ExchangeRatesConfig.vue'
import ModuleAssignments from '../views/ModuleAssignments.vue'
import Layout from '../components/Layout.vue'

// 路由权限映射 - 与后端 ROLE_PERMISSIONS 保持一致
const routePermissions = {
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
  'ModuleAssignments': null,
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
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
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

  // 检查权限
  const requiredPermission = routePermissions[to.name]
  if (requiredPermission) {
    const authStore = useAuthStore()
    const userPermissions = authStore.userInfo?.permissions || []

    // 使用通配符匹配
    if (!hasPermission(userPermissions, requiredPermission)) {
      // 没有权限，重定向到首页
      next('/dashboard')
      return
    }
  }

  next()
})

export { hasPermission }
export default router
