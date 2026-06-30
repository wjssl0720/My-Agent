from hooks.hook_event import HookContext, HookResult

async def pre_model_call_guard(context: HookContext) -> HookResult:
    return HookResult(allowed=True, message="pre_model_call passed")
