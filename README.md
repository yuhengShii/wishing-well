# 许愿池

收集各年龄段用户需求，将日常工作生活中的问题转化成应用来提供便利。

## 技术栈

| 层 | 技术 |
|----|------|
| 前端 | Taro 4.x + Vue 3 + TypeScript |
| 后端 | Python + FastAPI |
| 数据库 | SQLite（开发）/ MySQL（生产）|
| 部署 | Docker + Docker Compose |

## 快速启动

### 后端

```bash
cd backend
cp .env.example .env   # 可选，保留默认配置
./.venv/Scripts/python -m pip install -r requirements.txt
./.venv/Scripts/python -m uvicorn app.main:app --reload --port 8000
```

> Windows 用户注意：WSL 下路径为 `./.venv/bin/python`。

API 文档访问：http://127.0.0.1:8000/docs

### 前端

```bash
cd wishing-well-frontend
npm install
npm run dev:weapp
```

用微信开发者工具导入目录 `wishing-well-frontend/dist`。

## 工程规范

### 代码规范
- **前端**：ESLint + Prettier，提交前运行检查
- **后端**：遵循 PEP 8，使用类型注解

### 测试
- **后端单元测试**：`.venv\Scripts\python -m pytest app/tests/ -v`
- **前端单元测试**：`npm test`（`jest.config.js`）

### 环境配置
所有配置通过 `backend/.env` 管理（参考 `.env.example`）。`.env` 不提交到版本库。

### Docker 部署

```bash
docker-compose up --build
```

## 目录结构

```
.
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── core/              # 配置和日志
│   │   ├── routers/           # 路由
│   │   └── tests/             # 单元测试
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
│
├── wishing-well-frontend/     # Taro 微信小程序前端
│   ├── src/
│   │   ├── api/               # API 封装
│   │   ├── types/             # TypeScript 类型
│   │   ├── constants/         # 全局常量
│   │   └── utils/             # 工具函数
│   ├── tests/                 # 单元测试
│   └── package.json
│
├── docs/                      # 文档
│   ├── ARCHITECTURE.md         # 架构文档
│   └── API.md                 # 接口文档
│
├── .github/workflows/ci.yml    # CI/CD 流水线
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## 注意事项

- 部署时需将前端 `src/constants/index.ts` 中的 `baseUrl` 替换为实际后端地址
- 小程序要求后端域名已备案（生产环境需配置 HTTPS 域名）
