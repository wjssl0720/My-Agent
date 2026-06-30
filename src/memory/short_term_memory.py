from collections import defaultdict
from typing import Any

class ShortTermMemory:
    # 会话短期记忆。当前是 in-memory；生产建议 Redis。
    def __init__(self, max_messages: int = 20) -> None:
        self.max_messages = max_messages
        self._store: dict[str, list[dict[str, Any]]] = defaultdict(list)

    async def load(self, session_id: str) -> dict[str, Any]:
        return {"history": self._store.get(session_id, [])[-self.max_messages:]}

    async def append(self, session_id: str, item: dict[str, Any]) -> None:
        self._store[session_id].append(item)
        self._store[session_id] = self._store[session_id][-self.max_messages:]
