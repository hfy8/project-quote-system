import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const status = error.response?.status
    const message = error.response?.data?.msg || error.response?.data?.message || ''

    // token 损坏（JWT 格式异常）-> 清空并跳转登录
    if (status === 422 && message.includes('Not enough segments')) {
      localStorage.removeItem('token')
      router.push('/login')
      ElMessage.error('登录状态异常，请重新登录')
      return Promise.reject(error)
    }

    if (status === 401) {
      localStorage.removeItem('token')
      router.push('/login')
      ElMessage.error('登录已过期，请重新登录')
    } else {
      ElMessage.error(message || '请求失败')
    }
    return Promise.reject(error)
  }
)

export default request
