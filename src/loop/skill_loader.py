from agents.profiles import AgentProfile
from loop.models import LoadedSkill
from context.context_pack import ContextPack
from skills.pack_builder import SkillPackBuilder
class SkillLoader:
    def __init__(self, pack_builder: SkillPackBuilder | None = None) -> None:
        self.pack_builder = pack_builder or SkillPackBuilder()
    def load(self, profile: AgentProfile, message: str, context: ContextPack | None = None) -> list[LoadedSkill]:
        if context is None:
            return [LoadedSkill(name=name, content=f"Skill: {name}") for name in profile.skills]
        skills = self.pack_builder.build(profile, context)
        return [LoadedSkill(name=skill.name, content=skill.content) for skill in skills]
