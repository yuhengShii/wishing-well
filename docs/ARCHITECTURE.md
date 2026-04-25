# 系统架构文档

## 1. 技术架构

许愿池采用标准前后端分离架构：

```
┌─────────────────────────┐     HTTP/JSON      ┌─────────────────┐
│   微信小程序前端 (Taro)   │ ◄──────────────► │   FastAPI 后端   │
│                          │                   │                 │
│  - 展示层：Vue 3 组件     │                   │  - 业务逻辑层    │
│  - 数据层：API 调用封装   │                   │  - 数据访问层    │
│  - 工具层：工具函数/常量   │                   │  - ORM (SQLAlchemy)
└─────────────────────────┘                   └────────┬────────┘
                                                         │
                                                    ┌─────▼─────┐
                                                    │  SQLite   │
                                                    └───────────┘
```

## 2. 前端架构

```
wishing-well-frontend/
├── src/
│   ├── api/          # API 封装层（统一封装所有接口调用）
│   │   └── wish.ts
│   ├── constants/    # 全局常量（API 地址、状态映射、选项列表）
│   │   └── index.ts
│   ├── types/        # TypeScript 类型定义（Wish、WishForm 等）
│   │   └── wish.ts
│   ├── utils/        # 纯工具函数（格式化、防抖等，无副作用）
│   │   └── format.ts
│   ├── pages/        # 页面组件
│   └── app.vue       # 根组件
└── tests/            # 单元测试
```

**分层职责**：
- `api/`：所有 HTTP 请求，统一错误处理，方便后续切换请求库
- `types/`：类型定义，IDE 自动补全，防止数据格式错误
- `constants/`：全局配置，避免硬编码
- `utils/`：纯函数，可独立测试，易于复用

## 3. 后端架构

```
backend/
├── app/
│   ├── main.py           # FastAPI 入口，注册路由和中间件
│   ├── database.py       # SQLAlchemy 引擎和会话管理
│   ├── models.py         # ORM 模型（数据库表结构）
│   ├── schemas.py        # Pydantic 模型（请求验证/响应序列化）
│   ├── core/
│   │   ├── config.py     # 环境变量配置（Settings 类）
│   │   └── logging_config.py  # 统一日志配置
│   ├── routers/          # 路由模块（按业务拆分）
│   │   └── wishes.py
│   └── tests/            # 单元测试
│       └── test_wishes.py
└── requirements.txt
```

**分层职责**：
- `routers/`：接收 HTTP 请求，调用 service 层，返回响应
- `schemas/`：请求体验证、响应序列化，完全与数据库解耦
- `models/`：数据库表结构定义
- `core/`：全局配置和日志，与业务无关

## 4. 数据模型

### Wish（愿望）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| title | String(200) | 愿望标题（必填）|
| description | Text | 详细描述 |
| category | String(50) | 分类标签 |
| priority | Integer | 优先级（默认 0）|
| status | String(20) | 状态：pending/approved/implemented/rejected |
| contact | String(200) | 联系方式 |
| is_deleted | Boolean | 软删除标记 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

## 5. 配置管理

```
.env.example  →  复制为 .env  →  填入实际值
```

所有配置通过环境变量读取，代码不包含硬编码值。开发环境和生产环境使用不同的 `.env` 文件。

## 6. 日志规范

统一使用 `logging.getLogger("wishing-well")`，日志格式：

```
2026-04-24 10:30:00 | INFO     | app.routers.wishes:23 — 创建愿望成功
```

日志级别可通过 `LOG_LEVEL` 环境变量控制（DEBUG/INFO/WARNING/ERROR）。

## 7. Docker 部署

```bash
# 构建并启动
docker-compose up --build

# 停止
docker-compose down
```

## 8. Python 虚拟环境

> 虚拟环境位于 `backend/.venv`

**激活方式**：
- Windows CMD/PowerShell：`backend\.venv\Scripts\activate`
- WSL/Linux/macOS：`source backend/.venv/bin/activate`

**安装依赖**：
```bash
./.venv/Scripts/python -m pip install -r requirements.txt
```

---

## 9. 产品需求文档

### 9.1 产品定位

许愿池是一个**需求收集与优先级排序平台**，核心价值：收集用户日常生活和工作中的真实需求，通过投票机制筛选出需求量高的愿望，指导 App 开发方向。

核心闭环：

```
用户提交愿望 → 其他用户投票支持 → 统计票数排序 → 团队筛选高票需求 → 开发成 App → 上线通知用户
```

### 9.2 用户角色

| 角色 | 说明 |
|------|------|
| **普通用户** | 提交愿望、投票支持、查看进度 |
| **管理员** | 审核愿望、设置状态、置顶/加精、数据分析 |

### 9.3 功能清单

#### 用户侧功能

| 功能 | 说明 | 优先级 |
|------|------|--------|
| 发布愿望 | 标题 + 描述 + 分类 + 联系方式（可选）| P0 |
| 投票支持 | 每个用户对每个愿望只能投一票，票数即需求量 | P0 |
| 愿望列表 | 按最新/最热/分类筛选，显示票数和状态 | P0 |
| 愿望详情 | 查看详情、参与评论、支持愿望 | P1 |
| 我的愿望 | 查看自己发布/支持的愿望及进度 | P1 |
| 微信登录 | 获取用户身份，防止刷票 | P1 |

#### 管理侧功能

| 功能 | 说明 | 优先级 |
|------|------|--------|
| 愿望审核 | 上线前审核内容，过滤无效/重复愿望 | P0 |
| 设置状态 | pending → approved → implementing → implemented/rejected | P0 |
| 置顶/加精 | 优质愿望置顶展示 | P1 |
| 数据统计 | 票数趋势图、分类分布图、每日提交量 | P1 |
| 公告通知 | 告知用户哪些愿望已被采纳/实现 | P2 |
| 分类管理 | 管理员可增删分类 | P1 |
| 搜索 + 标签 | 快速定位愿望 | P1 |

#### 进阶功能

| 功能 | 说明 | 优先级 |
|------|------|--------|
| 评论功能 | 用户讨论具体实现方式 | P2 |
| 实现进度条 | 展示开发进度 | P2 |
| 收藏/关注愿望 | 跟踪感兴趣的需求 | P2 |
| 推送通知 | 状态变更时通知提交者 | P2 |
| 热点推荐 | 自动推荐高票愿望 | P2 |
| 用户贡献榜单 | 激励用户参与 | P3 |
| 数据导出 | 方便产品团队分析 | P3 |

### 9.4 愿望状态流转

```
用户提交
    │
    ▼
pending（待审核） ──→ rejected（已拒绝）
    │                      │
    │ 管理员审核通过        │
    ▼                      │
approved（已采纳） ──────────────────→ implementing（开发中）
    │                                          │
    │                                          │
    └─────────────→ implemented（已实现）←──────┘
```

### 9.5 后续扩展方向

- [ ] 接入微信授权登录（防止刷票）
- [ ] 管理员后台（愿望审核、状态管理）
- [ ] 投票系统（需求量化核心）
- [ ] 数据统计面板（可视化需求分布）
- [ ] 分类管理（管理员可增删分类）
- [ ] 搜索 + 标签
- [ ] 评论功能
- [ ] 愿望实现进度条
- [ ] 收藏/关注愿望
- [ ] 推送通知
- [ ] 公告系统
- [ ] 用户贡献榜单
- [ ] 数据导出
- [ ] 从 SQLite 迁移到 MySQL/PostgreSQL
- [ ] 添加 Redis 缓存
- [ ] 接入文件存储（如七牛云 OSS）
- [ ] 生产环境使用 Gunicorn + Uvicorn
