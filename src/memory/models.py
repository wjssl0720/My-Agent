from typing import Any, Literal
from pydantic import BaseModel, Field

MemoryType = Literal["short_term", "long_term", "task_state", "business_object"]

class MemoryRecord(BaseModel):
    memory_id: str
    memory_type: MemoryType
    scope: str
    key: str
    value: dict[str, Any]
    metadata: dict[str, Any] = Field(default_factory=dict)

class MemoryQuery(BaseModel):
    scope: str
    query: str | None = None
    key: str | None = None
    top_k: int = 5

class MemoryWrite(BaseModel):
    scope: str
    key: str
    value: dict[str, Any]
    metadata: dict[str, Any] = Field(default_factory=dict)

class MemorySummary(BaseModel):
    session_id: str
    summary: str
    facts: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
