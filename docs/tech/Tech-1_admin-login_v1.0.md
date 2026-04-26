# Admin 登录页面 — Tech Spec

**ID**: Tech-1
**状态**: Draft
**负责人**: Architect
**日期**: 2026-04-24
**更新日期**: 2026-04-24

---

## 上下文

基于已批准的 PRD-1（admin 登录页面），本项目从零开始，需构建一个最小可工作的 admin 认证入口。

## 架构

采用最小化 Web 技术栈：

- **前端**: 纯 HTML + CSS + JavaScript（无框架依赖）
- **后端**: Python Flask（单文件，最小依赖）
- **认证方式**: Session Cookie（Flask 内置 session）
- **部署形态**: 单一进程运行，同时提供静态页面和 API

```
Browser ──HTTP──▶ Flask App
                ├── /          → 返回 login.html
                ├── /api/login → 处理认证请求
                └── /admin     → 返回 admin.html（受 session 保护）
```

## 接口

### POST /api/login

**Request**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (Success)**:
- HTTP 200
- Set-Cookie: session=...
```json
{
  "success": true
}
```

**Response (Failure)**:
- HTTP 401
```json
{
  "success": false,
  "message": "用户名或密码错误"
}
```

### GET /admin

- 检查 session 中是否存在 `logged_in = True`
- 若未登录，重定向到 `/`
- 若已登录，返回 admin.html

## 数据流

1. 用户访问 `/`，Flask 返回 `login.html`
2. 用户填写用户名、密码，点击登录
3. 前端 JS 进行非空校验；若为空，显示错误提示，不发送请求
4. 前端 JS 通过 `fetch` POST `/api/login`
5. 后端校验凭据（MVP 阶段使用硬编码凭据 `admin` / `admin123`）
6. 凭据正确 → 设置 session，返回 `success: true`
7. 凭据错误 → 返回 `success: false`，不设置 session
8. 前端收到成功响应后，跳转至 `/admin`
9. 前端收到失败响应后，显示统一错误信息（不区分用户名或密码错误）

## 可测试性

| 测试层级 | 测试目标 | 方式 |
|---------|---------|------|
| 单元测试 | 后端认证逻辑（正确/错误凭据）| Python unittest |
| 前端测试 | 表单非空校验 | 手动 / 简单 JS 测试 |
| E2E | 完整登录成功与失败流程 | 手动验证 |

## 风险

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 硬编码凭据 | 仅适用于 MVP/演示，不可用于生产 | Tech Spec 中显式标注，生产环境必须接入数据库 + 密码哈希 |
| 无 HTTPS | 凭据明文传输 | MVP 阶段仅本地运行，生产必须启用 TLS |
| 无密码哈希 | 安全风险 | MVP 阶段明文比对，生产必须切换为 bcrypt/argon2 |

## 发布推进

1. 确认 Python 3 环境可用
2. 安装依赖：`pip install flask`
3. 运行：`python app.py`
4. 访问 `http://localhost:5000`

## 回滚

1. 停止 Flask 进程
2. `git revert` 到上一版本
3. 重新运行 `python app.py`

## 评审记录

待 Gate 2 评审后填写。

## 版本历史

| 版本 | 日期 | 变更说明 | 变更人 |
|------|------|---------|-------|
| v1.0 | 2026-04-24 | 初始版本 | Architect |

## 前序文档追溯链

基于：PRD-1 v1.0（docs/prd/PRD-1_admin-login_v1.0.md）
Tech Spec 依赖：PRD-1 v1.0

## 评审记录表

| 评审日期 | 评审节点 | 评审结果 | 评审人 | 意见/打回原因 | 修改后版本 |
|----------|---------|---------|-------|-------------|-----------|
| 2026-04-24 | Gate 2 | 通过 | QA+Engineer+PM | — | v1.0 |
