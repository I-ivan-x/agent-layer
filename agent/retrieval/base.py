from abc import ABC, abstractmethod
from typing import Optional

from agent.schemas.retrieval import RetrievalResult


class BaseRetriever(ABC):
    @abstractmethod
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[dict] = None,
        mode: str = "hybrid",
        min_score: float = 0.0,
        trace_id: Optional[str] = None,
    ) -> list[RetrievalResult]:
        raise NotImplementedError
