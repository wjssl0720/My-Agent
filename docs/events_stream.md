# Events / Stream

`events/` 负责：

- AgentEvent schema
- EventBus
- EventStore
- StreamManager
- SSE adapter
- WebSocket adapter

API 后续可新增：

```text
POST /api/v1/sessions/{session_id}/messages:stream
GET  /api/v1/sessions/{session_id}/events
```
