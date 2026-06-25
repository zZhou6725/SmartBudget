<template>
  <div class="stat-card" :style="{ borderTopColor: accentColor }">
    <EmptyHolder v-if="isValueEmpty" text="暂无数据" />
    <template v-else>
      <div class="stat-card__header">
        <span class="stat-card__icon-dot" :style="{ background: accentColor }" />
        <span class="stat-card__title">{{ title }}</span>
      </div>
      <span class="stat-card__value" :style="{ color: accentColor }">{{ formattedValue }}</span>
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
  prefix?: string
  suffix?: string
  color?: string
}

const props = withDefaults(defineProps<Props>(), {
  color: 'var(--color-primary)',
})

const accentColor = computed(() => props.color)

const isValueEmpty = computed(() => props.value === null || props.value === undefined)

const formattedValue = computed(() => {
  if (props.value === null || props.value === undefined) return ''
  const prefix = props.prefix || ''
  const suffix = props.suffix || ''
  if (typeof props.value === 'number') {
    return `${prefix}${props.value.toLocaleString()}${suffix}`
  }
  return `${prefix}${props.value}${suffix}`
})
</script>

<style scoped>
.stat-card {
  background: var(--bg-card);
  border-radius: var(--border-radius-base);
  border: 1px solid var(--border-normal);
  border-top: 3px solid var(--color-primary);
  box-shadow: var(--box-shadow-base);
  padding: 20px var(--page-padding);
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.stat-card__header {
  display: flex;
  align-items: center;
  gap: 6px;
}

.stat-card__icon-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.stat-card__title {
  font-size: 13px;
  color: var(--text-placeholder);
}

.stat-card__value {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.stat-card__subtitle {
  font-size: 12px;
  color: var(--text-placeholder);
}
</style>