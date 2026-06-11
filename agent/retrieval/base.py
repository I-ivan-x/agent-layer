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
        mode: str = "hybrid",  # 新增
    ) -> list[RetrievalResult]:
        raise NotImplementedError