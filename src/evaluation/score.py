from pydantic import BaseModel, Field

class EvaluationScore(BaseModel):
    case_id: str
    passed: bool
    score: float = 0.0
    metrics: dict = Field(default_factory=dict)
    reason: str | None = None
