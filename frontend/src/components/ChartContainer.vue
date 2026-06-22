<template>
  <PageCard>
    <template v-if="title" #title>
      {{ title }}
    </template>
    <div v-if="empty" class="chart-container__empty">
      <EmptyHolder text="暂无图表数据" />
    </div>
    <div v-else class="chart-container__area">
      <slot />
    </div>
  </PageCard>
</template>

<script setup lang="ts">
import PageCard from './PageCard.vue'
import EmptyHolder from './EmptyHolder.vue'

interface Props {
  title?: string
  empty?: boolean
}

withDefaults(defineProps<Props>(), {
  title: '',
  empty: false,
})
</script>

<style scoped>
.chart-container__empty {
  min-height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-container__area {
  min-height: 280px;
}
</style>