from mcp_servers.base_server import BaseMcpServer
class ProductMcpServer(BaseMcpServer):
    name = "product"
    async def list_tools(self) -> list[dict]:
        return [{"name": "product.get_sku", "description": "查询 SKU 商品信息"}, {"name": "product.search_similar", "description": "查询相似商品"}]
