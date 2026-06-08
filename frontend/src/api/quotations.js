import request from './request'

export const quotationsAPI = {
  getList: (params) => request.get('/quotations', { params }),
  getChildren: (parentId) => request.get('/quotations', { params: { parent_id: parentId } }),
  getById: (id) => request.get(`/quotations/${id}`),
  create: (data) => request.post('/quotations', data),
  update: (id, data) => request.put(`/quotations/${id}`, data),
  delete: (id) => request.delete(`/quotations/${id}`),
  updateStatus: (id, status) => request.put(`/quotations/${id}/status`, { status }),
  copy: (id) => request.post(`/quotations/${id}/copy`),
  export: (id, type) => request.get(`/quotations/${id}/export/${type}`, { responseType: 'blob' }),
  getParticipants: (id) => request.get(`/quotations/${id}/participants`),
  addParticipant: (id, userId) => request.post(`/quotations/${id}/participants`, { user_id: userId }),
  removeParticipant: (quotationId, userId) => request.delete(`/quotations/${quotationId}/participants/${userId}`),
  archive: (id, remark) => request.post(`/quotations/${id}/archive`, { remark }),
  unarchive: (id) => request.post(`/quotations/${id}/unarchive`),
  getVersions: (id) => request.get(`/quotations/${id}/versions`),
  getVersionDetail: (id, versionNo) => request.get(`/quotations/${id}/versions/${versionNo}`)
}