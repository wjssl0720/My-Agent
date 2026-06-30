from loop.models import LoopState

class StopPolicy:
    def __init__(self, max_steps: int = 8) -> None:
        self.max_steps = max_steps

    def should_stop(self, state: LoopState) -> bool:
        if state.final_answer:
            return True
        if state.step >= self.max_steps:
            state.final_answer = "任务已达到最大执行步数，已基于当前观察结果给出阶段性结论。"
            state.add_event("loop.max_steps_reached", {"max_steps": self.max_steps})
            return True
        return False
