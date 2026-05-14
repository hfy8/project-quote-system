import request from './request'

const feeRatesAPI = {
  getList: () => request.get('/fee_rates'),
  create: (data) => request.post('/fee_rates', data),
  update: (id, data) => request.put(`/fee_rates/${id}`, data),
  delete: (id) => request.delete(`/fee_rates/${id}`),
  getByCategory: (category) => request.get(`/fee_rates/category/${category}`)
}

export { feeRatesAPI }
