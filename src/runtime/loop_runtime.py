from loop.loop_engine import AgentLoopEngine
from loop.model_policy import AgentScopeModelPolicy, LocalModelPolicy
from runtime.base import RuntimeInput, RuntimeOutput

class LoopRuntime:
    def __init__(self, model_policy_name: str = "local_harness") -> None:
        if model_policy_name == "agentscope":
            model_policy = AgentScopeModelPolicy()
        else:
            model_policy = LocalModelPolicy()
        self.engine = AgentLoopEngine(model_policy=model_policy)

    @classmethod
    def local_harness(cls) -> "LoopRuntime":
        return cls("local_harness")

    @classmethod
    def agentscope(cls) -> "LoopRuntime":
        return cls("agentscope")

    async def invoke(self, runtime_input: RuntimeInput) -> RuntimeOutput:
        return await self.engine.invoke(runtime_input)
