from typing import Any
from context.context_budget import ContextBudget

class ContextWindow:
    # 选择进入模型上下文的消息窗口；生产可接 tokenizer 做精确预算。
    def __init__(self, budget: ContextBudget | None = None, keep_recent_messages: int = 8) -> None:
        self.budget = budget or ContextBudget()
        self.keep_recent_messages = keep_recent_messages

    def select_messages(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return messages[-self.keep_recent_messages:]
