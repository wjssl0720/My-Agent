from rag.schemas import RagChunk
class RagAclFilter:
    def filter(self, chunks: list[RagChunk], allowed_scopes: list[str]) -> list[RagChunk]:
        scopes = set(allowed_scopes)
        return [chunk for chunk in chunks if chunk.scope in scopes]
