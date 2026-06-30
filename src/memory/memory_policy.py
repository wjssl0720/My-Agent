from context.context_pack import ContextPack

class MemoryPolicy:
    # 决定什么时候读写长期记忆、什么时候压缩、哪些数据禁止沉淀。
    def should_load_long_term(self, context: ContextPack) -> bool:
        return True

    def should_write_long_term(self, context: ContextPack, item: dict) -> bool:
        return item.get("persistable", False)

    def should_compact(self, context: ContextPack, step: int) -> bool:
        return step > 0 and step % 5 == 0
