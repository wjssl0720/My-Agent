from agents.profiles import AgentRegistry
from core.errors import ApprovalRequired, ToolPermissionDenied
from core.models import Citation, ToolCallRecord
from loop.context_assembler import ContextAssembler
from loop.context_compactor import ContextCompactor
from loop.error_recovery import ErrorRecovery
from loop.model_policy import ModelPolicy
from loop.models import LoopState
from loop.prompt_builder import SystemPromptBuilder
from loop.skill_loader import SkillLoader
from loop.stop_policy import StopPolicy
from loop.subagent_manager import SubAgentManager
from loop.task_planner import TaskPlanner
from loop.tool_resolver import ToolResolver
from runtime.base import RuntimeInput, RuntimeOutput
from tools.gateway import ToolGateway

class AgentLoopEngine:
    def __init__(
        self,
        model_policy: ModelPolicy,
        tool_gateway: ToolGateway | None = None,
        agent_registry: AgentRegistry | None = None,
    ) -> None:
        self.model_policy = model_policy
        self.tool_gateway = tool_gateway or ToolGateway.default()
        self.agent_registry = agent_registry or AgentRegistry.default()
        self.context_assembler = ContextAssembler()
        self.tool_resolver = ToolResolver()
        self.skill_loader = SkillLoader()
        self.task_planner = TaskPlanner()
        self.prompt_builder = SystemPromptBuilder()
        self.subagent_manager = SubAgentManager(tool_gateway=self.tool_gateway)
        self.context_compactor = ContextCompactor()
        self.stop_policy = StopPolicy()
        self.error_recovery = ErrorRecovery()

    async def invoke(self, runtime_input: RuntimeInput) -> RuntimeOutput:
        profile = self.agent_registry.get(runtime_input.agent_id)
        assembled_context = self.context_assembler.assemble(profile, runtime_input.context, runtime_input.message)
        tools = self.tool_resolver.resolve(profile, runtime_input.context)
        skills = self.skill_loader.load(profile, runtime_input.message, runtime_input.context)
        task_plan = self.task_planner.plan(profile, runtime_input.message)
        system_prompt = self.prompt_builder.build(
            profile=profile,
            context=runtime_input.context,
            tools=tools,
            skills=skills,
            task_plan=task_plan,
        )

        state = LoopState(
            message=runtime_input.message,
            agent_id=runtime_input.agent_id,
            context=runtime_input.context,
            system_prompt=system_prompt,
            available_tools=tools,
            loaded_skills=skills,
            task_plan=task_plan,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": runtime_input.message},
            ],
        )
        state.add_event("prompt.built", {"length": len(system_prompt)})
        state.add_event("context.assembled", assembled_context)
        state.add_event("tools.resolved", {"tools": [t.model_dump() for t in tools]})
        state.add_event("skills.loaded", {"skills": [s.name for s in skills]})
        state.add_event("task.planned", task_plan.model_dump())

        while not self.stop_policy.should_stop(state):
            try:
                action = await self.model_policy.next_action(state)
                state.add_event("loop.action", action.model_dump())

                if action.action_type == "final":
                    state.final_answer = action.content or "已完成。"
                    break

                if action.action_type == "tool":
                    await self._execute_tool_action(state, action.tool_name or "", action.tool_args)

                if action.action_type == "subagent":
                    await self._execute_subagent_action(state, action.subagent_name or "", action.subtask or "")

                state.step += 1
                self.context_compactor.maybe_compact(state)

            except Exception as exc:
                self.error_recovery.handle_error(state, exc)
                state.final_answer = f"执行过程中发生错误：{exc}"
                break

        return RuntimeOutput(
            answer=state.final_answer or "已完成，但没有生成最终回答。",
            tool_calls=state.tool_calls,
            citations=state.citations,
            events=state.events,
        )

    async def _execute_tool_action(self, state: LoopState, tool_name: str, args: dict) -> None:
        call = ToolCallRecord(tool_name=tool_name, arguments=args, status="planned")
        try:
            result = await self.tool_gateway.execute(tool_name=tool_name, args=args, context=state.context)
            call.status = "executed"
            call.result = result
            if tool_name == "rag.search":
                for citation in result.get("citations", []):
                    state.citations.append(Citation(**citation))
            state.messages.append({"role": "tool_result", "tool_name": tool_name, "content": result})
            state.add_event("tool.executed", {"tool_name": tool_name, "result": result})
        except ApprovalRequired as exc:
            call.status = "approval_required"
            call.reason = exc.reason
            call.result = {"approval_required": True}
            state.messages.append({"role": "tool_result", "tool_name": tool_name, "content": call.result})
            state.add_event("tool.approval_required", {"tool_name": tool_name, "reason": exc.reason})
        except ToolPermissionDenied as exc:
            call.status = "denied"
            call.reason = str(exc)
            call.result = {"denied": True}
            state.messages.append({"role": "tool_result", "tool_name": tool_name, "content": call.result})
            state.add_event("tool.denied", {"tool_name": tool_name, "reason": str(exc)})
        state.tool_calls.append(call)

    async def _execute_subagent_action(self, state: LoopState, subagent_name: str, subtask: str) -> None:
        state.add_event("subagent.dispatched", {"subagent_name": subagent_name, "subtask": subtask})
        result, calls = await self.subagent_manager.run_subagent(subagent_name, subtask, state.context)
        state.tool_calls.extend(calls)
        for call in calls:
            if call.tool_name == "rag.search" and isinstance(call.result, dict):
                for citation in call.result.get("citations", []):
                    state.citations.append(Citation(**citation))
        state.messages.append({"role": "subagent_result", "name": subagent_name, "content": result})
        state.add_event("subagent.completed", {"subagent_name": subagent_name, "result": result})
