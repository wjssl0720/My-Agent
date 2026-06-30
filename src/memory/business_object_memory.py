from collections import defaultdict
from typing import Any

class BusinessObjectMemory:
    # SPU/SKU/订单/门店/客户等业务对象记忆。
    def __init__(self) -> None:
        self._store: dict[str, list[dict[str, Any]]] = defaultdict(list)

    async def load(self, object_key: str) -> list[dict[str, Any]]:
        return self._store.get(object_key, [])

    async def append(self, object_key: str, item: dict[str, Any]) -> None:
        self._store[object_key].append(item)
