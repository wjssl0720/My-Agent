# Durable Execution

`execution/` 负责：

- ExecutionState
- Checkpoint
- CheckpointStore
- TaskQueue
- TaskRunner
- ResumePolicy
- RetryPolicy
- TimeoutPolicy
- CancellationToken

生产中应接 PostgreSQL / Redis / MQ / workflow engine。
