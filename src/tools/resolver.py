from agents.profiles import AgentProfile
from context.context_pack import ContextPack
from tools.dynamic_registry import DynamicToolRegistry
from tools.tool_pack import ToolPack
from tools.tool_policy import ToolPolicy

class ToolPackBuilder:
    def __init__(
        self,
        registry: DynamicToolRegistry | None = None,
        policy: ToolPolicy | None = None,
        max_tools_per_request: int = 12,
    ) -> None:
        self.registry = registry or DynamicToolRegistry.default()
        self.policy = policy or ToolPolicy()
        self.max_tools_per_request = max_tools_per_request

    async def build(
        self,
        *,
        profile: AgentProfile,
        context: ContextPack,
        task_intent: str | None = None,
    ) -> ToolPack:
        candidates = await self.registry.list_candidates(profile=profile, context=context, task_intent=task_intent)
        items = [self.policy.apply(candidate, context) for candidate in candidates]

        visible_count = 0
        for item in items:
            if not item.include_in_model:
                continue
            visible_count += 1
            if visible_count > self.max_tools_per_request:
                item.include_in_model = False

        return ToolPack(agent_id=profile.agent_id, task_intent=task_intent, items=items)
