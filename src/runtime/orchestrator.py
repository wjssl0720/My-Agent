from context.caller_context import CallerContext
from context.manager import ContextManager
from core.models import SendMessageRequest, SendMessageResponse
from core.settings import settings
from memory.memory_service import MemoryService
from observability.tracing import TraceRecorder
from runtime.base import RuntimeInput
from runtime.loop_runtime import LoopRuntime

class AgentOrchestrator:
    def __init__(
        self,
        runtime: LoopRuntime,
        context_manager: ContextManager | None = None,
        memory: MemoryService | None = None,
        trace: TraceRecorder | None = None,
    ) -> None:
        self.runtime = runtime
        self.context_manager = context_manager or ContextManager()
        self.memory = memory or MemoryService.default()
        self.trace = trace or TraceRecorder()

    @classmethod
    def default_for_api(cls) -> "AgentOrchestrator":
        if settings.runtime_model_policy == "agentscope":
            return cls(runtime=LoopRuntime.agentscope())
        return cls(runtime=LoopRuntime.local_harness())

    @classmethod
    def default_for_verification(cls) -> "AgentOrchestrator":
        return cls(runtime=LoopRuntime.local_harness())

    async def invoke(self, *, session_id: str, req: SendMessageRequest, caller: CallerContext) -> SendMessageResponse:
        trace_id = self.trace.start_trace(user_id=caller.user_id, session_id=session_id, agent_id=req.agent_id)
        memory_state = await self.memory.load(session_id=session_id)
        context = self.context_manager.build(
            caller=caller,
            session_id=session_id,
            agent_id=req.agent_id,
            file_ids=req.file_ids,
            short_term_memory=memory_state,
        )
        output = await self.runtime.invoke(RuntimeInput(message=req.message, agent_id=req.agent_id, context=context))
        await self.memory.append(
            session_id=session_id,
            item={
                "user": req.message,
                "assistant": output.answer,
                "tool_calls": [t.model_dump() for t in output.tool_calls],
            },
        )
        self.trace.add_event(trace_id, "agent.completed", {
            "agent_id": req.agent_id,
            "tool_calls": [t.model_dump() for t in output.tool_calls],
            "events": [e.model_dump() for e in output.events],
        })
        return SendMessageResponse(
            answer=output.answer,
            session_id=session_id,
            agent_id=req.agent_id,
            tool_calls=output.tool_calls,
            citations=output.citations,
            trace_id=trace_id,
            events=output.events,
        )
