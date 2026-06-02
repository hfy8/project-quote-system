import request from './request'

export const packingTypeAPI = {
  getList: (params) => request.get('/packing-types', { params }),
  create: (data) => request.post('/packing-types', data),
  update: (id, data) => request.put(`/packing-types/${id}`, data),
  delete: (id) => request.delete(`/packing-types/${id}`),
}

export const travelCategoryAPI = {
  getList: (params) => request.get('/travel-categories', { params }),
  create: (data) => request.post('/travel-categories', data),
  update: (id, data) => request.put(`/travel-categories/${id}`, data),
  delete: (id) => request.delete(`/travel-categories/${id}`),
}

export const travelDayRateAPI = {
  getList: (params) => request.get('/travel-day-rates', { params }),
  create: (data) => request.post('/travel-day-rates', data),
  update: (id, data) => request.put(`/travel-day-rates/${id}`, data),
  delete: (id) => request.delete(`/travel-day-rates/${id}`),
}

export const travelModeAPI = {
  getList: (params) => request.get('/travel-modes', { params }),
  create: (data) => request.post('/travel-modes', data),
  update: (id, data) => request.put(`/travel-modes/${id}`, data),
  delete: (id) => request.delete(`/travel-modes/${id}`),
}

export const travelPersonTripFeeAPI = {
  getList: (params) => request.get('/travel-person-trip-fees', { params }),
  create: (data) => request.post('/travel-person-trip-fees', data),
  update: (id, data) => request.put(`/travel-person-trip-fees/${id}`, data),
  delete: (id) => request.delete(`/travel-person-trip-fees/${id}`),
}
