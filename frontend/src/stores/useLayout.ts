import { defineStore } from 'pinia'
import { ref } from 'vue'

const STORAGE_KEY = 'finbalance-sidebar-collapse'

export const useLayoutStore = defineStore('layout', () => {
  const saved = localStorage.getItem(STORAGE_KEY)
  const isSidebarCollapse = ref<boolean>(saved === 'true')

  function toggleSidebar() {
    isSidebarCollapse.value = !isSidebarCollapse.value
    localStorage.setItem(STORAGE_KEY, String(isSidebarCollapse.value))
  }

  return {
    isSidebarCollapse,
    toggleSidebar,
  }
})