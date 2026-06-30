from typing import Any, Protocol
from pydantic import BaseModel, Field
from context.context_pack import ContextPack

class ToolSpec(BaseModel):
    name: str
    description: str
    risk_level: str = "low"
    input_schema: dict[str, Any] = Field(default_factory=dict)

class Tool(Protocol):
    spec: ToolSpec

    async def execute(self, args: dict[str, Any], context: ContextPack) -> Any:
        ...
