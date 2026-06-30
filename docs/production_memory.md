# Production Memory Architecture

memory 多层：

```text
MemoryManager
├── ShortTermMemory
├── LongTermMemory
├── TaskStateStore
├── BusinessObjectMemory
├── MemoryPolicy
└── MemorySummarizer
```

当前实现是 in-memory，占位生产结构。后续可替换成 Redis / PostgreSQL / Vector DB。
