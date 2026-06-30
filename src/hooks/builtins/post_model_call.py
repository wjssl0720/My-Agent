from hooks.hook_event import HookContext, HookResult

async def post_model_call_recorder(context: HookContext) -> HookResult:
    return HookResult(allowed=True, message="post_model_call recorded")
