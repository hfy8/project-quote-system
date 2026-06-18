<template>
  <div class="ai-chat-page">
    <!-- 顶部栏 -->
    <div class="top-bar">
      <div class="brand">
        <div class="logo">🤖</div>
        <div class="brand-text">
          <h1>AI 智能助手</h1>
          <span class="brand-sub">{{ toolCount }} 个业务工具 · 流式响应</span>
        </div>
      </div>
      <div class="top-actions">
        <el-button v-if="streaming" type="warning" plain size="small" @click="stopGeneration">
          <el-icon><CircleClose /></el-icon>
          停止生成
        </el-button>
        <el-button size="small" @click="newConversation">
          <el-icon><Plus /></el-icon>
          新对话
        </el-button>
      </div>
    </div>

    <!-- 聊天主区 -->
    <div class="chat-shell">
      <!-- 消息流 -->
      <div class="messages" ref="messagesRef">
        <!-- 欢迎卡片：只在空消息时显示 -->
        <div v-if="messages.length === 0" class="welcome">
          <div class="welcome-icon">💬</div>
          <h2>你好，我是报价系统 AI 助手</h2>
          <p>可以查报价单、算总价、审异常、分析趋势 — 直接问就行</p>
          <div class="suggestions">
            <div
              v-for="(s, i) in suggestions"
              :key="i"
              class="suggestion-chip"
              @click="askSuggestion(s)"
            >
              <span class="chip-icon">{{ s.icon }}</span>
              <span class="chip-text">{{ s.text }}</span>
            </div>
          </div>
        </div>

        <!-- 历史消息 -->
        <template v-for="(msg, idx) in messages" :key="msg.id || idx">
          <div :class="['message', `message-${msg.role}`]">
            <div class="avatar">
              <el-avatar
                :size="36"
                :style="{
                  background: msg.role === 'user' ? '#0D9488' : 'linear-gradient(135deg, #4F46E5, #7C3AED)',
                }"
              >
                {{ msg.role === 'user' ? '我' : 'AI' }}
              </el-avatar>
            </div>
            <div class="bubble-wrap">
              <div :class="['bubble', `bubble-${msg.role}`]">
                <div class="bubble-content" v-html="renderMarkdownImmediate(msg.content)"></div>
              </div>
              <!-- 工具调用折叠卡片（已完成消息）-->
              <div v-if="msg.toolCalls && msg.toolCalls.length" class="tool-calls">
                <details
                  v-for="(tc, i) in msg.toolCalls"
                  :key="i"
                  class="tool-call-card"
                >
                  <summary>
                    <span class="tool-icon">🔧</span>
                    <span class="tool-name">{{ tc.name }}</span>
                    <span class="tool-status" :class="tc.result ? 'ok' : 'pending'">
                      {{ tc.result ? '✓' : '…' }}
                    </span>
                  </summary>
                  <div class="tool-detail">
                    <div v-if="tc.arguments && Object.keys(tc.arguments).length" class="tool-section">
                      <div class="tool-label">参数：</div>
                      <pre class="tool-pre">{{ formatJSON(tc.arguments) }}</pre>
                    </div>
                    <div v-if="tc.result" class="tool-section">
                      <div class="tool-label">结果：</div>
                      <pre class="tool-pre">{{ tc.result }}</pre>
                    </div>
                  </div>
                </details>
              </div>
              <!-- 简单 tag（向后兼容，没有详细 tool_call 信息的场景）-->
              <div v-else-if="msg.tools && msg.tools.length" class="tools-row">
                <el-tag
                  v-for="t in msg.tools"
                  :key="t"
                  size="small"
                  type="info"
                  effect="plain"
                  round
                >
                  🔧 {{ t }}
                </el-tag>
              </div>
              <div v-if="msg.ts" class="ts">{{ formatTime(msg.ts) }}</div>
            </div>
          </div>
        </template>

        <!-- 流式回答中（用防抖渲染避免闪烁）-->
        <div v-if="streaming" class="message message-assistant">
          <div class="avatar">
            <el-avatar
              :size="36"
              :style="{ background: 'linear-gradient(135deg, #4F46E5, #7C3AED)' }"
            >
              AI
            </el-avatar>
          </div>
          <div class="bubble-wrap">
            <div class="bubble bubble-assistant">
              <div class="bubble-content">
                <span v-if="currentAnswer" v-html="renderedCurrentAnswer"></span>
                <span v-else-if="currentToolCalls.length === 0" class="thinking">
                  正在思考<span class="dots">.</span>
                </span>
                <span v-if="streaming" class="cursor">▍</span>
              </div>
            </div>
            <!-- 流式期间的 tool_calls（实时显示）-->
            <div v-if="currentToolCalls.length" class="tool-calls">
              <details
                v-for="(tc, i) in currentToolCalls"
                :key="i"
                class="tool-call-card"
                open
              >
                <summary>
                  <span class="tool-icon">🔧</span>
                  <span class="tool-name">{{ tc.name }}</span>
                  <span class="tool-status" :class="tc.result ? 'ok' : 'pending'">
                    {{ tc.result ? '✓' : '…' }}
                  </span>
                </summary>
                <div class="tool-detail">
                  <div v-if="tc.arguments && Object.keys(tc.arguments).length" class="tool-section">
                    <div class="tool-label">参数：</div>
                    <pre class="tool-pre">{{ formatJSON(tc.arguments) }}</pre>
                  </div>
                  <div v-if="tc.result" class="tool-section">
                    <div class="tool-label">结果：</div>
                    <pre class="tool-pre">{{ tc.result }}</pre>
                  </div>
                </div>
              </details>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区 -->
      <div class="composer">
        <div class="composer-inner">
          <el-input
            v-model="inputText"
            type="textarea"
            :autosize="{ minRows: 1, maxRows: 6 }"
            placeholder="问点什么... Shift+Enter 换行，Enter 发送"
            :disabled="false"
            @keydown="onKeydown"
            class="composer-input"
          />
          <el-button
            type="primary"
            :icon="ArrowUpBold"
            circle
            size="large"
            :disabled="!inputText.trim()"
            @click="sendMessage"
            class="send-btn"
          />
        </div>
        <div class="composer-foot">
          <span class="foot-hint">AI 回答可能不准确，关键数据请人工核对</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onBeforeUnmount, watch, computed } from 'vue'
import { Plus, CircleClose, ArrowUpBold } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { aiAPI } from '../api/ai'

// ===== 防抖渲染：避免流式过程中每个 token 都跑 regex =====
// 流式期间 100ms 才 render 一次，用户感知不到延迟，但 Vue 触发次数减少 10x
const renderedCurrentAnswer = ref('')
let _renderTimer = null
function scheduleRender(text) {
  if (_renderTimer) clearTimeout(_renderTimer)
  _renderTimer = setTimeout(() => {
    renderedCurrentAnswer.value = renderMarkdownImmediate(text)
  }, 100)
}

// 立即渲染（用于已完成的消息）
function renderSync(text) {
  return renderMarkdownImmediate(text)
}

// ===== 状态 =====
// 单条消息结构：
//   { id, role, content, ts, tools: ['name1'], toolCalls: [{name, args, result}] }
const messages = ref([])         // 已完成的消息
const inputText = ref('')
const streaming = ref(false)
const currentAnswer = ref('')
const currentToolCalls = ref([]) // 流式期间的 tool_call 列表（实时累计）
const conversationId = ref(null)
const messagesRef = ref(null)
const toolCount = ref(15)
const abortController = ref(null)
let nextId = 1

// ===== 建议问题（欢迎页 + 始终可点）=====
const suggestions = [
  { icon: '📋', text: '报价单 14 毛利率多少？' },
  { icon: '💰', text: '对比报价单 12 和 15 的总价' },
  { icon: '🔍', text: '审一下最新报价单有没有异常' },
  { icon: '📊', text: '本月已审批的报价单数量' },
  { icon: '📦', text: '物料库有哪些 PLC？' },
  { icon: '💡', text: '公司利润率计算规则是什么？' },
]

// ===== 工具：轻量 Markdown 渲染 =====
// 防抖版本：流式过程中 100ms 才 render 一次，避免每个 token 都跑 regex 导致闪烁
let _renderCache = new WeakMap()  // WeakMap 避免内存泄漏
let _renderDebounceTimer = null

function renderMarkdownDebounced(text, callback) {
  if (_renderDebounceTimer) clearTimeout(_renderDebounceTimer)
  _renderDebounceTimer = setTimeout(() => {
    callback(renderMarkdownImmediate(text))
  }, 100)
}
function escapeHtml(s) {
  return String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
}

function renderMarkdownImmediate(text) {
  if (!text) return ''

  // think 块处理：转为 <details> 折叠标签（用户可展开看 AI 推理过程）
  // 匹配 多个 think 块（有些模型会多轮思考）
  const thinkRe = /<think(?:ing)?>([\s\S]*?)<\/think>/gi
  let thinkRendered = ''
  let match
  while ((match = thinkRe.exec(text)) !== null) {
    const thinkContent = escapeHtml(match[1].trim())
    thinkRendered += `<details class="think-block"><summary>💭 AI 思考过程（点击展开）</summary><pre class="think-pre">${thinkContent}</pre></details>`
  }

  // 移除所有 think 块
  const cleaned = text.replace(thinkRe, '').trim()

  // 先按代码块切（保留代码块内容）
  const codeBlockRe = /```([a-zA-Z0-9_+-]*)\n?([\s\S]*?)```/g
  const parts = []
  let lastIdx = 0
  let m
  while ((m = codeBlockRe.exec(text)) !== null) {
    parts.push({ type: 'text', value: text.slice(lastIdx, m.index) })
    parts.push({ type: 'code', lang: m[1] || 'text', value: m[2] })
    lastIdx = m.index + m[0].length
  }
  parts.push({ type: 'text', value: text.slice(lastIdx) })

  // think 块渲染：拼接头部（顶部已提取，下面仅拼接）
  return thinkRendered + parts
    .map((p) => {
      if (p.type === 'code') {
        return `<pre class="md-code"><code class="lang-${escapeHtml(p.lang)}">${escapeHtml(p.value)}</code></pre>`
      }
      return renderInline(p.value)
    })
    .join('')
}

function renderInline(text) {
  // 行内处理：转义 → 代码/加粗/斜体/换行
  return escapeHtml(text)
    // 行内代码
    .replace(/`([^`]+)`/g, '<code class="md-inline-code">$1</code>')
    // 加粗
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    // 斜体
    .replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>')
    // 标题（简单支持 # ## ###）
    .replace(/^### (.+)$/gm, '<h4 class="md-h">$1</h4>')
    .replace(/^## (.+)$/gm, '<h3 class="md-h">$1</h3>')
    .replace(/^# (.+)$/gm, '<h2 class="md-h">$1</h2>')
    // 列表项
    .replace(/^[\-\*] (.+)$/gm, '<li class="md-li">$1</li>')
    // 连续 li 包成 ul
    .replace(/((?:<li class="md-li">.*<\/li>\n?)+)/g, '<ul class="md-ul">$1</ul>')
    // 数字列表
    .replace(/^(\d+)\. (.+)$/gm, '<li class="md-oli">$2</li>')
    .replace(/((?:<li class="md-oli">.*<\/li>\n?)+)/g, '<ol class="md-ol">$1</ol>')
    // 换行
    .replace(/\n/g, '<br>')
}

// ===== 工具：时间 =====
function formatTime(ts) {
  const d = new Date(ts)
  const pad = (n) => String(n).padStart(2, '0')
  return `${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}

// ===== 工具：格式化 JSON =====
function formatJSON(obj) {
  try {
    return JSON.stringify(obj, null, 2)
  } catch {
    return String(obj)
  }
}

// ===== 滚动：保证最新内容一定可见 =====
// 关键：用户如果手动往上滚看历史，则不要强制拉回；
// 但当 (a) 已经在底部 或 (b) 流式进行中 时，要自动跟到底。
function isNearBottom(el) {
  if (!el) return true
  return el.scrollHeight - el.scrollTop - el.clientHeight < 80
}

let pendingScroll = false
function scheduleScroll(force = false) {
  if (pendingScroll) return
  pendingScroll = true
  requestAnimationFrame(() => {
    pendingScroll = false
    const el = messagesRef.value
    if (!el) return
    if (force || isNearBottom(el)) {
      el.scrollTop = el.scrollHeight
    }
  })
}

// 监听内容变化（用 ResizeObserver 兜底，token 回调里也主动触发）
let resizeObserver = null
function setupScrollObserver() {
  if (!messagesRef.value || typeof ResizeObserver === 'undefined') return
  resizeObserver = new ResizeObserver(() => scheduleScroll())
  resizeObserver.observe(messagesRef.value)
}

// ===== 发送 / 接收 =====
async function sendMessage() {
  const text = inputText.value.trim()
  if (!text || streaming.value) return

  // 1) 用户消息入列
  const userMsg = { id: nextId++, role: 'user', content: text, ts: Date.now() }
  messages.value.push(userMsg)
  inputText.value = ''
  // 强制滚到底（用户消息必须可见）
  nextTick(() => {
    const el = messagesRef.value
    if (el) el.scrollTop = el.scrollHeight
  })

  // 2) 流式调用
  streaming.value = true
  currentAnswer.value = ''
  currentToolCalls.value = []  // 重置 tool_calls 列表
  let fullAnswer = ''
  const toolsUsed = []
  abortController.value = new AbortController()

  try {
    await aiAPI.askStream(
      { query: text, conversation_id: conversationId.value },
      (event) => {
        if (abortController.value?.signal.aborted) return
        if (event.type === 'start' || event.type === 'done') {
          if (event.conversation_id) conversationId.value = event.conversation_id
        }
        if (event.type === 'token') {
          currentAnswer.value += event.content
          fullAnswer += event.content
          scheduleScroll()  // 持续滚到底
        } else if (event.type === 'tool_call') {
          if (!toolsUsed.includes(event.name)) toolsUsed.push(event.name)
          // 记录本次调用（参数 + 待补 result）
          currentToolCalls.value.push({
            name: event.name,
            arguments: event.arguments || {},
            result: null,  // 等 tool_result 事件来补
          })
          scheduleScroll(true)
        } else if (event.type === 'tool_result') {
          // 补全上一个同名 tool_call 的 result
          for (let i = currentToolCalls.value.length - 1; i >= 0; i--) {
            if (currentToolCalls.value[i].name === event.name && !currentToolCalls.value[i].result) {
              currentToolCalls.value[i].result = event.result
              break
            }
          }
        } else if (event.type === 'done') {
          // 流式期间的内容已经全部进 currentAnswer（fullAnswer），
          // 渲染气泡由下面 push 触发；push 后 nextTick 强制滚到底
          const finalContent = fullAnswer || event.answer || ''
          messages.value.push({
            id: nextId++,
            role: 'assistant',
            content: finalContent,
            tools: toolsUsed,
            toolCalls: [...currentToolCalls.value],  // 快照
            ts: Date.now(),
          })
          currentAnswer.value = ''
          currentToolCalls.value = []  // 清空
          // 等 DOM 更新完再滚（push 和 currentAnswer 清空都触发 Vue 渲染）
          nextTick(() => {
            const el = messagesRef.value
            if (el) el.scrollTop = el.scrollHeight
          })
        } else if (event.type === 'error') {
          ElMessage.error(`AI 错误: ${event.message}`)
          messages.value.push({
            id: nextId++,
            role: 'assistant',
            content: `⚠️ ${event.message}`,
            tools: [],
            ts: Date.now(),
          })
          scheduleScroll(true)
        }
      },
      { signal: abortController.value.signal },
    )
  } catch (e) {
    if (e?.name === 'CanceledError' || abortController.value?.signal.aborted) {
      // 用户主动停止：把已收的内容保留为一条消息
      if (fullAnswer) {
        messages.value.push({
          id: nextId++,
          role: 'assistant',
          content: fullAnswer + '\n\n_（已停止生成）_',
          tools: toolsUsed,
          ts: Date.now(),
        })
      }
    } else {
      ElMessage.error(`请求失败: ${e?.message || e}`)
      messages.value.push({
        id: nextId++,
        role: 'assistant',
        content: `⚠️ 网络错误: ${e?.message || e}`,
        tools: [],
        ts: Date.now(),
      })
    }
  } finally {
    streaming.value = false
    currentAnswer.value = ''
    currentToolCalls.value = []
    abortController.value = null
    scheduleScroll(true)
  }
}

function stopGeneration() {
  if (abortController.value) {
    abortController.value.abort()
    ElMessage.info('已停止生成')
  }
}

function newConversation() {
  if (streaming.value) {
    ElMessage.warning('请先停止当前生成')
    return
  }
  messages.value = []
  conversationId.value = null
  currentAnswer.value = ''
  currentToolCalls.value = []
  ElMessage.success('已开始新对话')
}

function askSuggestion(s) {
  if (streaming.value) return
  inputText.value = s.text
  sendMessage()
}

function onKeydown(e) {
  // Enter 发送；Shift+Enter 换行（textarea 默认行为）
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

// 流式回答变化时触发防抖渲染 + 自动滚动
watch(currentAnswer, (newVal) => {
  scheduleRender(newVal)  // 防抖：100ms 才 render 一次
  scheduleScroll()        // 持续滚到底
})

// 流结束时立即 render 一次（避免最后几十个字符被 debounce 卡掉）
watch(streaming, (isStreaming, wasStreaming) => {
  if (wasStreaming && !isStreaming) {
    if (_renderTimer) clearTimeout(_renderTimer)
    renderedCurrentAnswer.value = renderMarkdownImmediate(currentAnswer.value)
  }
})

onMounted(async () => {
  await nextTick()
  setupScrollObserver()
  // 拉工具数（可选，不阻塞 UI）
  try {
    const r = await aiAPI.health?.()
    if (r?.tools) toolCount.value = r.tools
  } catch { /* ignore */ }
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  if (abortController.value) abortController.value.abort()
})
</script>

<style scoped>
/* ===== 整体布局 ===== */
.ai-chat-page {
  display: flex;
  flex-direction: column;
  height: 100dvh;  /* 直接视口高度，不被父级 flex 撑开 */
  background: linear-gradient(180deg, #f9fafb 0%, #f3f4f6 100%);
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
  z-index: 2;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, #4F46E5, #7C3AED);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  box-shadow: 0 2px 8px rgba(79, 70, 229, 0.25);
}

.brand-text h1 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: #111827;
  line-height: 1.2;
}

.brand-sub {
  font-size: 12px;
  color: #6b7280;
}

.top-actions {
  display: flex;
  gap: 8px;
}

/* ===== 聊天主区 ===== */
.chat-shell {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;  /* 关键：让内部 flex 正确收缩 */
  max-width: 960px;
  width: 100%;
  margin: 0 auto;
  padding: 0 24px;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px 0 16px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  scroll-behavior: smooth;
  /* 自定义滚动条 */
  scrollbar-width: thin;
  scrollbar-color: #d1d5db transparent;
}

.messages::-webkit-scrollbar { width: 6px; }
.messages::-webkit-scrollbar-track { background: transparent; }
.messages::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}
.messages::-webkit-scrollbar-thumb:hover { background: #9ca3af; }

/* ===== 欢迎页 ===== */
.welcome {
  margin: auto;
  text-align: center;
  padding: 40px 20px;
  max-width: 600px;
}

.welcome-icon { font-size: 56px; margin-bottom: 12px; }
.welcome h2 { font-size: 22px; color: #111827; margin: 0 0 8px; }
.welcome p { color: #6b7280; margin: 0 0 24px; }

.suggestions {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 10px;
  margin-top: 8px;
}

.suggestion-chip {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 12px 14px;
  text-align: left;
  cursor: pointer;
  transition: all 0.15s;
  display: flex;
  align-items: center;
  gap: 10px;
}
.suggestion-chip:hover {
  border-color: #4F46E5;
  background: #f5f3ff;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.08);
}
.chip-icon { font-size: 18px; }
.chip-text { font-size: 13px; color: #374151; line-height: 1.4; }

/* ===== 消息 ===== */
.message {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  animation: msg-in 0.2s ease-out;
}

@keyframes msg-in {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

.message-user { flex-direction: row-reverse; }

.avatar { flex-shrink: 0; }

.bubble-wrap {
  max-width: calc(100% - 56px);
  display: flex;
  flex-direction: column;
  min-width: 0;  /* 关键：让 flex 子项能收缩到内容宽度 */
}

.message-user .bubble-wrap { align-items: flex-end; }
.message-user .bubble { text-align: left; }  /* 气泡内文字仍左对齐，符合中文习惯 */

.bubble {
  padding: 10px 14px;
  border-radius: 14px;
  line-height: 1.6;
  font-size: 14px;
  word-wrap: break-word;
  position: relative;
  max-width: 100%;
  width: fit-content;  /* 气泡宽度跟随内容，不撑满 */
}

.bubble-assistant {
  background: white;
  color: #1f2937;
  border-top-left-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  border-left: 3px solid #4F46E5;
}

.bubble-user {
  background: linear-gradient(135deg, #0D9488, #14B8A6);
  color: white;
  border-top-right-radius: 4px;
  box-shadow: 0 2px 8px rgba(13, 148, 136, 0.18);
}

.bubble-content :deep(strong) { font-weight: 600; }
.bubble-content :deep(em) { font-style: italic; color: inherit; }
.bubble-content :deep(.md-h) {
  margin: 8px 0 4px;
  font-weight: 600;
  color: #111827;
}
.bubble-content :deep(h2.md-h) { font-size: 18px; }
.bubble-content :deep(h3.md-h) { font-size: 16px; }
.bubble-content :deep(h4.md-h) { font-size: 14px; }
.bubble-content :deep(.md-ul),
.bubble-content :deep(.md-ol) {
  margin: 4px 0;
  padding-left: 22px;
}
.bubble-content :deep(.md-li),
.bubble-content :deep(.md-oli) { margin: 2px 0; }
.bubble-content :deep(.md-code) {
  background: #1f2937;
  color: #e5e7eb;
  padding: 10px 12px;
  border-radius: 8px;
  overflow-x: auto;
  font-family: 'SF Mono', Menlo, Consolas, monospace;
  font-size: 13px;
  line-height: 1.5;
  margin: 8px 0;
}
.bubble-content :deep(.md-inline-code) {
  background: rgba(79, 70, 229, 0.1);
  color: #4F46E5;
  padding: 1px 6px;
  border-radius: 4px;
  font-family: 'SF Mono', Menlo, Consolas, monospace;
  font-size: 13px;
}
.bubble-user :deep(.md-inline-code) {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}
.bubble-content :deep(pre) { white-space: pre-wrap; }

.thinking { color: #9ca3af; font-style: italic; }
.dots { display: inline-block; }
.dots::after {
  content: '';
  animation: dots 1.4s steps(4) infinite;
}
@keyframes dots {
  0%   { content: ''; }
  25%  { content: '.'; }
  50%  { content: '..'; }
  75%  { content: '...'; }
}

.cursor {
  display: inline-block;
  margin-left: 2px;
  color: #4F46E5;
  animation: blink 1s step-end infinite;
}
@keyframes blink { 50% { opacity: 0; } }

.tools-row {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-top: 6px;
  padding: 0 4px;
}

/* ===== 工具调用折叠卡片 ===== */
.tool-calls {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tool-call-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  overflow: hidden;
  transition: border-color 0.15s;
}
.tool-call-card:hover {
  border-color: #cbd5e1;
}
.tool-call-card[open] {
  background: #fff;
}

.tool-call-card > summary {
  padding: 6px 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  user-select: none;
  list-style: none;  /* 去掉默认三角 */
}
.tool-call-card > summary::-webkit-details-marker { display: none; }
.tool-call-card > summary::before {
  content: '▶';
  font-size: 10px;
  color: #94a3b8;
  transition: transform 0.15s;
}
.tool-call-card[open] > summary::before {
  transform: rotate(90deg);
}

.tool-icon { font-size: 14px; }
.tool-name {
  font-family: 'SF Mono', Consolas, Monaco, monospace;
  font-size: 12px;
  font-weight: 500;
  color: #475569;
}
.tool-status {
  margin-left: auto;
  font-size: 12px;
  font-weight: 600;
}
.tool-status.ok { color: #10b981; }
.tool-status.pending { color: #f59e0b; }

.tool-detail {
  padding: 8px 12px 10px;
  border-top: 1px solid #f1f5f9;
  background: #fafbfc;
}
.tool-section { margin-top: 6px; }
.tool-section:first-child { margin-top: 0; }
.tool-label {
  font-size: 11px;
  color: #94a3b8;
  margin-bottom: 2px;
  font-weight: 500;
}
.tool-pre {
  font-family: 'SF Mono', Consolas, Monaco, monospace;
  font-size: 12px;
  color: #334155;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 200px;
  overflow-y: auto;
}

/* ===== Think 块（AI 推理过程）===== */
.think-block {
  margin-bottom: 12px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-left: 3px solid #f59e0b;
  border-radius: 6px;
  font-size: 12px;
  overflow: hidden;
}
.think-block > summary {
  padding: 6px 10px;
  cursor: pointer;
  color: #92400e;
  font-weight: 500;
  user-select: none;
  list-style: none;
}
.think-block > summary::-webkit-details-marker { display: none; }
.think-block > summary::before {
  content: '💭 ';
  margin-right: 2px;
}
.think-pre {
  margin: 0;
  padding: 8px 12px 10px;
  background: rgba(255, 255, 255, 0.5);
  color: #78350f;
  font-family: 'SF Mono', Consolas, Monaco, monospace;
  font-size: 11px;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 240px;
  overflow-y: auto;
}

.ts {
  font-size: 11px;
  color: #9ca3af;
  margin-top: 4px;
  padding: 0 4px;
}

/* ===== 输入区 ===== */
.composer {
  padding: 12px 0 20px;
  background: linear-gradient(180deg, transparent 0%, #f9fafb 30%);
}

.composer-inner {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 8px 8px 8px 14px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
  transition: border-color 0.15s, box-shadow 0.15s;
}
.composer-inner:focus-within {
  border-color: #4F46E5;
  box-shadow: 0 4px 16px rgba(79, 70, 229, 0.12);
}

.composer-input :deep(.el-textarea__inner) {
  border: none !important;
  box-shadow: none !important;
  padding: 8px 0;
  background: transparent;
  resize: none;
  font-size: 14px;
  line-height: 1.5;
}

.send-btn {
  flex-shrink: 0;
  height: 40px;
  width: 40px;
  background: linear-gradient(135deg, #4F46E5, #7C3AED);
  border: none;
}
.send-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #4338CA, #6D28D9);
}
.send-btn:disabled {
  background: #e5e7eb;
  color: #9ca3af;
}

.composer-foot {
  text-align: center;
  margin-top: 6px;
  font-size: 11px;
  color: #9ca3af;
}
</style>
