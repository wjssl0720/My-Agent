from enum import StrEnum
from pydantic import BaseModel, Field

class HookPoint(StrEnum):
    BEFORE_PROMPT_BUILD = "before_prompt_build"
    AFTER_PROMPT_BUILD = "after_prompt_build"
    BEFORE_MODEL_CALL = "before_model_call"
    AFTER_MODEL_CALL = "after_model_call"
    BEFORE_TOOL_CALL = "before_tool_call"
    AFTER_TOOL_CALL = "after_tool_call"
    BEFORE_SUBAGENT_DISPATCH = "before_subagent_dispatch"
    AFTER_SUBAGENT_FINISH = "after_subagent_finish"
    BEFORE_FINAL_ANSWER = "before_final_answer"
    ON_ERROR = "on_error"

class HookContext(BaseModel):
    hook_point: HookPoint
    trace_id: str | None = None
    session_id: str | None = None
    agent_id: str | None = None
    payload: dict = Field(default_factory=dict)

class HookResult(BaseModel):
    allowed: bool = True
    message: str | None = None
    mutations: dict = Field(default_factory=dict)
