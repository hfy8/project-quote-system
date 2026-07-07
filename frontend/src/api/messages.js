import request from '../utils/request'

const messagesAPI = {
  // 获取消息列表
  getMessages: (params) => request.get('/messages', { params }),
  
  // 获取未读消息数量
  getUnreadCount: () => request.get('/messages/unread-count'),
  
  // 标记单条消息为已读 (PUT /messages/{id}/read, Layout.vue 用)
  markAsRead: (messageId) => request.put(`/messages/${messageId}/read`),
  
  // 标记所有消息为已读 (PUT /messages/read-all)
  markAllAsRead: () => request.put('/messages/read-all'),
  
  // 批量标记指定消息为已读 (POST /messages/read, Messages.vue 用)
  markRead: (messageId) => request.post('/messages/read', { message_ids: [messageId] }),
  
  // 标记所有消息为已读 (别名)
  markAllRead: () => request.put('/messages/read-all'),
}

export { messagesAPI }