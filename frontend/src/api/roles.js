import request from './request'

export const rolesAPI = {
  getList: (params) => request.get('/roles', { params }),
  getById: (id) => request.get(`/roles/${id}`),
  create: (data) => request.post('/roles', data),
  update: (id, data) => request.put(`/roles/${id}`, data),
  delete: (id) => request.delete(`/roles/${id}`)
}
