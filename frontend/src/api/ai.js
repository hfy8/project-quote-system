/**
 * AI 助手 API（流式 + 多轮对话）
 */
import request from './request'
import axios from 'axios'

// AI 助手 API
export const aiAPI = {
  // 非流式问答（兼容旧版）
  ask: (data) => request.post('/ai/ask', data),

  // 流式问答（SSE）
  // 返回 EventSource 类似的 Promise<reader>，调用方自己处理流
  // options.signal: AbortSignal，调用方中断时 cancel reader
  askStream: async (data, onEvent, options = {}) => {
    const token = localStorage.getItem('token')
    const response = await fetch('/api/ai/ask/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(data),
      signal: options.signal,
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder('utf-8')
    let buffer = ''

    // 如果 signal 中断，主动 cancel reader（关闭 TCP 流）
    if (options.signal) {
      const onAbort = () => {
        reader.cancel().catch(() => {})
      }
      if (options.signal.aborted) {
        onAbort()
        throw Object.assign(new Error('aborted'), { name: 'CanceledError' })
      }
      options.signal.addEventListener('abort', onAbort, { once: true })
    }

    try {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })

        // SSE 消息以 \n\n 分隔
        const parts = buffer.split('\n\n')
        buffer = parts.pop() || ''  // 最后一段可能不完整，留到下次

        for (const part of parts) {
          if (!part.trim()) continue
          const line = part.trim()
          if (!line.startsWith('data: ')) continue
          const dataStr = line.slice(6)
          try {
            const event = JSON.parse(dataStr)
            onEvent(event)
          } catch (e) {
            console.warn('解析 SSE 事件失败:', dataStr, e)
          }
        }
      }
    } catch (e) {
      if (e?.name === 'AbortError' || options.signal?.aborted) {
        throw Object.assign(new Error('aborted'), { name: 'CanceledError' })
      }
      throw e
    }
  },

  // 清除会话
  clearConversation: (conversationId) =>
    request.delete(`/ai/conversation/${conversationId}`),

  // 健康检查
  health: () => request.get('/ai/health'),
}

export default aiAPI
