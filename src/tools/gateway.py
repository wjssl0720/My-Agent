from typing import Any
from context.context_pack import ContextPack
from core.errors import ApprovalRequired, ToolPermissionDenied
from permissions.permission_engine import PermissionEngine
from tools.registry import ToolRegistry

class ToolGateway:
    def __init__(
        self,
        registry: ToolRegistry | None = None,
        permission_engine: PermissionEngine | None = None,
    ) -> None:
        self.registry = registry or ToolRegistry.default()
        self.permission_engine = permission_engine or PermissionEngine.default()

    @classmethod
    def default(cls) -> "ToolGateway":
        return cls()

    async def execute(self, tool_name: str, args: dict[str, Any], context: ContextPack) -> Any:
        decision = self.permission_engine.decide_tool(context.caller, tool_name, args)
        if decision.decision == "deny":
            raise ToolPermissionDenied(decision.reason)
        if decision.decision == "ask":
            raise ApprovalRequired(tool_name=tool_name, reason=decision.reason)
        return await self.registry.get(tool_name).execute(args, context)
