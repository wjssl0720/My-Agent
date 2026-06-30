from uuid import uuid4
from execution.models import Checkpoint, ExecutionState

class CheckpointStore:
    def __init__(self) -> None:
        self._checkpoints: dict[str, list[Checkpoint]] = {}

    async def save(self, execution: ExecutionState) -> Checkpoint:
        checkpoint = Checkpoint(
            checkpoint_id=str(uuid4()),
            execution_id=execution.execution_id,
            step=execution.current_step,
            state=execution.state,
        )
        self._checkpoints.setdefault(execution.execution_id, []).append(checkpoint)
        return checkpoint

    async def latest(self, execution_id: str) -> Checkpoint | None:
        checkpoints = self._checkpoints.get(execution_id, [])
        return checkpoints[-1] if checkpoints else None
