from typing import Literal
from pydantic import BaseModel, Field

ExecutionStatus = Literal["pending", "running", "paused", "completed", "failed", "cancelled"]

class ExecutionState(BaseModel):
    execution_id: str
    session_id: str
    agent_id: str
    status: ExecutionStatus = "pending"
    current_step: int = 0
    state: dict = Field(default_factory=dict)

class Checkpoint(BaseModel):
    checkpoint_id: str
    execution_id: str
    step: int
    state: dict = Field(default_factory=dict)
    metadata: dict = Field(default_factory=dict)
