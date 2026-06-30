from hooks.hook_event import HookContext, HookResult
from hooks.hook_policy import HookPolicy
from hooks.hook_registry import HookRegistry

class HookRunner:
    def __init__(self, registry: HookRegistry | None = None, policy: HookPolicy | None = None) -> None:
        self.registry = registry or HookRegistry()
        self.policy = policy or HookPolicy()

    async def run(self, context: HookContext) -> list[HookResult]:
        results: list[HookResult] = []
        for name, handler in self.registry.list_handlers(context.hook_point):
            if not self.policy.can_run(context, name):
                continue
            result = await handler(context)
            results.append(result)
            if not result.allowed:
                break
        return results
