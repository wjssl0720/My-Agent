from pathlib import Path
from uuid import uuid4
from context.caller_context import CallerContext
from workspace.models import Workspace

class WorkspaceManager:
    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = base_dir or Path("/tmp/ecom_agent_workspaces")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._workspaces: dict[str, Workspace] = {}

    @classmethod
    def default(cls) -> "WorkspaceManager":
        return cls()

    async def create(self, *, caller: CallerContext, session_id: str) -> Workspace:
        workspace_id = str(uuid4())
        path = self.base_dir / workspace_id
        path.mkdir(parents=True, exist_ok=True)
        workspace = Workspace(
            workspace_id=workspace_id,
            tenant_id=caller.tenant_id,
            user_id=caller.user_id,
            session_id=session_id,
            base_path=str(path),
            status="active",
        )
        self._workspaces[workspace_id] = workspace
        return workspace

    async def get(self, workspace_id: str) -> Workspace | None:
        return self._workspaces.get(workspace_id)

    async def close(self, workspace_id: str) -> None:
        if workspace_id in self._workspaces:
            self._workspaces[workspace_id].status = "closed"
