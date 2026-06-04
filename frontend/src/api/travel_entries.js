import request from './request'

export const packingEntryAPI = {
  getList: (params) => request.get('/packing-entries', { params }),
  getByQuotation: (quotationId) => request.get('/packing-entries', { params: { quotation_id: quotationId } }),
  create: (quotationId, data) => request.post('/packing-entries', { quotation_id: quotationId, ...data }),
  update: (id, data) => request.put(`/packing-entries/${id}`, data),
  upsert: (data) => request.post('/packing-entries', data),
  delete: (id) => request.delete(`/packing-entries/${id}`),
}

export const travelPersonDaysAPI = {
  getList: (params) => request.get('/travel-person-days', { params }),
  getByQuotation: (quotationId) => request.get('/travel-person-days', { params: { quotation_id: quotationId } }),
  create: (quotationId, data) => request.post('/travel-person-days', { quotation_id: quotationId, ...data }),
  update: (id, data) => request.put(`/travel-person-days/${id}`, data),
  upsert: (data) => request.post('/travel-person-days', data),
  delete: (id) => request.delete(`/travel-person-days/${id}`),
}

export const travelPersonTripAPI = {
  getList: (params) => request.get('/travel-person-trips', { params }),
  getByQuotation: (quotationId) => request.get('/travel-person-trips', { params: { quotation_id: quotationId } }),
  create: (quotationId, data) => request.post('/travel-person-trips', { quotation_id: quotationId, ...data }),
  update: (id, data) => request.put(`/travel-person-trips/${id}`, data),
  upsert: (data) => request.post('/travel-person-trips', data),
  delete: (id) => request.delete(`/travel-person-trips/${id}`),
}
