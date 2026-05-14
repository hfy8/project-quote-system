import request from '../utils/request'

// 获取消息列表
export const getMessages = (params) => {
  return request({
    url: '/messages',
    method: 'get',
    params
  })
}

// 获取未读消息数量
export const getUnreadCount = () => {
  return request({
    url: '/messages/unread-count',
    method: 'get'
  })
}

// 标记单条消息为已读
export const markAsRead = (messageId) => {
  return request({
    url: `/messages/${messageId}/read`,
    method: 'put'
  })
}

// 标记所有消息为已读
export const markAllAsRead = () => {
  return request({
    url: '/messages/read-all',
    method: 'put'
  })
}

const messagesAPI = {
  getMessages,
  getUnreadCount,
  markAsRead,
  markAllAsRead
}

export default messagesAPI