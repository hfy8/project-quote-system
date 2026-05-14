import request from './request'

export const versionsAPI = {
  getByQuotation: (quotationId) => request.get(`/quotations/${quotationId}/versions`),
  getById: (id) => request.get(`/versions/${id}`),
  create: (quotationId, data) => request.post(`/quotations/${quotationId}/versions`, data),
  rollback: (id) => request.post(`/versions/${id}/rollback`),
  compare: (id, otherId) => request.get(`/versions/${id}/compare/${otherId}`)
}
