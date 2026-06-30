from collections import defaultdict
from typing import Awaitable, Callable
from events.event_schema import AgentEvent

Subscriber = Callable[[AgentEvent], Awaitable[None]]

class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Subscriber]] = defaultdict(list)

    def subscribe(self, event_type: str, subscriber: Subscriber) -> None:
        self._subscribers[event_type].append(subscriber)

    async def publish(self, event: AgentEvent) -> None:
        subscribers = self._subscribers.get(event.event_type, []) + self._subscribers.get("*", [])
        for subscriber in subscribers:
            await subscriber(event)
