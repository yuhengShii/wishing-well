# 工作规则

## 规则

1. **每次只做一个功能点**
   不同时并行开发多个功能，聚焦当前任务。

2. **当前功能点端到端验证通过后，才能开始下一个**
   必须实际运行验证（后端启动 + 前端构建 + 接口调用），不能只写完代码就结束。

3. **不要在实现功能 A 时"顺便"重构功能 B**
   功能开发和重构分开处理。重构应在独立的工作单元中进行。

4. **功能或 Bug 修复验证通过后，立即 commit**
   每完成一个功能点，或修复一个 Bug 并验证通过后，应该尽快 commit，不要等到多个功能完成后再批量提交。保持提交的原子性，一个 commit 对应一个完整的可工作增量。

## 说明

此规则适用于整个项目的开发阶段。规则的核心目的是避免范围蔓延和半成品堆积，确保每个功能独立验证通过后，再积累可工作的增量。

---

## 功能验证标准

每个功能点完成后，必须同时通过以下验证：

### 后端验证

```bash
# 1. 单元测试全过
cd backend && .\.venv\Scripts\python -m pytest app/tests/ -v

# 2. 服务能正常启动
cd backend && .\.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000

# 3. API 实际调用能通
# 浏览器访问 http://127.0.0.1:8000/docs
# 用 Swagger UI 手动点接口验证
```

### 前端验证

```bash
# 4. Taro 编译不报错
cd wishing-well-frontend && npm run dev:weapp

# 5. dist/ 目录有输出文件
```

### 判断标准

同时满足 **pytest 全过 + Taro 编译成功**，视为该功能点完成。微信开发者工具验证（步骤 6）若有环境问题可跳过，前两条必须通过。

---

## 已知问题

### npm install 网络超时（2026-04-24）

npm install 在当前环境无法访问任何 registry（registry.npmjs.org 和 registry.npmmirror.com 均 ETIMEDOUT），疑似网络代理/防火墙限制。

**影响**：前端无法安装依赖，Taro 编译步骤无法验证。

**解决**：在本地网络环境下执行：

```bash
cd wishing-well-frontend
npm install
npm run dev:weapp
```

同时启动后端：

```bash
cd backend
./.venv/Scripts/python -m uvicorn app.main:app --reload --port 8000
```

用微信开发者工具导入 `wishing-well-frontend/dist` 目录进行联调验证。
