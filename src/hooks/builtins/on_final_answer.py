from hooks.hook_event import HookContext, HookResult

async def on_final_answer_recorder(context: HookContext) -> HookResult:
    return HookResult(allowed=True, message="final answer recorded")
