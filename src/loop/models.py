from typing import Any, Literal
from pydantic import BaseModel, Field
from context.context_pack import ContextPack
from core.models import Citation, LoopEvent, ToolCallRecord

ActionType = Literal["tool", "subagent", "final", "noop"]

class TaskItem(BaseModel):
    task_id: str
    description: str
    assignee: str | None = None
    status: Literal["pending", "running", "done", "failed"] = "pending"

class TaskPlan(BaseModel):
    is_complex: bool = False
    goal: str
    tasks: list[TaskItem] = Field(default_factory=list)

class ResolvedTool(BaseModel):
    name: str
    permission: Literal["allow", "deny", "ask"]
    reason: str

class LoadedSkill(BaseModel):
    name: str
    content: str

class LoopAction(BaseModel):
    action_type: ActionType
    content: str | None = None
    tool_name: str | None = None
    tool_args: dict[str, Any] = Field(default_factory=dict)
    subagent_name: str | None = None
    subtask: str | None = None

class LoopState(BaseModel):
    message: str
    agent_id: str
    context: ContextPack
    system_prompt: str
    available_tools: list[ResolvedTool] = Field(default_factory=list)
    loaded_skills: list[LoadedSkill] = Field(default_factory=list)
    task_plan: TaskPlan
    messages: list[dict[str, Any]] = Field(default_factory=list)
    tool_calls: list[ToolCallRecord] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)
    events: list[LoopEvent] = Field(default_factory=list)
    step: int = 0
    final_answer: str | None = None

    def add_event(self, event_type: str, payload: dict[str, Any]) -> None:
        self.events.append(LoopEvent(type=event_type, payload=payload))
