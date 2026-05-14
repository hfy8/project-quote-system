import request from './request'

export const logsAPI = {
  getList: (params = {}) => {
    return request({
      url: '/logs',
      method: 'GET',
      params
    })
  }
}
