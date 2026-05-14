import request from './request'

const exchangeRatesAPI = {
  getList: () => request.get('/exchange_rates'),
  getBaseCurrency: () => request.get('/exchange_rates/base'),
  create: (data) => request.post('/exchange_rates', data),
  createExchangeRate: (data) => request.post('/exchange_rates', data),
  update: (id, data) => request.put(`/exchange_rates/${id}`, data),
  updateExchangeRate: (id, data) => request.put(`/exchange_rates/${id}`, data),
  setBaseCurrency: (id) => request.post(`/exchange_rates/${id}/set-base`),
  delete: (id) => request.delete(`/exchange_rates/${id}`),
  convert: (from, to, amount) => request.get(`/exchange_rates/convert?from=${from}&to=${to}&amount=${amount}`)
}

export { exchangeRatesAPI }
