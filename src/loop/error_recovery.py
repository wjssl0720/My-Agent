from loop.models import LoopState

class ErrorRecovery:
    def handle_error(self, state: LoopState, exc: Exception) -> None:
        state.add_event("loop.error", {"error": str(exc), "step": state.step})
        state.messages.append({"role": "observation", "content": f"ERROR: {exc}"})
