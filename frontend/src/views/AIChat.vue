<template>
  <div class="ai-chat-page">
    <div class="page-header-bar">
      <div class="header-left">
        <h1 class="page-title">AI 智能助手</h1>
        <span class="page-desc">基于 15 个工具的智能问答 + 业务知识库</span>
      </div>
      <div class="header-right">
        <el-button @click="newConversation">
          <el-icon><Plus /></el-icon>
          新对话
        </el-button>
      </div>
    </div>

    <div class="chat-container card">
      <!-- 消息列表 -->
      <div class="messages" ref="messagesRef">
        <div
          v-for="(msg, idx) in messages"
          :key="idx"
          :class="['message', `message-${msg.role}`]"
        >
          <div class="message-avatar">
            <el-avatar :size="32" :style="{ background: msg.role === 'user' ? '#0D9488' : '#4F46E5' }">
              {{ msg.role === 'user' ? '我' : 'AI' }}
            </el-avatar>
          </div>
          <div class="message-content">
            <div class="message-text" v-html="formatMessage(msg.content)"></div>
            <div v-if="msg.tools && msg.tools.length" class="message-tools">
              <el-tag
                v-for="t in msg.tools"
                :key="t"
                size="small"
                type="info"
                effect="plain"
              >
                🔧 {{ t }}
              </el-tag>
            </div>
          </div>
        </div>

        <!-- 流式回答时显示打字指示 -->
        <div v-if="streaming" class="message message-assistant">
          <div class="message-avatar">
            <el-avatar :size="32" style="background: #4F46E5">AI</el-avatar>
          </div>
          <div class="message-content">
            <div class="message-text">
              <span v-if="currentAnswer">{{ currentAnswer }}</span>
              <span v-else class="thinking">正在思考<span class="dots">...</span></span>
              <span v-if="streaming" class="cursor">▊</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区 -->
      <div class="input-area">
        <el-input
          v-model="inputText"
          type="textarea"
          :rows="2"
          placeholder="问点什么...例如：报价单 15 毛利率多少？物料库有哪些 CPU？"
          :disabled="streaming"
          @keydown.enter.ctrl="sendMessage"
        />
        <div class="input-actions">
          <span class="hint">⌘ + Enter 发送</span>
          <el-button
            type="primary"
            :loading="streaming"
            :disabled="!inputText.trim()"
            @click="sendMessage"
          >
            发送
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { aiAPI } from '../api/ai'

const messages = ref([])  // 历史消息
const inputText = ref('')
const streaming = ref(false)
const currentAnswer = ref('')
const conversationId = ref(null)
const messagesRef = ref(null)

// 欢迎语
const welcomeMessage = {
  role: 'assistant',
  content: '你好！我是项目报价系统的 AI 助手，可以帮你：\n\n- 📋 查询报价单、物料、模块\n- 💰 算总价、对比报价单\n- 🔍 审报价单（异常检测）\n- 📊 分析业务趋势\n- 💡 查业务知识库\n\n直接问就行！',
  tools: [],
}

// Markdown 简单渲染（处理粗体 + 换行 + 列表）
function formatMessage(text) {
  if (!text) return ''
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>')
}

async function scrollToBottom() {
  await nextTick()
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}

async function sendMessage() {
  const text = inputText.value.trim()
  if (!text || streaming.value) return

  // 1. 用户消息
  messages.value.push({ role: 'user', content: text })
  inputText.value = ''
  await scrollToBottom()

  // 2. 流式调用
  streaming.value = true
  currentAnswer.value = ''
  let fullAnswer = ''
  let toolsUsed = []

  try {
    await aiAPI.askStream(
      { query: text, conversation_id: conversationId.value },
      (event) => {
        const type = event.type
        if (type === 'start') {
          // 保存 conversation_id（后端从 SSE start/done 事件返回）
          if (event.conversation_id) {
            conversationId.value = event.conversation_id
          }
        } else if (type === 'token') {
          currentAnswer.value += event.content
          fullAnswer += event.content
          scrollToBottom()
        } else if (type === 'tool_call') {
          if (!toolsUsed.includes(event.name)) {
            toolsUsed.push(event.name)
          }
        } else if (type === 'done') {
          // 保存 conversation_id
          if (event.conversation_id) {
            conversationId.value = event.conversation_id
          }
          // 收尾
          messages.value.push({
            role: 'assistant',
            content: fullAnswer || event.answer,
            tools: toolsUsed,
          })
          currentAnswer.value = ''
        } else if (type === 'error') {
          ElMessage.error(`AI 错误: ${event.message}`)
          messages.value.push({
            role: 'assistant',
            content: `[错误] ${event.message}`,
            tools: [],
          })
        }
      },
    )
  } catch (e) {
    ElMessage.error(`请求失败: ${e.message}`)
    messages.value.push({
      role: 'assistant',
      content: `[网络错误] ${e.message}`,
      tools: [],
    })
  } finally {
    streaming.value = false
    await scrollToBottom()
  }
}

function newConversation() {
  messages.value = [welcomeMessage]
  conversationId.value = null
  currentAnswer.value = ''
  ElMessage.success('已开始新对话')
}

onMounted(() => {
  messages.value = [welcomeMessage]
})
</script>

<style scoped>
.ai-chat-page {
  padding: 24px;
  max-width: 1100px;
  margin: 0 auto;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 200px);
  min-height: 500px;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.message-user {
  flex-direction: row-reverse;
}

.message-content {
  max-width: 70%;
  background: #f3f4f6;
  padding: 12px 16px;
  border-radius: 12px;
  word-wrap: break-word;
  white-space: pre-wrap;
}

.message-user .message-content {
  background: #0D9488;
  color: white;
}

.message-text {
  line-height: 1.6;
  font-size: 14px;
}

.message-tools {
  margin-top: 8px;
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.thinking {
  color: #9ca3af;
  font-style: italic;
}

.dots::after {
  content: '';
  animation: dots 1.5s steps(4) infinite;
}

@keyframes dots {
  0% { content: ''; }
  25% { content: '.'; }
  50% { content: '..'; }
  75% { content: '...'; }
}

.cursor {
  animation: blink 1s infinite;
  color: #0D9488;
}

@keyframes blink {
  50% { opacity: 0; }
}

.input-area {
  border-top: 1px solid #e5e7eb;
  padding: 16px;
  background: white;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.hint {
  font-size: 12px;
  color: #9ca3af;
}
</style>
