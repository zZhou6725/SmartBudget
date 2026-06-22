<template>
  <aside
    class="sidebar"
    :class="{ collapsed: isSidebarCollapse }"
    :style="{ width: sidebarWidth }"
  >
    <!-- 顶部 Logo 区域 -->
    <div class="sidebar__brand">
      <div class="sidebar__logo">
        <el-icon :size="24">
          <component :is="logoIcon" />
        </el-icon>
        <span v-show="!isSidebarCollapse" class="sidebar__title">FinBalance 财衡中台</span>
      </div>
    </div>

    <!-- 折叠切换按钮 -->
    <div class="sidebar__toggle" @click="layoutStore.toggleSidebar()">
      <el-icon :size="16">
        <DArrowLeft v-if="!isSidebarCollapse" />
        <DArrowRight v-else />
      </el-icon>
    </div>

    <!-- 导航菜单区域 -->
    <div class="sidebar__menu-wrap">
      <div
        v-if="menuList.length === 0"
        class="sidebar__menu-empty"
      >
        菜单加载中
      </div>
      <el-menu
        v-else
        :default-active="activeRoute"
        :collapse="isSidebarCollapse"
        :collapse-transition="false"
        router
        class="sidebar__menu"
        text-color="var(--text-body)"
        active-text-color="var(--color-primary)"
        background-color="transparent"
      >
        <template
          v-for="item in menuList"
          :key="item.id"
        >
          <el-tooltip
            v-if="isSidebarCollapse"
            :content="item.title"
            placement="right"
            effect="light"
          >
            <el-menu-item :index="item.path">
              <el-icon :size="20">
                <component :is="item.icon" />
              </el-icon>
              <span>{{ item.title }}</span>
            </el-menu-item>
          </el-tooltip>
          <el-menu-item
            v-else
            :index="item.path"
          >
            <el-icon :size="20">
              <component :is="item.icon" />
            </el-icon>
            <span>{{ item.title }}</span>
          </el-menu-item>
        </template>
      </el-menu>
    </div>

    <!-- 底部用户区域 -->
    <div class="sidebar__user">
      <div class="sidebar__divider" />
      <div class="sidebar__user-info">
        <el-avatar
          :size="36"
          :src="userAvatar || undefined"
        >
          <el-icon :size="20"><UserFilled /></el-icon>
        </el-avatar>
        <div v-show="!isSidebarCollapse" class="sidebar__user-text">
          <span class="sidebar__user-name">{{ userName || '未登录' }}</span>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { DArrowLeft, DArrowRight, UserFilled, Setting } from '@element-plus/icons-vue'
import { useLayoutStore } from '@/stores/useLayout'
import type { MenuItem } from '@/types/menu'

const route = useRoute()
const layoutStore = useLayoutStore()

const isSidebarCollapse = computed(() => layoutStore.isSidebarCollapse)
const sidebarWidth = computed(() =>
  isSidebarCollapse.value ? 'var(--sidebar-width-collapse)' : 'var(--sidebar-width-expand)'
)

const activeRoute = computed(() => route.path)

/** 菜单列表 — 后续从路由配置注入，禁止硬编码 */
const menuList = ref<MenuItem[]>([])

/** 预留：用户信息绑定 */
const userName = ref('')
const userAvatar = ref('')

/** Logo图标，后续替换为实际品牌图标 */
const logoIcon = Setting
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  background: var(--bg-card);
  border-right: 1px solid var(--border-normal);
  transition: var(--transition-base);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  z-index: 100;
}

/* === 顶部品牌区 === */
.sidebar__brand {
  padding: 16px 20px;
  min-height: 56px;
  display: flex;
  align-items: center;
}

.sidebar__logo {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--color-primary);
  white-space: nowrap;
  overflow: hidden;
}

.sidebar__title {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-title);
}

/* === 折叠切换按钮 === */
.sidebar__toggle {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px 0;
  cursor: pointer;
  color: var(--text-placeholder);
  transition: var(--transition-base);
  border-bottom: 1px solid var(--border-normal);
}

.sidebar__toggle:hover {
  color: var(--color-primary);
  background: var(--color-primary-light);
}

/* === 菜单区域 === */
.sidebar__menu-wrap {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 8px 0;
}

.sidebar__menu-empty {
  padding: 40px 16px;
  text-align: center;
  color: var(--text-placeholder);
  font-size: 13px;
}

.sidebar__menu {
  border-right: none !important;
}

.sidebar__menu :deep(.el-menu-item) {
  margin: 2px 8px;
  border-radius: var(--border-radius-base);
  height: 44px;
  line-height: 44px;
  border-left: 3px solid transparent;
}

.sidebar__menu :deep(.el-menu-item:hover) {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.sidebar__menu :deep(.el-menu-item.is-active) {
  background: var(--color-primary-light);
  color: var(--color-primary);
  border-left-color: var(--color-primary);
}

/* === 底部分割线 + 用户区 === */
.sidebar__user {
  padding: 12px 16px;
}

.sidebar__divider {
  height: 1px;
  background: var(--border-normal);
  margin-bottom: 12px;
}

.sidebar__user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  overflow: hidden;
  white-space: nowrap;
}

.sidebar__user-name {
  font-size: 13px;
  color: var(--text-body);
}

/* === 折叠状态微调 === */
.sidebar.collapsed .sidebar__brand {
  justify-content: center;
  padding: 16px 0;
}

.sidebar.collapsed .sidebar__user-info {
  justify-content: center;
}
</style>
