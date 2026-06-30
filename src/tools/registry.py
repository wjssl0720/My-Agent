from tools.enterprise.product_tools import GetSkuTool, SearchSimilarProductTool
from tools.enterprise.order_tools import GetOrderTool, RefundOrderTool
from tools.enterprise.bi_tools import RunReadonlySqlTool, GenerateReportTool
from tools.enterprise.rag_tools import RagSearchTool

class ToolRegistry:
    def __init__(self) -> None:
        tools = [
            RagSearchTool(),
            GetSkuTool(),
            SearchSimilarProductTool(),
            GetOrderTool(),
            RefundOrderTool(),
            RunReadonlySqlTool(),
            GenerateReportTool(),
        ]
        self._tools = {tool.spec.name: tool for tool in tools}

    @classmethod
    def default(cls) -> "ToolRegistry":
        return cls()

    def get(self, name: str):
        return self._tools[name]

    def list_tools(self) -> list[dict]:
        return [tool.spec.model_dump() for tool in self._tools.values()]
