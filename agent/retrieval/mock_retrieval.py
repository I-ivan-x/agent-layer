from typing import Optional

from agent.retrieval.base import BaseRetriever
from agent.schemas.retrieval import RetrievalResult


class MockRetrieval(BaseRetriever):
    def __init__(self, return_empty: bool = False, should_raise: bool = False) -> None:
        self.return_empty = return_empty
        self.should_raise = should_raise

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[dict] = None,
        mode: str = "hybrid",  # 新增，Mock 阶段暂不使用
    ) -> list[RetrievalResult]:
        if self.should_raise:
            raise RuntimeError("mock retrieval error")
        if self.return_empty:
            return []

        results = [
            RetrievalResult(
                doc_id="agent-q1-plan",
                chunk_id="chunk-001",
                title="Agent 层 Q1 范围",
                source_url="https://example.local/docs/agent-q1-plan",
                score=0.96,
                chunk_text="Q1 只实现简化版单轮 RAG Agent，使用 Mock Retrieval 和 Mock LLM 打通最小闭环。",
            ),
            RetrievalResult(
                doc_id="agent-interface-contract",
                chunk_id="chunk-002",
                title="Web-Agent 接口契约",
                source_url="https://example.local/docs/interface-contract",
                score=0.91,
                chunk_text="/api/chat 返回 trace_id、status、answer、message 和 citations，普通 JSON 响应是 Q1 保底能力。",
            ),
            RetrievalResult(
                doc_id="agent-work-division",
                chunk_id="chunk-003",
                title="两人协作分工",
                source_url="https://example.local/docs/division-of-work",
                score=0.88,
                chunk_text="xdj 负责 Agent 主流程，lhf 负责基础设施、检索适配、日志、trace、配置、错误和测试。",
            ),
        ]
        return results[:top_k]