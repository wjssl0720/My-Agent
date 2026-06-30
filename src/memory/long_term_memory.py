from uuid import uuid4
from memory.models import MemoryQuery, MemoryRecord, MemoryWrite

class LongTermMemory:
    # 长期记忆接口。当前是 in-memory；生产建议 PostgreSQL + Vector DB。
    def __init__(self) -> None:
        self._records: list[MemoryRecord] = []

    async def search(self, query: MemoryQuery) -> list[MemoryRecord]:
        records = [r for r in self._records if r.scope == query.scope]
        if query.key:
            records = [r for r in records if r.key == query.key]
        return records[: query.top_k]

    async def write(self, write: MemoryWrite) -> MemoryRecord:
        record = MemoryRecord(
            memory_id=str(uuid4()),
            memory_type="long_term",
            scope=write.scope,
            key=write.key,
            value=write.value,
            metadata=write.metadata,
        )
        self._records.append(record)
        return record
