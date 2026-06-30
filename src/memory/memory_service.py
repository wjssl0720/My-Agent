from typing import Any
from memory.memory_manager import MemoryManager

class MemoryService:
    # Backward-compatible facade used by AgentOrchestrator.
    def __init__(self, manager: MemoryManager | None = None) -> None:
        self.manager = manager or MemoryManager.default()

    @classmethod
    def default(cls) -> "MemoryService":
        return cls()

    async def load(self, session_id: str) -> dict[str, Any]:
        return await self.manager.short_term.load(session_id)

    async def append(self, session_id: str, item: dict[str, Any]) -> None:
        await self.manager.short_term.append(session_id, item)
