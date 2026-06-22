# FinBalance 财衡中台 — 前端

## 技术栈

Vue3 + TypeScript + Vite + Element Plus + Pinia + Vue Router + SCSS

## 目录结构

```
frontend/
├── public/             # 静态资源
├── src/
│   ├── assets/         # 样式 & 图片
│   │   ├── css/global.css   # 全局 Design Token
│   │   └── images/
│   ├── api/            # 接口请求（模块化）
│   ├── components/     # 全局公共组件
│   ├── layout/         # 布局组件
│   │   ├── MainLayout.vue
│   │   └── components/
│   ├── router/         # 路由配置
│   ├── stores/         # Pinia 状态管理
│   ├── types/          # TypeScript 类型定义
│   └── views/          # 业务页面
├── index.html
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## 启动方式

```bash
# 安装依赖
npm install

# 开发启动（默认 http://localhost:5173）
npm run dev

# 构建
npm run build
```

## 设计规范

全局 Design Token 定义于 `src/assets/css/global.css`，所有组件复用全局变量，禁止零散自定义色值。