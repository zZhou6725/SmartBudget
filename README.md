# FinBalance 财衡中台

企业级预算管理与费用报销中台系统。

## 技术栈

| 端 | 技术 |
|---|---|
| 前端 | Vue3 + TypeScript + Vite + Element Plus + Pinia + Vue Router + SCSS |
| 后端 | Python3.10+ + FastAPI + MySQL8 + Redis + SQLAlchemy + Pydantic V2 + Alembic + PyJWT |

## 项目结构

```
FinBalance-Project
├── frontend/          # Vue3 前端子项目
│   ├── src/
│   │   ├── api/       # 接口请求（模块化）
│   │   ├── components/ # 全局公共组件
│   │   ├── layout/    # 布局组件（侧边栏/顶部栏/内容区）
│   │   ├── router/    # 路由配置
│   │   ├── stores/    # Pinia 状态管理
│   │   ├── types/     # TypeScript 类型定义
│   │   └── views/     # 业务页面
│   └── README.md
├── backend/           # FastAPI 后端子项目
│   ├── app/
│   │   ├── api/v1/    # 业务接口
│   │   ├── core/      # 全局配置/统一返回/异常处理
│   │   ├── models/    # ORM 模型
│   │   ├── schemas/   # Pydantic 校验
│   │   └── service/   # 业务逻辑层
│   └── README.md
├── .gitignore
└── README.md          # 本文件
```

## 开发进度

### 前端
- [x] 阶段0：项目初始化底座（Vue3 + Vite + TS + ElementPlus）
- [x] 阶段1：Layout 布局全套（SideBar/HeaderBar/AppMain/MainLayout）
- [x] 阶段2：全局公共组件库（EmptyHolder/PageCard/StatCard/TableWrapper/ChartContainer/ChatContainer）
- [ ] 阶段3：业务模块
  - [x] 工作台首页（概览统计/待办审批/支出趋势）
  - [ ] 费用报销页面
  - [ ] 预算管理页面
  - [ ] AI 财务助手
  - [ ] 数据看板
  - [ ] 消息预警中心
  - [ ] 组织权限页
  - [ ] 个人中心
- [ ] 阶段4：登录页面
- [ ] 阶段5：全局自检与部署文档

### 后端
- [ ] 阶段0：项目初始化底座（待开发）

## 快速启动

### 前端
```bash
cd frontend
npm install
npm run dev
```

### 后端（待开发）
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```