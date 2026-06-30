from typing import Any

class TaskStateStore:
    # 长任务状态存储。当前是 in-memory；生产建议 PostgreSQL。
    def __init__(self) -> None:
        self._store: dict[str, dict[str, Any]] = {}

    async def load(self, task_id: str) -> dict[str, Any] | None:
        return self._store.get(task_id)

    async def save(self, task_id: str, state: dict[str, Any]) -> None:
        self._store[task_id] = state

    async def append_event(self, task_id: str, event: dict[str, Any]) -> None:
        state = self._store.setdefault(task_id, {"events": []})
        state.setdefault("events", []).append(event)
