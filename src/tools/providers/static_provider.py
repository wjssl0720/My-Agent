from agents.profiles import AgentProfile
from context.context_pack import ContextPack
from tools.registry import ToolRegistry
from tools.tool_pack import ToolCandidate

class StaticToolProvider:
    name = "static"

    def __init__(self, registry: ToolRegistry | None = None) -> None:
        self.registry = registry or ToolRegistry.default()

    async def list_candidates(
        self,
        *,
        profile: AgentProfile,
        context: ContextPack,
        task_intent: str | None,
    ) -> list[ToolCandidate]:
        all_specs = {spec["name"]: spec for spec in self.registry.list_tools()}
        candidates = []
        for tool_name in profile.tools:
            spec = all_specs.get(tool_name)
            if not spec:
                continue
            candidates.append(
                ToolCandidate(
                    name=tool_name,
                    description=spec.get("description", ""),
                    source="static",
                    risk_level=spec.get("risk_level", "low"),
                )
            )
        return candidates
