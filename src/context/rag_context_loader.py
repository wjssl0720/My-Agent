class RagContextLoader:
    async def load_pinned_context(self, source_ids: list[str]) -> list[dict]:
        return [{"source_id": source_id, "status": "not_loaded"} for source_id in source_ids]
