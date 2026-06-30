from mcp_servers.base_server import BaseMcpServer
class RagMcpServer(BaseMcpServer):
    name = "rag"
    async def list_tools(self) -> list[dict]:
        return [{"name": "rag.search", "description": "检索企业知识库"}]
