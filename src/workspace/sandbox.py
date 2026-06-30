from workspace.models import ExecResult, SandboxPolicy, Workspace

class Sandbox:
    def __init__(self, policy: SandboxPolicy | None = None) -> None:
        self.policy = policy or SandboxPolicy()

    async def run_python(self, workspace: Workspace, code: str) -> ExecResult:
        if not self.policy.allow_python:
            return ExecResult(command="python", exit_code=1, stderr="python execution disabled")
        return ExecResult(command="python", exit_code=0, stdout="mock python execution", metadata={"code": code})

    async def run_shell(self, workspace: Workspace, command: str) -> ExecResult:
        if not self.policy.allow_shell:
            return ExecResult(command=command, exit_code=1, stderr="shell execution disabled")
        return ExecResult(command=command, exit_code=0, stdout="mock shell execution")
