from typing import Optional

from pydantic import BaseModel


class RetrievalResult(BaseModel):
    doc_id: str
    chunk_id: str
    chunk_index: Optional[int] = None
    chunk_text: str
    title: str
    source_url: Optional[str] = None
    score: float
