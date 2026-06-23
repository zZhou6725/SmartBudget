<template>
  <main class="app-main" :style="{ marginLeft: sidebarWidth }">
    <router-view />
  </main>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useLayoutStore } from '@/stores/useLayout'

const layoutStore = useLayoutStore()

const sidebarWidth = computed(() =>
  layoutStore.isSidebarCollapse
    ? 'var(--sidebar-width-collapse)'
    : 'var(--sidebar-width-expand)'
)
</script>

<style scoped>
.app-main {
  min-height: 100vh;
  padding: var(--page-padding);
  padding-top: calc(var(--header-height) + var(--page-padding));
  background: var(--bg-page);
  transition: var(--transition-base);
}
</style>