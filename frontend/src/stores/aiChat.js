import { defineStore } from 'pinia'
import { aiAPI } from '../api/ai'

/**
 * AI 会话历史 Store
 *
 * 后端持久化（PostgreSQL），替代 localStorage
 */
export const useAIChatStore = defineStore('aiChat', {
  state: () => ({
    sessions: [],
    currentSessionId: null,
    _loaded: false,
  }),

  getters: {
    currentSession: (state) => {
      return state.sessions.find(s => s.id === state.currentSessionId) || null
    },
    sessionList: (state) => {
      return [...state.sessions].sort((a, b) => (b.updatedAt || b.updated_at || '') > (a.updatedAt || a.updated_at || '') ? 1 : -1)
    },
  },

  actions: {
    /** 从后端加载会话列表 */
    async loadSessions() {
      try {
        const res = await aiAPI.getConversations()
        this.sessions = (res.data || []).map(s => ({
          id: s.id,
          title: s.title || '新对话',
          messages: [],
          createdAt: s.created_at,
          updatedAt: s.updated_at,
        }))
        this._loaded = true
      } catch (e) {
        console.warn('加载 AI 会话列表失败:', e)
        this.sessions = []
      }
    },

    /** 创建新会话 */
    async createSession(title = '新对话') {
      try {
        const res = await aiAPI.createConversation(title)
        const session = {
          id: res.data.id,
          title: res.data.title || title,
          messages: [],
          createdAt: res.data.created_at,
          updatedAt: res.data.updated_at,
        }
        this.sessions.unshift(session)
        this.currentSessionId = session.id
        return session
      } catch (e) {
        console.warn('创建会话失败:', e)
        return null
      }
    },

    /** 切换会话，加载消息 */
    async switchSession(id) {
      const exists = this.sessions.find(s => s.id === id)
      if (!exists) return false
      this.currentSessionId = id
      // 异步加载该会话的消息（如果还没加载）
      if (!exists.messages || exists.messages.length === 0) {
        await this._loadMessages(id)
      }
      return true
    },

    /** 加载指定会话的消息 */
    async _loadMessages(conversationId) {
      try {
        const res = await aiAPI.getMessages(conversationId)
        const msgs = (res.data || []).map(m => ({
          id: m.id,
          role: m.role,
          content: m.content,
          ts: m.created_at,
          toolCalls: m.tool_calls ? JSON.parse(m.tool_calls) : undefined,
        }))
        const session = this.sessions.find(s => s.id === conversationId)
        if (session) {
          session.messages = msgs
          if (msgs.length > 0) {
            const last = msgs[msgs.length - 1]
            session.updatedAt = last.ts
          }
        }
      } catch (e) {
        console.warn('加载消息失败:', e)
      }
    },

    /** 删除会话 */
    async deleteSession(id) {
      try {
        await aiAPI.deleteConversation(id)
        this.sessions = this.sessions.filter(s => s.id !== id)
        if (this.currentSessionId === id) {
          this.currentSessionId = this.sessions[0]?.id || null
        }
      } catch (e) {
        console.warn('删除会话失败:', e)
      }
    },

    /** 重命名会话 */
    async renameSession(id, title) {
      try {
        await aiAPI.renameConversation(id, title)
        const session = this.sessions.find(s => s.id === id)
        if (session) session.title = title
      } catch (e) {
        console.warn('重命名会话失败:', e)
      }
    },

    /** 清空会话消息 */
    async clearSessionMessages(id) {
      try {
        await aiAPI.clearMessages(id)
        const session = this.sessions.find(s => s.id === id)
        if (session) session.messages = []
      } catch (e) {
        console.warn('清空消息失败:', e)
      }
    },

    /** 追加消息到当前会话 */
    appendMessage(msg) {
      const session = this.sessions.find(s => s.id === this.currentSessionId)
      if (session) {
        session.messages.push({
          id: msg.id || Date.now(),
          role: msg.role,
          content: msg.content,
          ts: msg.ts || new Date().toISOString(),
          toolCalls: msg.toolCalls,
        })
      }
    },

    /** 初始化（加载会话列表） */
    async init() {
      if (!this._loaded) {
        await this.loadSessions()
        if (this.sessions.length > 0 && !this.currentSessionId) {
          this.currentSessionId = this.sessions[0].id
        }
      }
    },
  },
})
