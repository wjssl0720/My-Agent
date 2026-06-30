from hooks.hook_event import HookContext, HookResult

async def on_error_recorder(context: HookContext) -> HookResult:
    return HookResult(allowed=True, message="error recorded")
