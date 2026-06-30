from pydantic import BaseModel, Field

class ContextSummary(BaseModel):
    task_goal: str | None = None
    completed_steps: list[str] = Field(default_factory=list)
    key_facts: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    citations: list[dict] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)
