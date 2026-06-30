from mcp_servers.base_server import BaseMcpServer
class BiMcpServer(BaseMcpServer):
    name = "bi"
    async def list_tools(self) -> list[dict]:
        return [{"name": "bi.run_readonly_sql", "description": "执行只读 SQL"}, {"name": "bi.generate_report", "description": "生成报表"}]
