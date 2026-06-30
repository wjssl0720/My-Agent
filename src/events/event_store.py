from collections import defaultdict
from events.event_schema import AgentEvent

class EventStore:
    def __init__(self) -> None:
        self._events_by_session: dict[str, list[AgentEvent]] = defaultdict(list)

    async def append(self, event: AgentEvent) -> None:
        key = event.session_id or "global"
        self._events_by_session[key].append(event)

    async def list_by_session(self, session_id: str) -> list[AgentEvent]:
        return self._events_by_session.get(session_id, [])
