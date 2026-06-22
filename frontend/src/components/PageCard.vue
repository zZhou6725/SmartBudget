<template>
  <div class="page-card">
    <div v-if="$slots.title || $slots.extra" class="page-card__header">
      <div class="page-card__title">
        <slot name="title" />
      </div>
      <div class="page-card__extra">
        <slot name="extra" />
      </div>
    </div>
    <div class="page-card__body">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
// 通用卡片容器，所有业务页面统一复用
</script>

<style scoped>
.page-card {
  background: var(--bg-card);
  border-radius: var(--border-radius-base);
  border: 1px solid var(--border-normal);
  box-shadow: var(--box-shadow-base);
  overflow: hidden;
}

.page-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px var(--page-padding);
  border-bottom: 1px solid var(--border-normal);
}

.page-card__title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-title);
}

.page-card__body {
  padding: var(--page-padding);
}
</style>
