class FileContextLoader:
    async def load(self, file_ids: list[str]) -> list[dict]:
        return [{"file_id": file_id, "status": "not_loaded"} for file_id in file_ids]
