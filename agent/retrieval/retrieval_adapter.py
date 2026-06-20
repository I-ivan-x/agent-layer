# agent/retrieval/retrieval_adapter.py

from importlib import import_module
from typing import Any, Optional

from agent.config.settings import settings
from agent.errors.exceptions import RetrievalError
from agent.logger.logger import get_logger
from agent.retrieval.base import BaseRetriever
from agent.retrieval.mock_retrieval import MockRetrieval
from agent.schemas.retrieval import RetrievalResult
from agent.trace.trace_id import get_trace_id

logger = get_logger(__name__)


class RetrievalAdapter(BaseRetriever):
    """
    Unified retrieval adapter for Agent Layer.

    This adapter hides the difference between mock retrieval and real Tool Layer
    retrieval. It also normalizes all returned results into RetrievalResult.
    """

    def __init__(
        self,
        mode: Optional[str] = None,
        retriever: Optional[Any] = None,
    ) -> None:
        self.mode = (mode or settings.RETRIEVAL_MODE).lower()

        if retriever is not None:
            self.retriever = retriever
            logger.info("Using injected retriever")
            return

        if self.mode == "mock":
            self.retriever = MockRetrieval()
            logger.info("Using MockRetrieval")
        elif self.mode == "real":
            self.retriever = self._init_real_retriever()
            logger.info("Using real Tool Layer retriever")
        else:
            raise RetrievalError(f"Unsupported retrieval mode: {self.mode}")

    def _init_real_retriever(self) -> Any:
        """
        Initialize Tool Layer SearchTool dynamically.

        Expected Tool Layer contract:
            from tool_layer import SearchTool
            tool = SearchTool()
            tool.search(...)
        """
        try:
            module = import_module(settings.TOOL_LAYER_IMPORT)
            search_tool_class = getattr(module, settings.TOOL_LAYER_CLASS)
            return search_tool_class()
        except ImportError as exc:
            raise RetrievalError(f"Failed to import Tool Layer: {exc}") from exc
        except AttributeError as exc:
            raise RetrievalError(f"Tool Layer class not found: {exc}") from exc
        except Exception as exc:
            raise RetrievalError(f"Failed to initialize retriever: {exc}") from exc

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[dict] = None,
        mode: str = "hybrid",
        min_score: float = 0.0,
        trace_id: Optional[str] = None,
    ) -> list[RetrievalResult]:
        """
        Retrieve relevant chunks through mock retriever or Tool Layer.

        The method signature is aligned with the Tool Layer CP1 interface:
        query, top_k, mode, filters, min_score, trace_id.
        """
        if not query or not query.strip():
            raise RetrievalError("Query cannot be empty")

        actual_trace_id = trace_id or get_trace_id()

        logger.info(
            "[RETRIEVAL_ADAPTER] trace_id=%s mode=%s top_k=%s min_score=%s",
            actual_trace_id,
            mode,
            top_k,
            min_score,
        )

        try:
            raw_results = self._call_retriever(
                query=query,
                top_k=top_k,
                mode=mode,
                filters=filters,
                min_score=min_score,
                trace_id=actual_trace_id,
            )
            results = self._normalize_results(raw_results)

            logger.info(
                "[RETRIEVAL_ADAPTER] trace_id=%s results=%s",
                actual_trace_id,
                len(results),
            )
            return results

        except RetrievalError:
            raise
        except Exception as exc:
            logger.error(
                "[RETRIEVAL_ADAPTER] trace_id=%s failed: %s",
                actual_trace_id,
                exc,
                exc_info=True,
            )
            raise RetrievalError(f"Retrieval service unavailable: {exc}") from exc

    def _call_retriever(
        self,
        query: str,
        top_k: int,
        mode: str,
        filters: Optional[dict],
        min_score: float,
        trace_id: Optional[str],
    ) -> Any:
        """
        Call the underlying retriever.

        Real Tool Layer should provide search(...).
        MockRetriever may provide retrieve(...).
        """
        if hasattr(self.retriever, "search"):
            return self.retriever.search(
                query=query,
                top_k=top_k,
                mode=mode,
                filters=filters,
                min_score=min_score,
                trace_id=trace_id,
            )

        if hasattr(self.retriever, "retrieve"):
            return self.retriever.retrieve(
                query=query,
                top_k=top_k,
                mode=mode,
                filters=filters,
                min_score=min_score,
                trace_id=trace_id,
            )

        raise RetrievalError("Retriever must implement search() or retrieve()")

    def _normalize_results(self, results: Any) -> list[RetrievalResult]:
        """
        Normalize Tool Layer list[dict] results into list[RetrievalResult].
        """
        if results is None:
            return []

        if not isinstance(results, list):
            raise RetrievalError("Retrieval results must be a list")

        normalized_results: list[RetrievalResult] = []

        for item in results:
            if isinstance(item, RetrievalResult):
                normalized_results.append(item)
            elif isinstance(item, dict):
                normalized_results.append(RetrievalResult(**item))
            else:
                raise RetrievalError(
                    f"Invalid retrieval result item type: {type(item).__name__}"
                )

        return normalized_results