<template>
  <div class="stat-card">
    <EmptyHolder v-if="isValueEmpty" text="暂无数据" />
    <template v-else>
      <span class="stat-card__title">{{ title }}</span>
      <span class="stat-card__value">{{ formattedValue }}</span>
      <span v-if="subtitle" class="stat-card__subtitle">{{ subtitle }}</span>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import EmptyHolder from './EmptyHolder.vue'

interface Props {
  title: string
  value: number | string | null
  subtitle?: string
}

const props = defineProps<Props>()

const isValueEmpty = computed(() => props.value === null || props.value === undefined)

const formattedValue = computed(() => {
  if (typeof props.value === 'number') {
    return props.value.toLocaleString()
  }
  return props.value ?? ''
})
</script>

<style scoped>
.stat-card {
  background: var(--bg-card);
  border-radius: var(--border-radius-base);
  border: 1px solid var(--border-normal);
  box-shadow: var(--box-shadow-base);
  padding: 20px var(--page-padding);
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.stat-card__title {
  font-size: 13px;
  color: var(--text-placeholder);
}

.stat-card__value {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-title);
}

.stat-card__subtitle {
  font-size: 12px;
  color: var(--text-placeholder);
}
</style>
