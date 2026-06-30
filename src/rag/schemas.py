from pydantic import BaseModel, Field
class RagQuery(BaseModel):
    query: str
    top_k: int = 5
    allowed_scopes: list[str] = Field(default_factory=list)
class RagChunk(BaseModel):
    chunk_id: str
    source_id: str
    title: str
    text: str
    scope: str
    score: float = 1.0
    metadata: dict = Field(default_factory=dict)
class RagCitation(BaseModel):
    source_id: str
    title: str
    chunk_id: str
class RagSearchResult(BaseModel):
    query: str
    chunks: list[RagChunk] = Field(default_factory=list)
    citations: list[RagCitation] = Field(default_factory=list)
