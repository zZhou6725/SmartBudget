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
  - [x] 费用报销页面（筛选/统计/CRUD/详情抽屉）
  - [x] 预算管理页面（统计/筛选/CRUD/预算调整）
  - [x] AI 财务助手（快捷提问 + ChatContainer对话）
  - [x] 数据看板（4象限图表：趋势/排名/占比/预算执行）
  - [x] 消息预警中心（筛选/标记已读/全部已读/删除）
  - [x] 组织权限页（部门管理+用户管理 Tab切换）
  - [x] 个人中心（头像+基本信息表单+修改密码）
- [x] 阶段4：登录页面（粒子动画+JWT鉴权）
- [x] 阶段5：前后端联调（axios实例+API代理+8模块API解封）

### 后端
- [x] 阶段0：项目初始化底座（core/config/database/alembic）
- [x] 阶段3：业务模块（8/8 全部完成）
  - [x] 工作台 API（overview / pending-approvals / expense-trend）
  - [x] 费用报销 CRUD 接口（6端点）
  - [x] 预算管理接口（7端点）
  - [x] AI 财务助手接口
  - [x] 数据看板接口（4端点聚合查询）
  - [x] 消息预警接口（5端点CRUD）
  - [x] 组织权限接口（8端点：部门+用户CRUD）
  - [x] 个人中心接口（3端点：获取/编辑/改密码）
- [x] 阶段4：JWT鉴权（登录+Bearer验证）
- [x] 阶段5：数据库打通（MySQL+真实查询+种子数据）

## 快速启动

### 1. 数据库初始化
```bash
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS finbalance DEFAULT CHARACTER SET utf8mb4;"
cp backend/.env.example backend/.env  # 编辑填入数据库密码
cd backend
alembic upgrade head          # 创建5张表
python seed.py                # 插入演示数据
```

### 2. 后端
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
# Swagger → http://127.0.0.1:8000/docs
```

### 3. 前端
```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

### 登录凭证

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |
| zhangsan | 123456 | 部门经理 |
| lisi | 123456 | 财务 |
