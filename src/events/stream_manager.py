from asyncio import Queue
from events.event_schema import AgentEvent

class StreamManager:
    def __init__(self) -> None:
        self._queues: dict[str, Queue] = {}

    def get_queue(self, session_id: str) -> Queue:
        if session_id not in self._queues:
            self._queues[session_id] = Queue()
        return self._queues[session_id]

    async def publish(self, event: AgentEvent) -> None:
        if event.session_id is None:
            return
        await self.get_queue(event.session_id).put(event)

    async def next_event(self, session_id: str) -> AgentEvent:
        return await self.get_queue(session_id).get()
