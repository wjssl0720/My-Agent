from mcp.auth import McpAuthProvider
from mcp.schemas import McpCallRequest, McpCallResult, McpServerConfig, McpToolSchema

class McpClient:
    def __init__(self, auth_provider: McpAuthProvider | None = None) -> None:
        self.auth_provider = auth_provider or McpAuthProvider()

    async def list_tools(self, server: McpServerConfig) -> list[McpToolSchema]:
        return [
            McpToolSchema(name=tool_name, description=f"MCP tool from {server.name}: {tool_name}", server_name=server.name)
            for tool_name in server.tools
        ]

    async def call_tool(self, server: McpServerConfig, request: McpCallRequest) -> McpCallResult:
        return McpCallResult(server_name=server.name, tool_name=request.tool_name, result={"status": "mock_mcp_result", "arguments": request.arguments})
