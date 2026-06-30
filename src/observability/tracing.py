from collections import defaultdict
from uuid import uuid4

class TraceRecorder:
    def __init__(self) -> None:
        self._events: dict[str, list[dict]] = defaultdict(list)

    def start_trace(self, user_id: str, session_id: str, agent_id: str) -> str:
        trace_id = str(uuid4())
        self.add_event(trace_id, "trace.started", {"user_id": user_id, "session_id": session_id, "agent_id": agent_id})
        return trace_id

    def add_event(self, trace_id: str, event_type: str, payload: dict) -> None:
        self._events[trace_id].append({"type": event_type, "payload": payload})

    def get_events(self, trace_id: str) -> list[dict]:
        return self._events.get(trace_id, [])
