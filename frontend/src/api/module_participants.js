import request from './request'

const moduleParticipantsAPI = {
  getList: (moduleId) => request.get(`/modules/${moduleId}/participants`),
  create: (moduleId, userIds) => request.post(`/modules/${moduleId}/participants`, { user_ids: userIds }),
  remove: (moduleId, participantId) => request.delete(`/modules/${moduleId}/participants/${participantId}`)
}

export { moduleParticipantsAPI }
