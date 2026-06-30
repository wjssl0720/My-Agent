from loop.models import LoopState
from context.context_window import ContextWindow

class ContextCompactor:
    # Loop 内部轻量 compactor。生产级接口在 context/context_compactor.py。
    def __init__(self, compact_after_steps: int = 5, window: ContextWindow | None = None) -> None:
        self.compact_after_steps = compact_after_steps
        self.window = window or ContextWindow(keep_recent_messages=6)

    def maybe_compact(self, state: LoopState) -> None:
        if state.step > 0 and state.step % self.compact_after_steps == 0:
            kept = self.window.select_messages(state.messages)
            state.messages = kept
            state.add_event("context.compacted", {"kept_messages": len(kept), "step": state.step})
