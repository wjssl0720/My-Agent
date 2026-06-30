from workspace.models import ExecResult, Workspace
from workspace.sandbox import Sandbox

class PythonExecutor:
    def __init__(self, sandbox: Sandbox | None = None) -> None:
        self.sandbox = sandbox or Sandbox()

    async def execute(self, workspace: Workspace, code: str) -> ExecResult:
        return await self.sandbox.run_python(workspace, code)
