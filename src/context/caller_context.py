from pydantic import BaseModel, Field

class CallerContext(BaseModel):
    user_id: str
    tenant_id: str = "default"
    department: str = "guest"
    roles: list[str] = Field(default_factory=list)
    request_id: str | None = None
    attributes: dict[str, str] = Field(default_factory=dict)
