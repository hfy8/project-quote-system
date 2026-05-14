import request from './request'

export const feesAPI = {
  getByQuotation: (quotationId) => request.get(`/quotations/${quotationId}/fees`),
  create: (quotationId, data) => request.post(`/quotations/${quotationId}/fees`, data),
  update: (id, data) => request.put(`/fees/${id}`, data),
  delete: (id) => request.delete(`/fees/${id}`),
  getFeeTypes: () => request.get('/fee-types'),
  createFeeType: (data) => request.post('/fee-types', data),
  updateFeeType: (id, data) => request.put(`/fee-types/${id}`, data),
  deleteFeeType: (id) => request.delete(`/fee-types/${id}`)
}
