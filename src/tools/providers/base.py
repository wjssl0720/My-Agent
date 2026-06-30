from typing import Protocol
from agents.profiles import AgentProfile
from context.context_pack import ContextPack
from tools.tool_pack import ToolCandidate

class ToolProvider(Protocol):
    name: str

    async def list_candidates(
        self,
        *,
        profile: AgentProfile,
        context: ContextPack,
        task_intent: str | None,
    ) -> list[ToolCandidate]:
        ...
