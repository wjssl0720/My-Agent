from hooks.hook_event import HookContext, HookResult

async def pre_tool_use_guard(context: HookContext) -> HookResult:
    return HookResult(allowed=True, message="pre_tool_use passed")
