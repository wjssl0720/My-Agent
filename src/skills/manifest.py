from pydantic import BaseModel, Field

class SkillManifest(BaseModel):
    name: str
    version: str = "0.1.0"
    description: str = ""
    owner: str = "platform"
    enabled: bool = True
    tags: list[str] = Field(default_factory=list)
    required_tools: list[str] = Field(default_factory=list)
    prompt_file: str = "SKILL.md"
