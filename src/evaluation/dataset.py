from pydantic import BaseModel, Field

class EvaluationCase(BaseModel):
    case_id: str
    input: str
    expected: dict = Field(default_factory=dict)
    metadata: dict = Field(default_factory=dict)

class EvaluationDataset(BaseModel):
    name: str
    cases: list[EvaluationCase] = Field(default_factory=list)
