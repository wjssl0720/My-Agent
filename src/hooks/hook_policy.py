from hooks.hook_event import HookContext

class HookPolicy:
    def can_run(self, context: HookContext, hook_name: str) -> bool:
        return True
