from agents.profiles import AgentProfile
from context.context_pack import ContextPack
from tools.tool_pack import ToolCandidate

class RagToolProvider:
    name = "rag"

    async def list_candidates(
        self,
        *,
        profile: AgentProfile,
        context: ContextPack,
        task_intent: str | None,
    ) -> list[ToolCandidate]:
        if "rag.search" not in profile.tools:
            return []
        return [
            ToolCandidate(
                name="rag.search",
                description="检索企业知识库，带 scope / ACL / citation",
                source="rag",
                risk_level="low",
                metadata={"allowed_scopes": context.allowed_rag_scopes},
            )
        ]
