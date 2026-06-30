from workspace.models import ExecResult, Workspace
from workspace.sandbox import Sandbox

class ShellExecutor:
    def __init__(self, sandbox: Sandbox | None = None) -> None:
        self.sandbox = sandbox or Sandbox()

    async def execute(self, workspace: Workspace, command: str) -> ExecResult:
        return await self.sandbox.run_shell(workspace, command)
