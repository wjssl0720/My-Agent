from typing import Literal
from pydantic import BaseModel, Field

ToolSource = Literal["static", "rag", "mcp", "skill"]

class ToolCandidate(BaseModel):
    name: str
    description: str
    source: ToolSource
    risk_level: str = "low"
    metadata: dict = Field(default_factory=dict)

class ToolPackItem(BaseModel):
    name: str
    permission: Literal["allow", "deny", "ask"]
    reason: str
    source: ToolSource = "static"
    risk_level: str = "low"
    include_in_model: bool = True

class ToolPack(BaseModel):
    agent_id: str
    task_intent: str | None = None
    items: list[ToolPackItem] = Field(default_factory=list)

    def model_visible_tools(self) -> list[ToolPackItem]:
        return [item for item in self.items if item.include_in_model and item.permission in ("allow", "ask")]
