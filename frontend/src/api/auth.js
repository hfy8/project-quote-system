import request from './request'

export const authAPI = {
  login: (data) => request.post('/auth/login', data),
  logout: () => request.post('/auth/logout'),
  getUserInfo: () => request.get('/auth/me'),
  changePassword: (data) => request.post('/auth/change-password', data)
}
