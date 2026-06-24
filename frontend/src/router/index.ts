import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { title: '登录' },
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/layout/MainLayout.vue'),
    redirect: '/workbench',
    children: [
      {
        path: 'workbench',
        name: 'Workbench',
        component: () => import('@/views/workbench/index.vue'),
        meta: { title: '工作台首页' },
      },
      {
        path: 'expense',
        name: 'Expense',
        component: () => import('@/views/expense/index.vue'),
        meta: { title: '费用报销' },
      },
      {
        path: 'budget',
        name: 'Budget',
        component: () => import('@/views/budget/index.vue'),
        meta: { title: '预算管理' },
      },
      {
        path: 'ai-assistant',
        name: 'AIAssistant',
        component: () => import('@/views/ai-assistant/index.vue'),
        meta: { title: 'AI财务助手' },
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '数据看板' },
      },
      {
        path: 'message',
        name: 'Message',
        component: () => import('@/views/message/index.vue'),
        meta: { title: '消息预警中心' },
      },
      {
        path: 'organization',
        name: 'Organization',
        component: () => import('@/views/organization/index.vue'),
        meta: { title: '组织权限管理' },
      },
      {
        path: 'personal',
        name: 'Personal',
        component: () => import('@/views/personal/index.vue'),
        meta: { title: '个人中心' },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to, from) => {
  const token = localStorage.getItem('finbalance-token')
  const isLoggedIn = !!token
  if (to.path !== '/login' && !isLoggedIn) {
    return '/login'
  }
})

export default router