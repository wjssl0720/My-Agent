from mcp.client import McpClient
from mcp.config_loader import McpConfigLoader
from mcp.schemas import McpServerConfig, McpToolSchema

class McpServerRegistry:
    def __init__(self, loader: McpConfigLoader | None = None, client: McpClient | None = None) -> None:
        self.loader = loader or McpConfigLoader()
        self.client = client or McpClient()
        self._servers = {server.name: server for server in self.loader.load()}

    @classmethod
    def default(cls) -> "McpServerRegistry":
        return cls()

    def list_servers(self, enabled_only: bool = True) -> list[McpServerConfig]:
        servers = list(self._servers.values())
        if enabled_only:
            servers = [server for server in servers if server.enabled]
        return servers

    async def list_tools(self, enabled_only: bool = True) -> list[McpToolSchema]:
        tools: list[McpToolSchema] = []
        for server in self.list_servers(enabled_only=enabled_only):
            tools.extend(await self.client.list_tools(server))
        return tools

    def get_server(self, name: str) -> McpServerConfig:
        return self._servers[name]
