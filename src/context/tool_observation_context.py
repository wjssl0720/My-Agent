class ToolObservationContext:
    def summarize(self, tool_name: str, result: dict) -> dict:
        return {
            "tool_name": tool_name,
            "summary": str(result)[:1000],
            "raw_available_in_trace": True,
        }
