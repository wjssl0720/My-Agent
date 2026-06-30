from hooks.hook_event import HookContext, HookResult

async def post_tool_use_recorder(context: HookContext) -> HookResult:
    return HookResult(allowed=True, message="post_tool_use recorded")
