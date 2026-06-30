from typing import Any, Literal
from pydantic import BaseModel, Field

class CreateSessionRequest(BaseModel):
    agent_id: str = "knowledge_agent"
    metadata: dict[str, Any] = Field(default_factory=dict)

class CreateSessionResponse(BaseModel):
    session_id: str
    agent_id: str

class SendMessageRequest(BaseModel):
    message: str
    agent_id: str = "knowledge_agent"
    file_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

class ToolCallRecord(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    status: Literal["planned", "executed", "denied", "approval_required", "failed"] = "planned"
    result: Any | None = None
    reason: str | None = None

class Citation(BaseModel):
    source_id: str
    title: str
    chunk_id: str | None = None
    url: str | None = None

class LoopEvent(BaseModel):
    type: str
    payload: dict[str, Any] = Field(default_factory=dict)

class SendMessageResponse(BaseModel):
    answer: str
    session_id: str
    agent_id: str
    tool_calls: list[ToolCallRecord] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)
    trace_id: str | None = None
    events: list[LoopEvent] = Field(default_factory=list)
