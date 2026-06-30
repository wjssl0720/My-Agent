from workspace.models import Workspace

class CleanupPolicy:
    def should_cleanup(self, workspace: Workspace) -> bool:
        return workspace.status in ("closed", "failed")
