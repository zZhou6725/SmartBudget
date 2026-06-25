<template>
  <div class="ai-assistant">
    <PageCard>
      <template #title>AI 财务助手</template>
      <template #extra>
        <span class="ai-assistant__subtitle">DeepSeek · 智能分析 · 票据识别</span>
      </template>

      <!-- 快捷提问 -->
      <div class="ai-assistant__prompts">
        <el-tag
          v-for="p in prompts"
          :key="p.id"
          class="ai-assistant__tag"
          @click="handlePrompt(p.text)"
        >
          {{ p.text }}
        </el-tag>
      </div>

      <!-- 对话区域 -->
      <ChatContainer
        :chat-list="displayList"
        :loading="streaming"
        @send="handleSend"
        @upload="handleUploadClick"
      >
        <template #bubble-content="{ item }">
          <!-- 思考过程 -->
          <div
            v-if="item.role === 'ai' && item.thinking"
            class="ai-assistant__thinking"
          >
            <div
              class="ai-assistant__thinking-header"
              @click="toggleThinking(item.id)"
            >
              <span>💭 思考过程</span>
              <span class="ai-assistant__thinking-arrow">{{ thinkingOpen[item.id] ? '▾' : '▸' }}</span>
            </div>
            <div v-show="thinkingOpen[item.id]" class="ai-assistant__thinking-body">
              {{ item.thinking }}
            </div>
          </div>
          <!-- AI 回复内容（预渲染 markdown） -->
          <div
            v-if="item.role === 'ai'"
            class="ai-assistant__content"
            v-html="item.renderedContent || renderMarkdown(item.content)"
          />
          <!-- 用户消息纯文本 -->
          <span v-else class="ai-assistant__user-text">{{ item.content }}</span>
        </template>
      </ChatContainer>

      <!-- 隐藏文件上传 -->
      <input
        ref="fileInput"
        type="file"
        accept=".txt,.csv,.json,image/*"
        hidden
        @change="handleFileChange"
      />

      <!-- 票据识别结果 Dialog -->
      <el-dialog v-model="receiptVisible" title="票据识别结果" width="420px">
        <el-descriptions v-if="receiptResult" :column="2" border size="small">
          <el-descriptions-item label="金额">
            {{ receiptResult.amount ? '¥' + receiptResult.amount.toLocaleString() : '--' }}
          </el-descriptions-item>
          <el-descriptions-item label="类型">
            {{ receiptResult.category || '--' }}
          </el-descriptions-item>
          <el-descriptions-item label="日期">
            {{ receiptResult.date || '--' }}
          </el-descriptions-item>
          <el-descriptions-item label="商户">
            {{ receiptResult.vendor || '--' }}
          </el-descriptions-item>
          <el-descriptions-item label="置信度" :span="2">
            <el-progress
              :percentage="Math.round((receiptResult.confidence || 0) * 100)"
              :color="(receiptResult.confidence || 0) > 0.7 ? 'var(--color-success)' : 'var(--color-warning)'"
              :stroke-width="8"
            />
          </el-descriptions-item>
        </el-descriptions>
        <EmptyHolder v-else text="未能识别票据信息" />
      </el-dialog>
    </PageCard>
  </div>
</template>

<script setup lang="ts">
import { ref, shallowRef, triggerRef, computed, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import PageCard from '@/components/PageCard.vue'
import ChatContainer from '@/components/ChatContainer.vue'
import EmptyHolder from '@/components/EmptyHolder.vue'
import type { QuickPrompt, ReceiptValidateResult } from '@/types/ai'
import type { ChatItem } from '@/types/chat'
import { getQuickPrompts, streamChat, receiptUpload } from '@/api/modules/ai'

const prompts = ref<QuickPrompt[]>([])
const chatList = shallowRef<ChatItem[]>([])
const displayList = computed(() => chatList.value)
const streaming = ref(false)
const thinkingOpen = reactive<Record<string, boolean>>({})
const fileInput = ref<HTMLInputElement | null>(null)

const receiptVisible = ref(false)
const receiptResult = ref<ReceiptValidateResult | null>(null)

let abortCtrl: AbortController | null = null

function fmtTime(): string {
  const now = new Date()
  return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`
}

function toggleThinking(id: string) {
  thinkingOpen[id] = !thinkingOpen[id]
}

/** 简单 markdown → HTML（内容来自 AI） */
function renderMarkdown(text: string): string {
  if (!text) return ''
  let html = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')

  html = html.replace(/```(\w*)\n([\s\S]*?)```/g,
    '<pre class="ai-assistant__code"><code>$2</code></pre>')
  html = html.replace(/`([^`]+)`/g, '<code class="ai-assistant__inline-code">$1</code>')
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  html = html.replace(/^### (.+)$/gm, '<h4 class="ai-assistant__h4">$1</h4>')
  html = html.replace(/^## (.+)$/gm, '<h3 class="ai-assistant__h3">$1</h3>')
  html = html.replace(/^# (.+)$/gm, '<h2 class="ai-assistant__h2">$1</h2>')
  html = html.replace(/^[*-] (.+)$/gm, '<li>$1</li>')
  html = html.replace(/((?:<li>.*<\/li>\n?)+)/g, '<ul class="ai-assistant__list">$1</ul>')
  html = html.replace(/\n\n/g, '<br/><br/>')
  html = html.replace(/\n/g, '<br/>')

  return html
}

async function handlePrompt(text: string) {
  await doChat(text)
}

async function handleSend(content: string) {
  await doChat(content)
}

async function doChat(message: string) {
  // 取消上一次未完成的请求
  if (abortCtrl) {
    abortCtrl.abort()
    abortCtrl = null
  }

  const userMsg: ChatItem = {
    id: `u${Date.now()}`,
    role: 'user',
    content: message,
    time: fmtTime(),
  }
  const aiMsg: ChatItem = {
    id: `a${Date.now()}`,
    role: 'ai',
    content: '',
    renderedContent: '',
    thinking: '',
    time: fmtTime(),
  }
  chatList.value = [...chatList.value, userMsg, aiMsg]
  streaming.value = true

  abortCtrl = new AbortController()
  const signal = abortCtrl.signal

  try {
    let content = ''
    let thinking = ''
    let lastUpdate = 0

    for await (const chunk of streamChat(message, signal)) {
      content += chunk.content
      thinking += chunk.thinking

      // 直接修改 shallowRef 内部对象，然后手动触发更新
      aiMsg.content = content
      aiMsg.thinking = thinking

      // 节流：最多 20 次/秒 UI 更新
      const now = Date.now()
      if (now - lastUpdate > 50) {
        aiMsg.renderedContent = renderMarkdown(content)
        triggerRef(chatList)
        lastUpdate = now
      }

      if (chunk.done) break
    }

    // 最后一次确保完整渲染
    aiMsg.renderedContent = renderMarkdown(content)
    triggerRef(chatList)
  } catch {
    if (signal.aborted) return // 用户主动取消，不提示
    chatList.value[chatList.value.length - 1].content = '网络连接失败，请稍后重试'
    chatList.value[chatList.value.length - 1].renderedContent = renderMarkdown('网络连接失败，请稍后重试')
    triggerRef(chatList)
  } finally {
    streaming.value = false
    abortCtrl = null
  }
}

function handleUploadClick() {
  fileInput.value?.click()
}

async function handleFileChange(e: Event) {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return
  target.value = ''

  ElMessage.info(`正在识别 ${file.name} ...`)
  try {
    const res = await receiptUpload(file)
    if (res.code === 0 && res.data) {
      receiptResult.value = res.data
      receiptVisible.value = true
    } else {
      ElMessage.warning(res.msg || '识别失败')
    }
  } catch {
    ElMessage.error('上传失败，请重试')
  }
}

onMounted(async () => {
  try {
    const res = await getQuickPrompts()
    if (res.code === 0 && res.data) prompts.value = res.data
  } catch { /* ignore */ }
})
</script>

<style scoped>
.ai-assistant__subtitle {
  font-size: 13px;
  color: var(--text-placeholder);
}

.ai-assistant__prompts {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.ai-assistant__tag {
  cursor: pointer;
  transition: var(--transition-base);
}

.ai-assistant__tag:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.ai-assistant__user-text {
  white-space: pre-wrap;
  word-break: break-word;
}

.ai-assistant__thinking {
  margin-bottom: 8px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid var(--border-normal);
}

.ai-assistant__thinking-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 10px;
  font-size: 12px;
  color: var(--text-placeholder);
  background: var(--bg-page);
  cursor: pointer;
  user-select: none;
}

.ai-assistant__thinking-header:hover {
  color: var(--text-body);
}

.ai-assistant__thinking-arrow {
  font-size: 14px;
}

.ai-assistant__thinking-body {
  padding: 8px 10px;
  font-size: 12px;
  color: var(--text-placeholder);
  background: #fafbfc;
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.5;
  border-top: 1px solid var(--border-normal);
}

.ai-assistant__content {
  font-size: 14px;
  line-height: 1.7;
  color: var(--text-body);
  word-break: break-word;
}

.ai-assistant__content :deep(.ai-assistant__code) {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 12px 14px;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 13px;
  line-height: 1.5;
  margin: 8px 0;
}

.ai-assistant__content :deep(.ai-assistant__inline-code) {
  background: var(--bg-page);
  color: var(--color-danger);
  padding: 1px 5px;
  border-radius: 3px;
  font-size: 13px;
  font-family: 'Consolas', 'Monaco', monospace;
}

.ai-assistant__content :deep(.ai-assistant__h2) {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-title);
  margin: 12px 0 6px;
}

.ai-assistant__content :deep(.ai-assistant__h3) {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-title);
  margin: 10px 0 4px;
}

.ai-assistant__content :deep(.ai-assistant__h4) {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-title);
  margin: 8px 0 4px;
}

.ai-assistant__content :deep(.ai-assistant__list) {
  padding-left: 20px;
  margin: 4px 0;
}

.ai-assistant__content :deep(.ai-assistant__list li) {
  margin: 2px 0;
}

.ai-assistant__content :deep(strong) {
  color: var(--text-title);
  font-weight: 600;
}
</style>