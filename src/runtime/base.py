from typing import Protocol
from pydantic import BaseModel, Field
from context.context_pack import ContextPack
from core.models import Citation, LoopEvent, ToolCallRecord

class RuntimeInput(BaseModel):
    message: str
    agent_id: str
    context: ContextPack

class RuntimeOutput(BaseModel):
    answer: str
    tool_calls: list[ToolCallRecord] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)
    events: list[LoopEvent] = Field(default_factory=list)

class AgentRuntime(Protocol):
    async def invoke(self, runtime_input: RuntimeInput) -> RuntimeOutput:
        ...
