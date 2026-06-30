from pathlib import Path
from skills.manifest import SkillManifest
from skills.registry import SkillRegistry

class LoadedSkill:
    def __init__(self, name: str, content: str, manifest: SkillManifest) -> None:
        self.name = name
        self.content = content
        self.manifest = manifest
    def model_dump(self) -> dict:
        return {"name": self.name, "content": self.content, "manifest": self.manifest.model_dump()}

class SkillLoader:
    def __init__(self, registry: SkillRegistry | None = None, skills_root: Path | None = None) -> None:
        self.registry = registry or SkillRegistry.default()
        self.skills_root = skills_root or Path("skills")
    def load_one(self, name: str) -> LoadedSkill:
        manifest = self.registry.get(name)
        skill_file = self.skills_root / name / manifest.prompt_file
        content = skill_file.read_text(encoding="utf-8") if skill_file.exists() else manifest.description
        return LoadedSkill(name=name, content=content, manifest=manifest)
    def load_many(self, names: list[str]) -> list[LoadedSkill]:
        return [self.load_one(name) for name in names]
