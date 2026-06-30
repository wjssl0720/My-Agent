from context.context_pack import ContextPack
from tools.base import ToolSpec

class GetOrderTool:
    spec = ToolSpec(name="order.get_order", description="查询订单", risk_level="medium")

    async def execute(self, args: dict, context: ContextPack) -> dict:
        return {
            "order_id": args.get("order_id", "O001"),
            "status": "paid",
            "days_after_purchase": 8,
            "source": "mock_oms",
        }

class RefundOrderTool:
    spec = ToolSpec(name="order.refund", description="发起退款，需要 HITL", risk_level="high")

    async def execute(self, args: dict, context: ContextPack) -> dict:
        return {
            "order_id": args.get("order_id", "O001"),
            "status": "refund_submitted",
            "source": "mock_oms",
        }
