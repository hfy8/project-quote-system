import request from './request'

export const usersAPI = {
  getList: (params) => request.get('/users', { params }),
  getById: (id) => request.get(`/users/${id}`),
  getRoles: () => request.get('/users/roles'),
  create: (data) => request.post('/users', data),
  update: (id, data) => request.put(`/users/${id}`, data),
  delete: (id) => request.delete(`/users/${id}`),
  resetPassword: (id) => request.post(`/users/${id}/reset-password`)
}
