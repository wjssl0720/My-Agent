# My Agent

电商企业内部多 Agent 智能体执行平台

## 现在的核心分层

```text
api/          Java 调用入口
loop/         Agent 执行循环
runtime/      Local / AgentScope / LangGraph 等执行后端
tools/        ToolGateway / Dynamic Tool Registry / ToolPack
mcp/          MCP client / server registry / tool adapter
skills/       Skill runtime
rag/          RAG 内部实现
memory/       短期记忆 / 长期记忆 / 任务状态 / 业务对象记忆
context/      上下文预算 / 窗口 / 摘要 / 压缩
workspace/    沙箱 / 文件系统 / 产物 / 执行器
hooks/        生命周期钩子
execution/    可恢复执行 / checkpoint / queue / timeout / cancel
events/       event bus / event store / stream
evaluation/   benchmark / judge / replay / report / failure analysis
observability/ trace / metrics / cost / token usage
workflows/    确定性业务流程
```

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m verification.run_verification
pytest -q
uvicorn main:app --reload
```

## 当前状态

未真实接入：
- Redis / PostgreSQL / VectorDB
- AgentScope 真实 runtime adapter
- SSE / WebSocket 网关
- 真实队列系统
- 真实 sandbox 容器
- Langfuse / LangSmith / OTel
