from agents.profiles import AgentProfile
from context.context_pack import ContextPack
from mcp.server_registry import McpServerRegistry
from mcp.tool_adapter import McpToolAdapter
from tools.tool_pack import ToolCandidate
class McpToolProvider:
    name = "mcp"
    def __init__(self, registry: McpServerRegistry | None = None, adapter: McpToolAdapter | None = None) -> None:
        self.registry = registry or McpServerRegistry.default()
        self.adapter = adapter or McpToolAdapter()
    async def list_candidates(self, *, profile: AgentProfile, context: ContextPack, task_intent: str | None) -> list[ToolCandidate]:
        schemas = await self.registry.list_tools(enabled_only=True)
        return [self.adapter.to_candidate(schema) for schema in schemas]
