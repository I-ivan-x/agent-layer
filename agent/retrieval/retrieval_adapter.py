from typing import Optional

from agent.retrieval.base import BaseRetriever
from agent.retrieval.mock_retrieval import MockRetrieval
from agent.schemas.retrieval import RetrievalResult


class RetrievalAdapter(BaseRetriever):
    def __init__(self, retriever: BaseRetriever | None = None) -> None:
        self.retriever = retriever or MockRetrieval()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[dict] = None,
    ) -> list[RetrievalResult]:
        # TODO: 后续在这里接入真实 Tool Layer。Q1 不连接 Milvus、BM25 或 embedding API。
        return self.retriever.retrieve(query=query, top_k=top_k, filters=filters)

