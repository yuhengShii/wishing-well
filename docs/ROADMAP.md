# 开发路线图

本文档记录许愿池各阶段的开发计划和里程碑。

---

## 阶段一：MVP（最小可行产品）

**目标**：跑通核心闭环，用户能提交愿望、能投票、管理员能审核。

### 后端

- [ ] **Vote 模型**：愿望投票表（wish_id, user_openid, created_at）
- [ ] `POST /wishes/{id}/vote` — 投票接口（每人每愿望限一票）
- [ ] `DELETE /wishes/{id}/vote` — 取消投票
- [ ] `GET /wishes/?sort=votes` — 按票数排序列表
- [ ] **Vote 测试用例**：正常投票、重复投票、取消投票
- [ ] `models.py` 添加 `vote_count` 字段（冗余计数，查询高效）

### 前端

- [ ] 更新愿望列表页：显示票数 + 投票按钮
- [ ] 投票交互：点击投票 → 调用 API → 更新本地状态
- [ ] 列表排序切换：最新 / 最热（票数）
- [ ] 愿望详情页：显示投票数和投票按钮

---

## 阶段二：微信授权登录

**目标**：接入微信登录，获取用户身份，防止刷票。

### 后端

- [x] 微信登录接口：`POST /auth/login`（接收 code，换 openid）✅
- [x] User 模型：存储 openid、昵称、头像、创建时间 ✅
- [ ] 中间件/依赖：提取请求头中的 `Authorization: Bearer <token>`
- [ ] 投票接口加登录校验：未登录用户不能投票

### 前端

- [ ] 小程序端获取微信登录 code
- [ ] 调用后端登录接口，存储 token
- [ ] 所有 API 请求自动附加 token
- [ ] 未登录状态：提示授权登录后才能投票

---

## 阶段三：管理后台

**目标**：管理员能审核愿望、设置状态、查看统计数据。

### 后端

- [ ] AdminUser 模型：管理员账号
- [ ] `GET /admin/wishes` — 管理员列表（含全部状态）
- [ ] `PATCH /admin/wishes/{id}/status` — 更新状态
- [ ] `PATCH /admin/wishes/{id}/pin` — 置顶/取消置顶
- [ ] `GET /admin/stats` — 统计数据（总愿望数、总票数、分类分布、每日提交趋势）
- [ ] 管理员登录接口（独立 admin 账号体系，或复用微信登录）

### 前端

- [ ] 新增管理端页面（独立 tab 或新页面）
- [ ] 愿望审核列表（pending 状态优先）
- [ ] 状态操作按钮
- [ ] 统计面板（图表：饼图 + 折线图）

---

## 阶段四：增强互动

**目标**：提升用户参与感和产品粘性。

- [ ] Comment 模型 + 评论接口
- [ ] 愿望详情页显示评论列表
- [ ] 收藏/关注愿望
- [ ] 公告系统：管理员发布公告，用户首页展示
- [ ] 进度条：管理员填写当前开发进度（0-100%）

---

## 阶段五：运营与优化

**目标**：提升数据可用性和用户体验。

- [ ] 用户贡献榜单（提交最多/投票最多）
- [ ] 数据导出：CSV 格式导出愿望数据
- [ ] 搜索功能：按关键词搜索愿望
- [ ] 标签功能：一个愿望可有多个标签
- [ ] 推送通知：状态变更通知提交者（需微信消息模板）
- [ ] SQLite → MySQL/PostgreSQL 迁移
- [ ] Redis 缓存（高票愿望列表缓存）
- [ ] 生产部署：Gunicorn + Uvicorn + Nginx + HTTPS

---

## 当前阶段

> **阶段一：MVP** — 进行中

下一步具体任务：

1. 在 `backend/app/models.py` 添加 Vote 模型
2. 在 `backend/app/routers/` 添加 votes.py
3. 在 `backend/app/tests/` 添加投票测试用例
4. 前端愿望列表页增加投票按钮和票数展示

---

## 前端页面重构（5 Tab）

**目标**：从单页到多 Tab 架构，提升用户体验和代码组织。

### 页面规划

| 页面 | 路径 | 功能 |
|------|------|------|
| 首页（index）| pages/index/index | 愿望列表 + 排序切换 |
| 添加愿望（add-wish）| pages/add-wish/index | 独立的添加愿望表单 |
| 我的愿望（my-wishes）| pages/my-wishes/index | 我提交的愿望列表 + 状态跟踪 |
| 我的投票（my-votes）| pages/my-votes/index | 我支持的愿望列表 |
| 分类（categories）| pages/categories/index | 按分类浏览愿望 |
| 我的（profile）| pages/profile/index | 用户信息 + 设置（语言切换）|

### TabBar 改造

- [ ] 中间加号按钮（突出"发布愿望"入口）
- [ ] 加号点击跳转到添加愿望页

### 技术实现

- [x] 配置 Taro tabBar（5个 Tab）
- [x] 拆分首页为独立 Tab 页面
- [x] 新增 pages/my-wishes/ 页面
- [x] 新增 pages/my-votes/ 页面
- [x] 新增 pages/categories/ 页面
- [x] 新增 pages/profile/ 页面
- [ ] 新增 pages/add-wish/ 页面
- [ ] TabBar 中间加号按钮
- [ ] 新增 pages/my-votes/ 页面
- [ ] 新增 pages/categories/ 页面
- [ ] 新增 pages/profile/ 页面
- [ ] 统一 API 调用层（api/）
- [ ] 统一 i18n 国际化

---

## 附录：已完成的附加功能

### 中英文切换（已完成）

**目标**：支持界面中英文切换，提升国际化体验。

- [x] 简单 i18n 实现（reactive + 翻译对象）
- [x] 语言文件：中文（zh）/ 英文（en）
- [x] 语言切换按钮（Header）
- [x] 持久化语言选择（storage）
