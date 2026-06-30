from rag.schemas import RagChunk, RagCitation
class CitationBuilder:
    def build(self, chunks: list[RagChunk]) -> list[RagCitation]:
        return [RagCitation(source_id=chunk.source_id, title=chunk.title, chunk_id=chunk.chunk_id) for chunk in chunks]
