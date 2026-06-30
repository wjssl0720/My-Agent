from context.context_pack import ContextPack
from tools.base import ToolSpec

class GetSkuTool:
    spec = ToolSpec(name="product.get_sku", description="查询 SKU 商品基础信息", risk_level="low")

    async def execute(self, args: dict, context: ContextPack) -> dict:
        sku = args.get("sku", "Y28H23093T1")
        return {
            "sku": sku,
            "spu": "Y28H23093",
            "title": "示例商品：防泼水通勤双肩包",
            "category": "箱包",
            "selling_points": ["轻量", "防泼水", "大容量", "适合通勤"],
            "source": "mock_product_center",
        }

class SearchSimilarProductTool:
    spec = ToolSpec(name="product.search_similar", description="查询相似商品", risk_level="low")

    async def execute(self, args: dict, context: ContextPack) -> dict:
        return {
            "items": [
                {"sku": "Y28H23093T2", "similarity": 0.92},
                {"sku": "Y28H23093T3", "similarity": 0.88},
            ],
            "source": "mock_product_center",
        }
