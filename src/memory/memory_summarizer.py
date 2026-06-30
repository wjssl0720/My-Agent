from memory.models import MemorySummary

class MemorySummarizer:
    # 当前是规则占位；生产可接 LLM 做结构化摘要。
    async def summarize(self, session_id: str, history: list[dict]) -> MemorySummary:
        facts = []
        decisions = []
        for item in history[-10:]:
            if "tool_calls" in item:
                facts.append(f"tool_calls={len(item.get('tool_calls', []))}")
        return MemorySummary(
            session_id=session_id,
            summary=f"Session {session_id} summary with {len(history)} records.",
            facts=facts,
            decisions=decisions,
            open_questions=[],
        )
