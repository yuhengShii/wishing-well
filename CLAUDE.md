# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 工作规则（强制）

> 详见 `WORK_RULES.md`

1. **每次只做一个功能点**，不并行开发多个功能
2. **当前功能点端到端验证通过后，才能开始下一个**（必须实际运行验证）
3. **不借机顺手重构其他功能**（功能开发与重构分开）
4. **代码完成后必须通过 lint 检查**，后才能提交

## 项目概述

**许愿池** — 微信小程序，用于收集用户日常生活和工作中的需求，通过投票筛选高需求量愿望来指导 App 开发方向。技术栈：Taro(Vue3+TS) 前端 + FastAPI(Python) 后端 + SQLite 数据库。

**核心闭环**：用户提交愿望 → 其他用户投票支持 → 统计票数排序 → 团队筛选高票需求 → 开发成 App → 上线通知用户

## 技术栈

| 层 | 技术 |
|----|------|
| 前端 | Taro 4.x + Vue 3 + TypeScript |
| 后端 | Python + FastAPI + SQLAlchemy + Pydantic v2 |
| 数据库 | SQLite（开发环境）|
| 部署 | Docker + Docker Compose |

## 项目结构

```
.
├── backend/                      # FastAPI 后端
│   ├── app/
│   │   ├── main.py              # 应用入口，注册路由/中间件
│   │   ├── core/
│   │   │   ├── config.py         # 环境变量配置（Settings）
│   │   │   └── logging_config.py # 统一日志配置
│   │   ├── database.py           # SQLAlchemy 引擎和会话
│   │   ├── models.py             # ORM 模型
│   │   ├── schemas.py            # Pydantic 模型（请求/响应验证）
│   │   ├── routers/
│   │   │   └── wishes.py         # 愿望 CRUD 路由
│   │   └── tests/
│   │       └── test_wishes.py    # 单元测试（pytest + FastAPI TestClient）
│   ├── .env.example              # 环境变量模板（不提交 .env）
│   └── requirements.txt
│
├── wishing-well-frontend/        # Taro 微信小程序前端
│   ├── src/
│   │   ├── api/wish.ts           # API 封装层
│   │   ├── types/wish.ts         # TypeScript 类型定义
│   │   ├── constants/index.ts    # 全局常量（baseUrl、statusMap）
│   │   ├── utils/format.ts       # 纯工具函数
│   │   └── pages/                # 页面组件
│   ├── tests/                    # Jest 单元测试
│   ├── .eslintrc.js              # ESLint 配置
│   ├── .prettierrc.js            # Prettier 配置
│   └── package.json
│
├── docs/
│   ├── ARCHITECTURE.md           # 系统架构 + 产品需求文档
│   ├── ROADMAP.md                # 开发路线图
│   └── API.md                    # API 接口文档
│
├── WORK_RULES.md                 # 工作规则（强制）
├── PROGRESS.md                   # 开发进度记录（每次完成功能后更新）
│
├── .github/workflows/ci.yml       # GitHub Actions CI 流水线
├── docker-compose.yml
└── Dockerfile
```

## 产品功能优先级

| 优先级 | 功能 |
|--------|------|
| **P0** | 发布愿望、投票支持（每人每愿望一票）、愿望列表（最新/最热排序）、状态流转（pending→approved→implementing→implemented/rejected）、管理员审核 |
| **P1** | 微信授权登录、愿望详情页、我的愿望、数据统计面板、分类管理、搜索+标签、置顶/加精 |
| **P2** | 评论功能、实现进度条、收藏/关注、推送通知、公告系统 |
| **P3** | 用户贡献榜单、数据导出 |

详细说明见 [docs/ROADMAP.md](docs/ROADMAP.md)。

## 开发路线图

**当前阶段**：阶段一（MVP）—— 进行中

路线图详情见 [docs/ROADMAP.md](docs/ROADMAP.md)。

## 启动命令

### 后端

> 虚拟环境位于 `backend/.venv`（Windows：`.venv\Scripts\python`，WSL/Linux：`.venv/bin/python`）

```bash
cd backend
./.venv/Scripts/python -m pip install -r requirements.txt
./.venv/Scripts/python -m uvicorn app.main:app --reload --port 8000
```

运行测试：
```bash
./.venv/Scripts/python -m pytest app/tests/ -v
```

API 文档：http://127.0.0.1:8000/docs

### 前端

```bash
cd wishing-well-frontend
npm install
npm run dev:weapp
```

用微信开发者工具导入 `wishing-well-frontend/dist` 目录。

### Docker

```bash
docker-compose up --build
```

## 工程规范

### 前端分层
- `api/`：所有接口调用，**不要在页面组件中直接使用 `Taro.request`**
- `types/`：所有 TypeScript 接口定义，**禁止使用 `any`**
- `constants/`：**不包含业务逻辑**，只放配置和映射
- `utils/`：**纯函数**，无副作用，可独立测试

### 后端分层
- `routers/`：接收请求、参数校验、返回响应，不写业务逻辑
- `schemas/`：Pydantic 模型，**与数据库模型严格分离**
- `models/`：SQLAlchemy 模型，**只定义表结构**
- `core/`：**不含业务逻辑**，只放配置和基础设施

### 环境变量
所有配置通过 `backend/.env` 管理。参考 `.env.example` 创建，`.env` 不提交到 Git。

### 日志
统一使用 `logging.getLogger("wishing-well")`，通过 `LOG_LEVEL` 环境变量控制级别。

### 新增文件规范
- 新增路由文件：放在 `app/routers/` 下，并在 `main.py` 中注册
- 新增 Pydantic Schema：放在 `schemas.py` 中，与 `models.py` 分离
- 新增工具函数：放在 `utils/` 下，纯函数，有对应测试
- 新增页面组件：在 `pages/` 下建独立目录，包含 `.vue` + 样式

## API 路由

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /wishes | 列表（支持 category、status、sort、skip、limit 过滤）|
| POST | /wishes | 创建 |
| GET | /wishes/{id} | 获取单个 |
| PUT | /wishes/{id} | 更新（支持部分字段）|
| DELETE | /wishes/{id} | 软删除 |
| POST | /wishes/{id}/vote | 投票 |
| DELETE | /wishes/{id}/vote | 取消投票 |
