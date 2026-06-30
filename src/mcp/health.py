from mcp.server_registry import McpServerRegistry

class McpHealthChecker:
    def __init__(self, registry: McpServerRegistry | None = None) -> None:
        self.registry = registry or McpServerRegistry.default()

    async def check(self) -> list[dict]:
        return [{"server": server.name, "enabled": server.enabled, "status": "not_checked"} for server in self.registry.list_servers(enabled_only=False)]
