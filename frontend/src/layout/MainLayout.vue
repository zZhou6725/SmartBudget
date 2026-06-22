<template>
  <div class="main-layout">
    <SideBar />
    <HeaderBar />
    <AppMain />
  </div>
</template>

<script setup lang="ts">
import SideBar from './components/SideBar.vue'
import HeaderBar from './components/HeaderBar.vue'
import AppMain from './components/AppMain.vue'
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  background: var(--bg-page);
}
</style>