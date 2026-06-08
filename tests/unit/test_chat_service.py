from agent.llm.mock_llm import MockLLM
from agent.retrieval.mock_retrieval import MockRetrieval
from agent.schemas.chat import ChatRequest
from agent.schemas.common import StatusCode
from agent.service.chat_service import ChatService


def test_normal_query_returns_success() -> None:
    response = ChatService().chat(ChatRequest(query="项目 Q1 阶段需要完成哪些功能？"))

    assert response.status == StatusCode.SUCCESS
    assert response.answer
    assert response.citations
    assert response.trace_id.startswith("trace-")


def test_empty_query_returns_invalid_query() -> None:
    response = ChatService().chat(ChatRequest(query="   "))

    assert response.status == StatusCode.INVALID_QUERY
    assert response.answer == ""
    assert response.message == "请输入有效问题。"
    assert response.citations == []


def test_empty_retrieval_returns_no_relevant_context() -> None:
    service = ChatService(retriever=MockRetrieval(return_empty=True))

    response = service.chat(ChatRequest(query="知识库外问题"))

    assert response.status == StatusCode.NO_RELEVANT_CONTEXT
    assert response.answer == ""
    assert response.citations == []


def test_retrieval_error_returns_retrieval_error() -> None:
    service = ChatService(retriever=MockRetrieval(should_raise=True))

    response = service.chat(ChatRequest(query="触发检索异常"))

    assert response.status == StatusCode.RETRIEVAL_ERROR
    assert response.message == "检索服务暂时不可用，请稍后重试。"


def test_llm_error_returns_llm_error() -> None:
    service = ChatService(llm=MockLLM(should_raise=True))

    response = service.chat(ChatRequest(query="触发模型异常"))

    assert response.status == StatusCode.LLM_ERROR
    assert response.message == "模型服务暂时不可用，请稍后重试。"

