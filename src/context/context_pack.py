from pydantic import BaseModel, Field
from context.caller_context import CallerContext

class ContextPack(BaseModel):
    caller: CallerContext
    session_id: str
    agent_id: str
    short_term_memory: dict = Field(default_factory=dict)
    business_context: dict = Field(default_factory=dict)
    file_ids: list[str] = Field(default_factory=list)
    allowed_rag_scopes: list[str] = Field(default_factory=list)
