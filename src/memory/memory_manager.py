from typing import Any
from context.context_pack import ContextPack
from memory.business_object_memory import BusinessObjectMemory
from memory.long_term_memory import LongTermMemory
from memory.memory_policy import MemoryPolicy
from memory.memory_summarizer import MemorySummarizer
from memory.models import MemoryQuery, MemoryWrite
from memory.short_term_memory import ShortTermMemory
from memory.task_state_store import TaskStateStore

class MemoryManager:
    # 生产级 memory facade。外层不直接依赖 Redis/Postgres/VectorDB。
    def __init__(
        self,
        short_term: ShortTermMemory | None = None,
        long_term: LongTermMemory | None = None,
        task_state: TaskStateStore | None = None,
        business_memory: BusinessObjectMemory | None = None,
        policy: MemoryPolicy | None = None,
        summarizer: MemorySummarizer | None = None,
    ) -> None:
        self.short_term = short_term or ShortTermMemory()
        self.long_term = long_term or LongTermMemory()
        self.task_state = task_state or TaskStateStore()
        self.business_memory = business_memory or BusinessObjectMemory()
        self.policy = policy or MemoryPolicy()
        self.summarizer = summarizer or MemorySummarizer()

    @classmethod
    def default(cls) -> "MemoryManager":
        return cls()

    async def load_for_context(self, context: ContextPack) -> dict[str, Any]:
        short = await self.short_term.load(context.session_id)
        long_records = []
        if self.policy.should_load_long_term(context):
            long_records = await self.long_term.search(
                MemoryQuery(scope=f"user:{context.caller.user_id}", query=context.agent_id, top_k=5)
            )
        return {
            "short_term": short,
            "long_term": [r.model_dump() for r in long_records],
        }

    async def append_short_term(self, session_id: str, item: dict[str, Any]) -> None:
        await self.short_term.append(session_id, item)

    async def maybe_write_long_term(self, context: ContextPack, key: str, value: dict[str, Any]) -> None:
        item = {"persistable": value.get("persistable", False), **value}
        if self.policy.should_write_long_term(context, item):
            await self.long_term.write(MemoryWrite(scope=f"user:{context.caller.user_id}", key=key, value=value))

    async def compact_session(self, session_id: str) -> dict[str, Any]:
        short = await self.short_term.load(session_id)
        summary = await self.summarizer.summarize(session_id, short.get("history", []))
        return summary.model_dump()
