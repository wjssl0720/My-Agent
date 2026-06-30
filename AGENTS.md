# AGENTS.md

## 工程约束

1. Java / SpringCloud 负责外部登录、SSO、菜单权限、API 网关鉴权。
2. Python Agent Service 只信任 Java 传入的 CallerContext。
3. Python 只做 Agent 执行层 permission：tool、参数、RAG scope、HITL、SQL 安全。
4. RAG 是 tool，必须经过 ToolGateway。
5. MCP / Skills / SubAgents 必须纳入 trace 与 verification。
6. 复杂任务必须经过 TaskPlanner。
7. 不允许把全量 tools 一股脑丢给模型，必须经过 ToolPackBuilder。

