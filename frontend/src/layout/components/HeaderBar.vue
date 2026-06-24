<template>
  <header class="header" :style="{ paddingLeft: sidebarWidth }">
    <!-- 左侧自适应占位 -->
    <div class="header__left" />

    <!-- 右侧操作区 -->
    <div class="header__right">
      <!-- 消息入口 -->
      <el-badge :value="unreadCount" :hidden="unreadCount === 0" :max="99">
        <el-button class="header__btn" text>
          <el-icon :size="20"><Bell /></el-icon>
        </el-button>
      </el-badge>

      <!-- 用户下拉菜单 -->
      <el-dropdown trigger="click" @command="handleCommand">
        <div class="header__user">
          <el-avatar :size="32" :src="userAvatar || undefined">
            <el-icon :size="18"><UserFilled /></el-icon>
          </el-avatar>
          <span class="header__username">{{ userName || '未登录' }}</span>
          <el-icon :size="14"><ArrowDown /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="personal">个人中心</el-dropdown-item>
            <el-dropdown-item command="password">修改密码</el-dropdown-item>
            <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { Bell, UserFilled, ArrowDown } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { useLayoutStore } from '@/stores/useLayout'

const router = useRouter()
const layoutStore = useLayoutStore()

const sidebarWidth = computed(() =>
  layoutStore.isSidebarCollapse
    ? 'var(--sidebar-width-collapse)'
    : 'var(--sidebar-width-expand)'
)

interface UserInfo { username: string; real_name: string; avatar: string }
const userInfo = ref<UserInfo | null>(null)
const userName = computed(() => userInfo.value?.real_name || userInfo.value?.username || '')
const userAvatar = computed(() => userInfo.value?.avatar || '')

onMounted(() => {
  const raw = localStorage.getItem('finbalance-user')
  if (raw) {
    try { userInfo.value = JSON.parse(raw) } catch {}
  }
})

const unreadCount = ref(0)

function handleCommand(command: string) {
  if (command === 'personal') router.push('/personal')
  if (command === 'logout') {
    localStorage.removeItem('finbalance-token')
    localStorage.removeItem('finbalance-user')
    router.push('/login')
  }
}
</script>

<style scoped>
.header {
  position: fixed;
  top: 0;
  right: 0;
  height: var(--header-height);
  background: var(--bg-card);
  border-bottom: 1px solid var(--border-normal);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--page-padding);
  transition: var(--transition-base);
  z-index: 99;
}

.header__left {
  flex: 1;
}

.header__right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header__btn {
  color: var(--text-body);
  transition: var(--transition-base);
}

.header__btn:hover {
  color: var(--color-primary);
}

.header__user {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: var(--border-radius-base);
  transition: var(--transition-base);
}

.header__user:hover {
  background: var(--bg-page);
}

.header__username {
  font-size: 13px;
  color: var(--text-body);
  white-space: nowrap;
}
</style>