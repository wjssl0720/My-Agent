from pydantic import BaseModel, Field

class AgentEvent(BaseModel):
    event_id: str
    event_type: str
    session_id: str | None = None
    trace_id: str | None = None
    payload: dict = Field(default_factory=dict)
