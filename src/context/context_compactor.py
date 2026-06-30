from context.context_summary import ContextSummary

class ProductionContextCompactor:
    # 生产级上下文压缩器接口。当前规则占位，后续可接 LLM。
    async def compact(
        self,
        *,
        task_goal: str,
        messages: list[dict],
        tool_calls: list[dict],
        citations: list[dict],
    ) -> ContextSummary:
        return ContextSummary(
            task_goal=task_goal,
            completed_steps=[f"message_count={len(messages)}", f"tool_call_count={len(tool_calls)}"],
            key_facts=[],
            decisions=[],
            citations=citations,
            open_questions=[],
            next_steps=[],
        )
