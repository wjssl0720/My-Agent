from mcp_servers.base_server import BaseMcpServer
class OrderMcpServer(BaseMcpServer):
    name = "order"
    async def list_tools(self) -> list[dict]:
        return [{"name": "order.get_order", "description": "查询订单"}, {"name": "order.refund", "description": "发起退款"}]
