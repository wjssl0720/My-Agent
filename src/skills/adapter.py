from skills.loader import LoadedSkill
from tools.tool_pack import ToolCandidate
class SkillAdapter:
    def to_prompt_block(self, skill: LoadedSkill) -> str:
        return f"## Skill: {skill.name}\n{skill.content}"
    def to_tool_candidate(self, skill: LoadedSkill) -> ToolCandidate | None:
        return None
