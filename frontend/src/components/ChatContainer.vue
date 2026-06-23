<template>
  <div class="chat-container">
    <!-- 头部标题 -->
    <div class="chat-container__header">
      <span class="chat-container__title">{{ title }}</span>
      <span v-if="subtitle" class="chat-container__subtitle">{{ subtitle }}</span>
    </div>

    <!-- 消息滚动区 -->
    <div ref="messageArea" class="chat-container__messages">
      <EmptyHolder
        v-if="chatList.length === 0"
        text="暂无对话记录"
      />
      <div
        v-for="item in chatList"
        :key="item.id"
        class="chat-container__bubble-row"
        :class="item.role === 'user' ? 'chat-container__bubble-row--right' : 'chat-container__bubble-row--left'"
      >
        <div
          class="chat-container__bubble"
          :class="item.role === 'user' ? 'chat-container__bubble--user' : 'chat-container__bubble--ai'"
        >
          <span class="chat-container__bubble-text">{{ item.content }}</span>
          <span class="chat-container__bubble-time">{{ item.time }}</span>
        </div>
      </div>
    </div>

    <!-- 底部输入栏 -->
    <div class="chat-container__input-bar">
      <el-button class="chat-container__attach-btn" text>
        <el-icon :size="20"><Paperclip /></el-icon>
      </el-button>
      <el-input
        v-model="inputText"
        class="chat-container__input"
        placeholder="请输入您的问题..."
        @keyup.enter="handleSend"
      />
      <el-button
        type="primary"
        :disabled="!inputText.trim()"
        @click="handleSend"
      >
        发送
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { Paperclip } from '@element-plus/icons-vue'
import type { ChatItem } from '@/types/chat'
import EmptyHolder from './EmptyHolder.vue'

interface Props {
  title?: string
  subtitle?: string
  chatList?: ChatItem[]
}

const props = withDefaults(defineProps<Props>(), {
  title: 'AI 财务助手',
  subtitle: '',
  chatList: () => [],
})

const emit = defineEmits<{
  (e: 'send', content: string): void
}>()

const inputText = ref('')
const messageArea = ref<HTMLElement | null>(null)

function handleSend() {
  const text = inputText.value.trim()
  if (!text) return
  emit('send', text)
  inputText.value = ''
}

watch(
  () => props.chatList.length,
  async () => {
    await nextTick()
    if (messageArea.value) {
      messageArea.value.scrollTop = messageArea.value.scrollHeight
    }
  },
)
</script>

<style scoped>
.chat-container {
  background: var(--bg-card);
  border-radius: var(--border-radius-base);
  border: 1px solid var(--border-normal);
  box-shadow: var(--box-shadow-base);
  display: flex;
  flex-direction: column;
  height: 560px;
  overflow: hidden;
}

/* === 头部标题 === */
.chat-container__header {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 16px var(--page-padding);
  border-bottom: 1px solid var(--border-normal);
}

.chat-container__title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-title);
}

.chat-container__subtitle {
  font-size: 13px;
  color: var(--text-placeholder);
}

/* === 消息滚动区 === */
.chat-container__messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px var(--page-padding);
}

.chat-container__bubble-row {
  display: flex;
  margin-bottom: 16px;
}

.chat-container__bubble-row--left {
  justify-content: flex-start;
}

.chat-container__bubble-row--right {
  justify-content: flex-end;
}

.chat-container__bubble {
  max-width: 70%;
  padding: 10px 14px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.chat-container__bubble--ai {
  background: var(--bg-page);
  border-bottom-left-radius: 4px;
}

.chat-container__bubble--user {
  background: var(--color-primary);
  border-bottom-right-radius: 4px;
}

.chat-container__bubble--user .chat-container__bubble-text {
  color: #ffffff;
}

.chat-container__bubble--user .chat-container__bubble-time {
  color: rgba(255, 255, 255, 0.7);
}

.chat-container__bubble-text {
  font-size: 14px;
  color: var(--text-body);
  line-height: 1.6;
  white-space: pre-wrap;
}

.chat-container__bubble-time {
  font-size: 11px;
  color: var(--text-placeholder);
  align-self: flex-end;
}

/* === 底部输入栏 === */
.chat-container__input-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px var(--page-padding);
  border-top: 1px solid var(--border-normal);
  background: var(--bg-card);
}

.chat-container__attach-btn {
  color: var(--text-placeholder);
}

.chat-container__input {
  flex: 1;
}
</style>