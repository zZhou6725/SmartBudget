<template>
  <div class="ai-assistant">
    <PageCard>
      <template #title>AI 财务助手</template>
      <template #extra>
        <span class="ai-assistant__subtitle">智能财务分析 · 票据校验</span>
      </template>

      <!-- 快捷提问 -->
      <div class="ai-assistant__prompts">
        <el-tag
          v-for="p in prompts"
          :key="p.id"
          class="ai-assistant__tag"
          type="info"
          @click="handlePrompt(p.text)"
        >
          {{ p.text }}
        </el-tag>
      </div>

      <!-- 对话区域 -->
      <ChatContainer
        :title="''"
        subtitle=""
        :chat-list="chatList"
        @send="handleSend"
      />
    </PageCard>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import PageCard from '@/components/PageCard.vue'
import ChatContainer from '@/components/ChatContainer.vue'
import type { QuickPrompt, ChatItem } from '@/types/chat'

/** 快捷提问列表（空绑定，后续从API获取） */
const prompts = ref<QuickPrompt[]>([])

/** 对话列表 */
const chatList = ref<ChatItem[]>([])

function handlePrompt(text: string) {
  // TODO: 填入输入框并发起提问
}

function handleSend(content: string) {
  // TODO: 调用 aiChat API，追加消息到 chatList
}
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
</style>