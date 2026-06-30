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

// 标记单条消息为已读 (PUT /messages/{id}/read, Layout.vue 用)
export const markAsRead = (messageId) => {
  return request({
    url: `/messages/${messageId}/read`,
    method: 'put'
  })
}

// 标记所有消息为已读 (PUT /messages/read-all)
export const markAllAsRead = () => {
  return request({
    url: '/messages/read-all',
    method: 'put'
  })
}

// 标记所有消息为已读 (别名, Messages.vue 用)
export const markAllRead = () => markAllAsRead()

// 批量标记指定消息为已读 (POST /messages/read, Messages.vue 用)
export const markRead = (messageId) => {
  return request({
    url: '/messages/read',
    method: 'post',
    data: { message_ids: [messageId] }
  })
}

const messagesAPI = {
  getMessages,
  getUnreadCount,
  markRead,
  markAllRead,
  markAsRead,
  markAllAsRead,
}

export default messagesAPI