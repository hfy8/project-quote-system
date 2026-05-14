import request from './request'

export const modulesAPI = {
  getByQuotation: (quotationId) => request.get(`/quotations/${quotationId}/modules`),
  getById: (id) => request.get(`/modules/${id}`),
  create: (quotationId, data) => request.post(`/quotations/${quotationId}/modules`, data),
  update: (id, data) => request.put(`/modules/${id}`, data),
  delete: (id) => request.delete(`/modules/${id}`),
  getMaterials: (moduleId) => request.get(`/modules/${moduleId}/materials`),
  addMaterial: (moduleId, data) => request.post(`/modules/${moduleId}/materials`, data),
  updateMaterial: (id, data) => request.put(`/module_materials/${id}`, data),
  removeMaterial: (id) => request.delete(`/module_materials/${id}`),
  getSummary: (moduleId) => request.get(`/modules/${moduleId}/summary`)
}
