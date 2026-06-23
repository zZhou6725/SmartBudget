import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
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
      // 后续业务路由在此添加：
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
      // { path: 'ai-assistant', name: 'AIAssistant', component: ..., meta: { title: 'AI财务助手' } },
      // { path: 'dashboard', name: 'Dashboard', component: ..., meta: { title: '数据看板' } },
      // { path: 'message', name: 'Message', component: ..., meta: { title: '消息预警' } },
      // { path: 'organization', name: 'Organization', component: ..., meta: { title: '组织权限' } },
      // { path: 'personal', name: 'Personal', component: ..., meta: { title: '个人中心' } },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router