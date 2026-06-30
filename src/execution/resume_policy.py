from execution.models import Checkpoint

class ResumePolicy:
    def can_resume(self, checkpoint: Checkpoint | None) -> bool:
        return checkpoint is not None
