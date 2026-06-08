from agent.retrieval.mock_retrieval import MockRetrieval
from agent.retrieval.retrieval_adapter import RetrievalAdapter


def test_retrieval_adapter_wraps_mock_retrieval() -> None:
    adapter = RetrievalAdapter(retriever=MockRetrieval())

    results = adapter.retrieve(query="测试", top_k=2)

    assert len(results) == 2
    assert results[0].doc_id

