from mcp.schemas import McpServerConfig

class McpAuthProvider:
    def build_headers(self, server: McpServerConfig) -> dict[str, str]:
        return dict(server.headers)
