from agents.profiles import AgentProfile
from context.context_pack import ContextPack
from loop.models import ResolvedTool
from tools.resolver import ToolPackBuilder

class ToolResolver:
    # Loop 层工具解析器。V4 保留同步 resolve 兼容 V3，同时提供 async resolve_async。
    def __init__(self, builder: ToolPackBuilder | None = None) -> None:
        self.builder = builder or ToolPackBuilder()

    def resolve(self, profile: AgentProfile, context: ContextPack, task_intent: str | None = None) -> list[ResolvedTool]:
        from permissions.permission_engine import PermissionEngine
        engine = PermissionEngine.default()
        resolved = []
        for tool_name in profile.tools:
            decision = engine.decide_tool(context.caller, tool_name, {})
            resolved.append(ResolvedTool(name=tool_name, permission=decision.decision, reason=decision.reason))
        return resolved

    async def resolve_async(self, profile: AgentProfile, context: ContextPack, task_intent: str | None = None) -> list[ResolvedTool]:
        pack = await self.builder.build(profile=profile, context=context, task_intent=task_intent)
        return [ResolvedTool(name=item.name, permission=item.permission, reason=item.reason) for item in pack.items]
