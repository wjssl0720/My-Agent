class AgentPlatformError(Exception):
    pass

class ToolPermissionDenied(AgentPlatformError):
    pass

class ApprovalRequired(AgentPlatformError):
    def __init__(self, tool_name: str, reason: str) -> None:
        super().__init__(f"HITL approval required for {tool_name}: {reason}")
        self.tool_name = tool_name
        self.reason = reason

class LoopExecutionError(AgentPlatformError):
    pass
