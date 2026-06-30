from typing import Literal
from pydantic import BaseModel, Field

WorkspaceStatus = Literal["created", "active", "closed", "failed"]

class Workspace(BaseModel):
    workspace_id: str
    tenant_id: str
    user_id: str
    session_id: str
    base_path: str
    status: WorkspaceStatus = "created"
    metadata: dict = Field(default_factory=dict)

class SandboxPolicy(BaseModel):
    allow_shell: bool = False
    allow_python: bool = True
    allow_network: bool = False
    max_runtime_seconds: int = 60

class Artifact(BaseModel):
    artifact_id: str
    workspace_id: str
    path: str
    artifact_type: str = "file"
    metadata: dict = Field(default_factory=dict)

class ExecResult(BaseModel):
    command: str
    exit_code: int
    stdout: str = ""
    stderr: str = ""
    metadata: dict = Field(default_factory=dict)
