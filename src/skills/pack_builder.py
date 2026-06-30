from agents.profiles import AgentProfile
from context.context_pack import ContextPack
from skills.loader import LoadedSkill, SkillLoader
from skills.policy import SkillPolicy
class SkillPackBuilder:
    def __init__(self, loader: SkillLoader | None = None, policy: SkillPolicy | None = None) -> None:
        self.loader = loader or SkillLoader()
        self.policy = policy or SkillPolicy()
    def build(self, profile: AgentProfile, context: ContextPack) -> list[LoadedSkill]:
        loaded = []
        for skill_name in profile.skills:
            skill = self.loader.load_one(skill_name)
            if self.policy.can_load(skill.manifest, context):
                loaded.append(skill)
        return loaded
