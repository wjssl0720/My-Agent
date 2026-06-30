from pydantic import BaseModel

class ContextBudget(BaseModel):
    max_input_tokens: int = 24000
    reserve_output_tokens: int = 4000
    reserve_tool_tokens: int = 4000

    @property
    def usable_input_tokens(self) -> int:
        return max(0, self.max_input_tokens - self.reserve_output_tokens - self.reserve_tool_tokens)
