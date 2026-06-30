from collections import deque
from execution.models import ExecutionState

class TaskQueue:
    def __init__(self) -> None:
        self._queue: deque[ExecutionState] = deque()

    async def enqueue(self, execution: ExecutionState) -> None:
        self._queue.append(execution)

    async def dequeue(self) -> ExecutionState | None:
        if not self._queue:
            return None
        return self._queue.popleft()

    def size(self) -> int:
        return len(self._queue)
