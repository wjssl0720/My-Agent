from agents.profiles import AgentProfile
from context.context_pack import ContextPack
from tools.providers.mcp_provider import McpToolProvider
from tools.providers.rag_provider import RagToolProvider
from tools.providers.skill_provider import SkillToolProvider
from tools.providers.static_provider import StaticToolProvider
from tools.tool_pack import ToolCandidate

class DynamicToolRegistry:
    def __init__(self, providers: list | None = None) -> None:
        self.providers = providers or [
            StaticToolProvider(),
            RagToolProvider(),
            McpToolProvider(),
            SkillToolProvider(),
        ]

    @classmethod
    def default(cls) -> "DynamicToolRegistry":
        return cls()

    async def list_candidates(
        self,
        *,
        profile: AgentProfile,
        context: ContextPack,
        task_intent: str | None,
    ) -> list[ToolCandidate]:
        candidates: list[ToolCandidate] = []
        seen: set[str] = set()

        for provider in self.providers:
            for candidate in await provider.list_candidates(profile=profile, context=context, task_intent=task_intent):
                if candidate.name in seen:
                    continue
                candidates.append(candidate)
                seen.add(candidate.name)

        return candidates
