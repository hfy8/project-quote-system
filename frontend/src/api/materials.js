import request from './request'

export const materialsAPI = {
  getList: (params) => request.get('/materials', { params }),
  getById: (id) => request.get(`/materials/${id}`),
  create: (data) => request.post('/materials', data),
  update: (id, data) => request.put(`/materials/${id}`, data),
  delete: (id) => request.delete(`/materials/${id}`),
  toggle: (id) => request.put(`/materials/${id}/toggle`, {}),
  import: (data) => request.post('/materials/import', { materials: data })
}
