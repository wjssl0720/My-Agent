from uuid import uuid4
from execution.cancellation import CancellationToken
from execution.checkpoint import CheckpointStore
from execution.models import ExecutionState
from execution.retry_policy import RetryPolicy

class TaskRunner:
    def __init__(
        self,
        checkpoint_store: CheckpointStore | None = None,
        retry_policy: RetryPolicy | None = None,
    ) -> None:
        self.checkpoint_store = checkpoint_store or CheckpointStore()
        self.retry_policy = retry_policy or RetryPolicy()

    async def create_execution(self, session_id: str, agent_id: str, state: dict | None = None) -> ExecutionState:
        return ExecutionState(
            execution_id=str(uuid4()),
            session_id=session_id,
            agent_id=agent_id,
            status="pending",
            state=state or {},
        )

    async def run_once(self, execution: ExecutionState, token: CancellationToken | None = None) -> ExecutionState:
        token = token or CancellationToken()
        token.raise_if_cancelled()
        execution.status = "running"
        execution.current_step += 1
        await self.checkpoint_store.save(execution)
        execution.status = "completed"
        return execution
