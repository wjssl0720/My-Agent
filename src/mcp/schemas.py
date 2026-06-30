from pydantic import BaseModel, Field

class McpServerConfig(BaseModel):
    name: str
    enabled: bool = False
    base_url: str | None = None
    auth_type: str = "none"
    headers: dict[str, str] = Field(default_factory=dict)
    tools: list[str] = Field(default_factory=list)

class McpToolSchema(BaseModel):
    name: str
    description: str = ""
    input_schema: dict = Field(default_factory=dict)
    output_schema: dict = Field(default_factory=dict)
    server_name: str
    risk_level: str = "low"

class McpCallRequest(BaseModel):
    server_name: str
    tool_name: str
    arguments: dict = Field(default_factory=dict)

class McpCallResult(BaseModel):
    server_name: str
    tool_name: str
    result: dict
