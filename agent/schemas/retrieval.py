# agent/schemas/retrieval.py

from typing import Optional

from pydantic import BaseModel, Field


class RetrievalResult(BaseModel):
    """Standard retrieval result returned to Agent Layer."""

    doc_id: str
    chunk_id: str
    chunk_index: int
    chunk_text: str
    title: str
    score: float = Field(ge=0.0, le=1.0)
    source_url: Optional[str] = ""