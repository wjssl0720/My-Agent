from rag.acl_filter import RagAclFilter
from rag.citation import CitationBuilder
from rag.reranker import Reranker
from rag.schemas import RagQuery, RagSearchResult
from rag.vector_store import VectorStore
class RagService:
    def __init__(self, vector_store: VectorStore | None = None, acl_filter: RagAclFilter | None = None, reranker: Reranker | None = None, citation_builder: CitationBuilder | None = None) -> None:
        self.vector_store = vector_store or VectorStore()
        self.acl_filter = acl_filter or RagAclFilter()
        self.reranker = reranker or Reranker()
        self.citation_builder = citation_builder or CitationBuilder()
    @classmethod
    def default(cls) -> "RagService":
        return cls()
    async def search(self, query: RagQuery) -> RagSearchResult:
        chunks = await self.vector_store.search(query)
        chunks = self.acl_filter.filter(chunks, query.allowed_scopes)
        chunks = await self.reranker.rerank(chunks, query.query)
        citations = self.citation_builder.build(chunks)
        return RagSearchResult(query=query.query, chunks=chunks, citations=citations)
