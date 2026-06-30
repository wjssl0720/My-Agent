from context.context_pack import ContextPack
from core.models import ToolCallRecord
from core.errors import ApprovalRequired, ToolPermissionDenied
from agents.subagents import SubAgentRegistry
from tools.gateway import ToolGateway

class SubAgentManager:
    def __init__(
        self,
        registry: SubAgentRegistry | None = None,
        tool_gateway: ToolGateway | None = None,
    ) -> None:
        self.registry = registry or SubAgentRegistry.default()
        self.tool_gateway = tool_gateway or ToolGateway.default()

    async def run_subagent(self, subagent_name: str, subtask: str, context: ContextPack) -> tuple[dict, list[ToolCallRecord]]:
        profile = self.registry.get(subagent_name)
        tool_calls: list[ToolCallRecord] = []
        observations = []

        for tool_name, args in self._plan_tools_for_subagent(subagent_name, subtask):
            call = ToolCallRecord(tool_name=tool_name, arguments=args, status="planned")
            try:
                result = await self.tool_gateway.execute(tool_name=tool_name, args=args, context=context)
                call.status = "executed"
                call.result = result
                observations.append({"tool": tool_name, "result": result})
            except ApprovalRequired as exc:
                call.status = "approval_required"
                call.reason = exc.reason
                call.result = {"approval_required": True}
                observations.append({"tool": tool_name, "approval_required": True})
            except ToolPermissionDenied as exc:
                call.status = "denied"
                call.reason = str(exc)
                call.result = {"denied": True}
                observations.append({"tool": tool_name, "denied": True})
            tool_calls.append(call)

        result = {
            "subagent_name": subagent_name,
            "role": profile.role,
            "subtask": subtask,
            "observations": observations,
            "summary": f"{subagent_name} completed subtask: {subtask}",
        }
        return result, tool_calls

    def _plan_tools_for_subagent(self, subagent_name: str, subtask: str) -> list[tuple[str, dict]]:
        if subagent_name == "product_subagent":
            return [("product.get_sku", {"sku": "Y28H23093T1"})]
        if subagent_name == "rag_subagent":
            return [("rag.search", {"query": subtask})]
        if subagent_name == "data_subagent":
            return [("bi.run_readonly_sql", {"sql": "select current_date as dt, 1 as conversion_drop_mock"})]
        if subagent_name == "order_subagent":
            return [("order.get_order", {"order_id": "O001"})]
        if subagent_name == "report_subagent":
            return [("bi.generate_report", {"topic": subtask})]
        return []
