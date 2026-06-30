from context.context_pack import ContextPack
from skills.manifest import SkillManifest
class SkillPolicy:
    def can_load(self, manifest: SkillManifest, context: ContextPack) -> bool:
        return manifest.enabled
