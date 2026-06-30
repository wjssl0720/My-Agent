class EmbeddingClient:
    async def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] for _ in texts]
