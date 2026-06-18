import { defineStore } from 'pinia'

const STORAGE_KEY = 'aiChatHistory'
const MAX_SESSIONS = 20  // 最多保留 20 个会话
const MAX_MESSAGES_PER_SESSION = 100  // 每个会话最多 100 条消息

/**
 * AI 会话历史 Store
 *
 * 持久化到 localStorage（key: aiChatHistory）
 * 数据结构：
 * {
 *   sessions: [
 *     {
 *       id: 'conv_xxx',           // 后端 conversation_id（前端可能没有，用前端生成）
 *       title: '报价单 15 毛利率',  // 从首条 user 消息截取
 *       messages: [
 *         { id, role, content, ts, tools, toolCalls }
 *       ],
 *       createdAt: 1234567890,
 *       updatedAt: 1234567890,
 *     }
 *   ],
 *   currentSessionId: null,
 * }
 */
export const useAIChatStore = defineStore('aiChat', {
  state: () => {
    // 从 localStorage 恢复
    let stored = { sessions: [], currentSessionId: null }
    try {
      const raw = localStorage.getItem(STORAGE_KEY)
      if (raw) stored = JSON.parse(raw)
    } catch (e) {
      console.warn('AI 会话历史解析失败，重置:', e)
    }
    return stored
  },

  getters: {
    currentSession: (state) => {
      return state.sessions.find(s => s.id === state.currentSessionId) || null
    },
    sessionList: (state) => {
      // 按 updatedAt 倒序
      return [...state.sessions].sort((a, b) => b.updatedAt - a.updatedAt)
    },
  },

  actions: {
    /**
     * 创建新会话（无 id，待第一次发消息时回填）
     */
    createSession() {
      const session = {
        id: 'local_' + Date.now() + '_' + Math.random().toString(36).slice(2, 8),
        title: '新对话',
        messages: [],
        createdAt: Date.now(),
        updatedAt: Date.now(),
      }
      this.sessions.unshift(session)
      this.currentSessionId = session.id
      this._trim()
      this._save()
      return session
    },

    /**
     * 切换到指定会话（id 不存在则不动）
     */
    switchSession(id) {
      if (this.sessions.find(s => s.id === id)) {
        this.currentSessionId = id
        this._save()
        return true
      }
      return false
    },

    /**
     * 删除指定会话
     */
    deleteSession(id) {
      const idx = this.sessions.findIndex(s => s.id === id)
      if (idx >= 0) {
        this.sessions.splice(idx, 1)
        // 如果删的是当前会话，切到最新的一个
        if (this.currentSessionId === id) {
          this.currentSessionId = this.sessions[0]?.id || null
        }
        this._save()
      }
    },

    /**
     * 清空所有会话
     */
    clearAll() {
      this.sessions = []
      this.currentSessionId = null
      this._save()
    },

    /**
     * 添加一条消息到当前会话
     */
    addMessage(msg) {
      let session = this.currentSession
      if (!session) {
        session = this.createSession()
      }
      const enriched = {
        id: msg.id || ('m_' + Date.now() + '_' + Math.random().toString(36).slice(2, 6)),
        ts: msg.ts || Date.now(),
        ...msg,
      }
      session.messages.push(enriched)
      session.updatedAt = Date.now()

      // 自动从首条 user 消息提取标题
      if (session.title === '新对话' && enriched.role === 'user') {
        session.title = enriched.content.slice(0, 30) || '新对话'
      }

      // 限制消息数
      if (session.messages.length > MAX_MESSAGES_PER_SESSION) {
        session.messages = session.messages.slice(-MAX_MESSAGES_PER_SESSION)
      }
      this._trim()
      this._save()
    },

    /**
     * 替换最后一条消息（用于流式回答完成后）
     */
    replaceLastMessage(msg) {
      const session = this.currentSession
      if (!session || session.messages.length === 0) {
        return this.addMessage(msg)
      }
      Object.assign(session.messages[session.messages.length - 1], msg, {
        id: session.messages[session.messages.length - 1].id,  // 保留 id
        ts: msg.ts || session.messages[session.messages.length - 1].ts,
      })
      session.updatedAt = Date.now()
      this._save()
    },

    /**
     * 重命名会话
     */
    renameSession(id, newTitle) {
      const session = this.sessions.find(s => s.id === id)
      if (session && newTitle?.trim()) {
        session.title = newTitle.trim().slice(0, 50)
        this._save()
      }
    },

    // ===== 内部工具 =====
    _trim() {
      if (this.sessions.length > MAX_SESSIONS) {
        // 按 updatedAt 排序，删最旧的
        this.sessions.sort((a, b) => a.updatedAt - b.updatedAt)
        this.sessions = this.sessions.slice(-MAX_SESSIONS)
      }
    },

    _save() {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({
          sessions: this.sessions,
          currentSessionId: this.currentSessionId,
        }))
      } catch (e) {
        // localStorage 满（5MB）→ 删一半再试
        console.warn('AI 会话历史保存失败，尝试清理旧数据:', e)
        if (this.sessions.length > 5) {
          this.sessions = this.sessions.slice(0, 5)
          try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify({
              sessions: this.sessions,
              currentSessionId: this.currentSessionId,
            }))
          } catch (e2) {
            console.error('AI 会话历史彻底保存失败:', e2)
          }
        }
      }
    },
  },
})
