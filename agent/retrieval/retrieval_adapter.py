from typing import Optional

from agent.retrieval.base import BaseRetriever
from agent.retrieval.mock_retrieval import MockRetrieval
from agent.schemas.retrieval import RetrievalResult
from agent.config.settings import settings


class RetrievalAdapter(BaseRetriever):
    def __init__(self, retriever: Optional[BaseRetriever] = None) -> None:
        if retriever:
            self.retriever = retriever
        elif settings.USE_MOCK_RETRIEVAL:
            self.retriever = MockRetrieval()
        else:
            self.retriever = MockRetrieval()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[dict] = None,
        mode: str = "hybrid",  # 新增
    ) -> list[RetrievalResult]:
        return self.retriever.retrieve(
            query=query,
            top_k=top_k,
            filters=filters,
            mode=mode,  # 传递
        )