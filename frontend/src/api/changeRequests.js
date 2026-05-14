import request from '../utils/request'

const changeRequestsAPI = {
  // 获取变更申请列表
  getList: (params) => request.get('/change-requests', { params }),
  
  // 获取待审核的变更申请（报价单负责人视角）
  getPending: () => request.get('/change-requests/pending'),
  
  // 提交变更申请
  create: (data) => request.post('/change-requests', data),
  
  // 批准变更申请
  approve: (id, remark) => request.post(`/change-requests/${id}/approve`, { remark }),
  
  // 拒绝变更申请
  reject: (id, remark) => request.post(`/change-requests/${id}/reject`, { remark })
}

export default changeRequestsAPI
