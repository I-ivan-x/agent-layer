from typing import Any, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    top_k: int = Field(default=5, ge=1)
    filters: dict[str, Any] = Field(default_factory=dict)
    stream: bool = False


class Citation(BaseModel):
    citation_id: int
    title: str
    source_url: Optional[str] = None
    doc_id: str
    chunk_id: str
    score: Optional[float] = None
    snippet: Optional[str] = None


class ChatResponse(BaseModel):
    trace_id: str
    status: str
    answer: str
    message: str
    citations: list[Citation]
