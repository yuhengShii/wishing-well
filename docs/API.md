# API 接口文档

> 基础路径：`http://127.0.0.1:8000`（开发环境）

## 愿望（Wishes）

### 创建愿望

**POST** `/wishes/`

**请求体**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 愿望标题，最多 200 字符 |
| description | string | 否 | 详细描述 |
| category | string | 否 | 分类标签 |
| contact | string | 否 | 联系方式 |

**响应** `201 Created`：

```json
{
  "id": 1,
  "title": "希望有个记账功能",
  "description": "每天记流水太麻烦了",
  "category": "生活",
  "priority": 0,
  "status": "pending",
  "vote_count": 0,
  "contact": "wx:xxx",
  "created_at": "2026-04-24T10:30:00",
  "updated_at": null
}
```

---

### 获取愿望列表

**GET** `/wishes/`

**查询参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| category | string | 按分类过滤 |
| status | string | 按状态过滤 |
| sort | string | 排序方式：`latest`（最新，默认）/ `votes`（票数）|
| skip | int | 跳过记录数（分页，默认 0）|
| limit | int | 返回记录数（默认 50）|

**响应** `200 OK`：

```json
[
  {
    "id": 1,
    "title": "愿望1",
    "vote_count": 5,
    "status": "pending",
    "created_at": "2026-04-24T10:30:00"
  }
]
```

---

### 获取单个愿望

**GET** `/wishes/{id}`

**响应** `200 OK`：返回完整愿望对象。

**响应** `404 Not Found`：

```json
{ "detail": "愿望不存在" }
```

---

### 更新愿望

**PUT** `/wishes/{id}`

所有字段均可单独更新（支持部分更新）。

**请求体**：

```json
{
  "status": "approved",
  "priority": 1
}
```

**响应** `200 OK`：返回更新后的完整对象。

---

### 删除愿望

**DELETE** `/wishes/{id}`

软删除，将 `is_deleted` 置为 `true`。

**响应** `200 OK`：

```json
{ "message": "删除成功" }
```

---

## 投票（Votes）

> 每人每愿望限投一票。未登录状态下通过 `X-Client-ID` 请求头识别客户端（Phase 2 接入微信登录后改为 openid）。

### 对愿望投票

**POST** `/wishes/{id}/vote`

**请求头**（可选）：`X-Client-ID: <客户端标识>`

**响应** `200 OK`：

```json
{ "message": "投票成功", "vote_count": 1 }
```

**响应** `400 Bad Request`（已投过票）：

```json
{ "detail": "已经投过票了" }
```

---

### 取消投票

**DELETE** `/wishes/{id}/vote`

**响应** `200 OK`：

```json
{ "message": "取消投票成功", "vote_count": 0 }
```

**响应** `400 Bad Request`（未投过票）：

```json
{ "detail": "尚未投过票" }
```

---

### 查询投票状态

**GET** `/wishes/{id}/voted`

**响应** `200 OK`：

```json
{ "voted": true, "vote_count": 3 }
```

---

## 状态码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 422 | 请求体验证失败（Pydantic 校验未通过）|
| 500 | 服务器内部错误 |
