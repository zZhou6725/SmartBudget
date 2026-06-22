<template>
  <div class="empty-holder">
    <el-icon :size="48" class="empty-holder__icon">
      <Document />
    </el-icon>
    <span class="empty-holder__text">{{ text }}</span>
  </div>
</template>

<script setup lang="ts">
import { Document } from '@element-plus/icons-vue'

interface Props {
  text?: string
}

withDefaults(defineProps<Props>(), {
  text: '暂无数据',
})
</script>

<style scoped>
.empty-holder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 24px;
}

.empty-holder__icon {
  color: var(--text-placeholder);
  margin-bottom: 12px;
}

.empty-holder__text {
  font-size: 14px;
  color: var(--text-placeholder);
}
</style>
