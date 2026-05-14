import { defineStore } from 'pinia'
import { authAPI } from '../api'

const USER_INFO_KEY = 'userInfo'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem(USER_INFO_KEY) || 'null')
  }),

  getters: {
    isLoggedIn: (state) => !!state.token
  },

  actions: {
    async login(username, password) {
      const res = await authAPI.login({ username, password })
      this.token = res.access_token
      this.userInfo = res.user
      localStorage.setItem('token', res.access_token)
      localStorage.setItem(USER_INFO_KEY, JSON.stringify(res.user))
      return res
    },

    async logout() {
      try {
        await authAPI.logout()
      } finally {
        this.token = ''
        this.userInfo = null
        localStorage.removeItem('token')
        localStorage.removeItem(USER_INFO_KEY)
      }
    },

    async getUserInfo() {
      const res = await authAPI.getUserInfo()
      this.userInfo = res
      localStorage.setItem(USER_INFO_KEY, JSON.stringify(res))
      return res
    },

    async changePassword(data) {
      const res = await authAPI.changePassword(data)
      return res
    }
  }
})
