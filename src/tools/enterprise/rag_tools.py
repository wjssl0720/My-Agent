from context.context_pack import ContextPack
from rag.schemas import RagQuery
from rag.service import RagService
from tools.base import ToolSpec
class RagSearchTool:
    spec = ToolSpec(name="rag.search", description="检索企业知识库，带 scope / ACL / citation", risk_level="low")
    def __init__(self, service: RagService | None = None) -> None:
        self.service = service or RagService.default()
    async def execute(self, args: dict, context: ContextPack) -> dict:
        result = await self.service.search(RagQuery(query=args.get("query", ""), top_k=args.get("top_k", 5), allowed_scopes=context.allowed_rag_scopes))
        return {"query": result.query, "chunks": [chunk.model_dump() for chunk in result.chunks], "citations": [citation.model_dump() for citation in result.citations], "source": "rag_service"}
