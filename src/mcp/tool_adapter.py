from mcp.schemas import McpToolSchema
from tools.tool_pack import ToolCandidate

class McpToolAdapter:
    def to_candidate(self, schema: McpToolSchema) -> ToolCandidate:
        return ToolCandidate(name=schema.name, description=schema.description, source="mcp", risk_level=schema.risk_level, metadata={"server_name": schema.server_name})
