from typing import Protocol
from loop.models import LoopAction, LoopState

class ModelPolicy(Protocol):
    async def next_action(self, state: LoopState) -> LoopAction:
        ...

class LocalModelPolicy:
    async def next_action(self, state: LoopState) -> LoopAction:
        message = state.message.lower()
        executed = {c.tool_name for c in state.tool_calls if c.status in ("executed", "denied", "approval_required")}
        dispatched = {
            event.payload.get("subagent_name")
            for event in state.events
            if event.type == "subagent.completed"
        }

        if state.task_plan.is_complex:
            for task in state.task_plan.tasks:
                if task.assignee and task.assignee not in dispatched:
                    return LoopAction(action_type="subagent", subagent_name=task.assignee, subtask=task.description)
            return LoopAction(action_type="final", content=self._final_answer(state))

        if "退款" in message or "refund" in message:
            if "order.refund" not in executed:
                return LoopAction(action_type="tool", tool_name="order.refund", tool_args={"order_id": "O001", "reason": "客服承诺退款"})
            return LoopAction(action_type="final", content=self._final_answer(state))

        if "报表" in message or "销售" in message or "sql" in message:
            if "bi.run_readonly_sql" not in executed:
                return LoopAction(action_type="tool", tool_name="bi.run_readonly_sql", tool_args={"sql": "select current_date as dt, 1 as mock_value"})
            return LoopAction(action_type="final", content=self._final_answer(state))

        if "sku" in message or "商品" in message or "导购" in message:
            if "product.get_sku" not in executed:
                return LoopAction(action_type="tool", tool_name="product.get_sku", tool_args={"sku": "Y28H23093T1"})
            if "rag.search" not in executed:
                return LoopAction(action_type="tool", tool_name="rag.search", tool_args={"query": state.message})
            return LoopAction(action_type="final", content=self._final_answer(state))

        if "rag.search" not in executed:
            return LoopAction(action_type="tool", tool_name="rag.search", tool_args={"query": state.message})
        return LoopAction(action_type="final", content=self._final_answer(state))

    def _final_answer(self, state: LoopState) -> str:
        lines = ["已完成 Agent Loop 执行。", "", "执行摘要："]
        for call in state.tool_calls:
            lines.append(f"- tool={call.tool_name}, status={call.status}")
        for event in state.events:
            if event.type == "subagent.completed":
                lines.append(f"- subagent={event.payload.get('subagent_name')} completed")
        return "\n".join(lines)

class AgentScopeModelPolicy:
    async def next_action(self, state: LoopState) -> LoopAction:
        try:
            import agentscope  # noqa: F401
        except ImportError as exc:
            raise RuntimeError("AgentScope 未安装。生产环境请执行 pip install -e '.[agentscope]'。") from exc

        raise NotImplementedError(
            "请在锁定 AgentScope 2.x 版本后，实现 AgentScope event/tool_use 到 LoopAction 的适配。"
        )
