from events.event_schema import AgentEvent

class WebSocketEventAdapter:
    def encode(self, event: AgentEvent) -> dict:
        return event.model_dump()
