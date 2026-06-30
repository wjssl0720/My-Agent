from mcp.schemas import McpServerConfig

class McpConfigLoader:
    def load(self) -> list[McpServerConfig]:
        return [
            McpServerConfig(name="product", enabled=False, base_url="http://product-mcp.local", auth_type="internal_token", tools=["product.get_sku", "product.search_similar"]),
            McpServerConfig(name="order", enabled=False, base_url="http://order-mcp.local", auth_type="internal_token", tools=["order.get_order", "order.refund"]),
        ]
