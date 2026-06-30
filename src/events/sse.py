from events.event_schema import AgentEvent

class SseEncoder:
    def encode(self, event: AgentEvent) -> str:
        return f"event: {event.event_type}\ndata: {event.model_dump_json()}\n\n"
