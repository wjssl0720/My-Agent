from rag.schemas import RagChunk, RagQuery
class VectorStore:
    async def search(self, query: RagQuery) -> list[RagChunk]:
        return [
            RagChunk(chunk_id="chunk_product_001", source_id="doc_product_001", title="商品导购手册", text="通勤双肩包主推卖点：轻量、防泼水、大容量、适合日常通勤。", scope="product_docs", score=0.92),
            RagChunk(chunk_id="chunk_operation_001", source_id="doc_operation_001", title="运营分析 SOP", text="分析转化下降时，需要检查曝光、点击率、价格、库存、评论和活动。", scope="operation_docs", score=0.88),
            RagChunk(chunk_id="chunk_finance_001", source_id="doc_finance_001", title="财务制度", text="财务资料示例。", scope="finance_docs", score=0.86),
        ][: query.top_k]
