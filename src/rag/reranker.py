from rag.schemas import RagChunk
class Reranker:
    async def rerank(self, chunks: list[RagChunk], query: str) -> list[RagChunk]:
        return sorted(chunks, key=lambda chunk: chunk.score, reverse=True)
