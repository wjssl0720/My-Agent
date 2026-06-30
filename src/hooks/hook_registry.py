from collections import defaultdict
from typing import Awaitable, Callable
from hooks.hook_event import HookContext, HookPoint, HookResult

HookHandler = Callable[[HookContext], Awaitable[HookResult]]

class HookRegistry:
    def __init__(self) -> None:
        self._handlers: dict[HookPoint, list[tuple[str, HookHandler]]] = defaultdict(list)

    def register(self, point: HookPoint, name: str, handler: HookHandler) -> None:
        self._handlers[point].append((name, handler))

    def list_handlers(self, point: HookPoint) -> list[tuple[str, HookHandler]]:
        return self._handlers.get(point, [])
