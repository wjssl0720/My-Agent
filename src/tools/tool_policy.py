from context.context_pack import ContextPack
from permissions.permission_engine import PermissionEngine
from tools.tool_pack import ToolCandidate, ToolPackItem

class ToolPolicy:
    def __init__(
        self,
        permission_engine: PermissionEngine | None = None,
        include_denied_tools_in_prompt: bool = False,
    ) -> None:
        self.permission_engine = permission_engine or PermissionEngine.default()
        self.include_denied_tools_in_prompt = include_denied_tools_in_prompt

    def apply(self, candidate: ToolCandidate, context: ContextPack) -> ToolPackItem:
        decision = self.permission_engine.decide_tool(context.caller, candidate.name, {})
        include = decision.decision in ("allow", "ask") or self.include_denied_tools_in_prompt
        return ToolPackItem(
            name=candidate.name,
            permission=decision.decision,
            reason=decision.reason,
            source=candidate.source,
            risk_level=candidate.risk_level,
            include_in_model=include,
        )
