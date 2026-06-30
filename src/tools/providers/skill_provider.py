from agents.profiles import AgentProfile
from context.context_pack import ContextPack
from skills.adapter import SkillAdapter
from skills.pack_builder import SkillPackBuilder
from tools.tool_pack import ToolCandidate
class SkillToolProvider:
    name = "skill"
    def __init__(self, pack_builder: SkillPackBuilder | None = None, adapter: SkillAdapter | None = None) -> None:
        self.pack_builder = pack_builder or SkillPackBuilder()
        self.adapter = adapter or SkillAdapter()
    async def list_candidates(self, *, profile: AgentProfile, context: ContextPack, task_intent: str | None) -> list[ToolCandidate]:
        candidates: list[ToolCandidate] = []
        for skill in self.pack_builder.build(profile, context):
            candidate = self.adapter.to_tool_candidate(skill)
            if candidate is not None:
                candidates.append(candidate)
        return candidates
