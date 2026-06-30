class TimeoutPolicy:
    def __init__(self, default_seconds: int = 120) -> None:
        self.default_seconds = default_seconds

    def timeout_for(self, task_type: str | None = None) -> int:
        return self.default_seconds
