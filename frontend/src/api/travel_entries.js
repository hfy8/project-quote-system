import request from './request'

export const packingEntryAPI = {
  getList: (params) => request.get('/packing-entries', { params }),
  upsert: (data) => request.post('/packing-entries', data),
  delete: (id) => request.delete(`/packing-entries/${id}`),
}

export const travelPersonDaysAPI = {
  getList: (params) => request.get('/travel-person-days', { params }),
  upsert: (data) => request.post('/travel-person-days', data),
  delete: (id) => request.delete(`/travel-person-days/${id}`),
}

export const travelPersonTripAPI = {
  getList: (params) => request.get('/travel-person-trips', { params }),
  upsert: (data) => request.post('/travel-person-trips', data),
  delete: (id) => request.delete(`/travel-person-trips/${id}`),
}
