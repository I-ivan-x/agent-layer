# agent/retrieval/retrieval_adapter.py
from typing import Optional, Dict, Any
from importlib import import_module

from agent.retrieval.base import BaseRetriever
from agent.retrieval.mock_retrieval import MockRetrieval
from agent.schemas.retrieval import RetrievalResult
from agent.config.settings import settings
from agent.logger.logger import get_logger
from agent.errors.exceptions import RetrievalError
from agent.trace.trace_id import get_trace_id

logger = get_logger(__name__)


class RetrievalAdapter(BaseRetriever):
    """
    Retrieval adapter that supports switching between Mock and Real retrieval modes.

    When USE_MOCK_RETRIEVAL is True, uses MockRetrieval.
    When False, uses the real SearchTool from the tool layer.
    """

    def __init__(self):
        if settings.USE_MOCK_RETRIEVAL:
            logger.info("Using Mock retrieval mode")
            self.retriever = MockRetrieval()
        else:
            logger.info("Using Real retrieval mode")
            self._init_real_retriever()

    def _init_real_retriever(self):
        """Initialize the real retriever from tool layer."""
        try:
            module = import_module(settings.TOOL_LAYER_IMPORT)
            search_tool_class = getattr(module, settings.TOOL_LAYER_CLASS)
            self.retriever = search_tool_class()
            logger.info("Real retriever initialized successfully from tool layer")
        except ImportError as e:
            logger.error(f"Failed to import tool layer: {e}")
            raise RetrievalError(f"Tool layer import failed: {e}")
        except Exception as e:
            logger.error(f"Failed to initialize real retriever: {e}")
            raise RetrievalError(f"Retriever initialization failed: {e}")

    def retrieve(
            self,
            query: str,
            top_k: int = 5,
            filters: Optional[Dict[str, Any]] = None,
            mode: str = "hybrid"
    ) -> list[RetrievalResult]:
        """
        Execute retrieval based on current mode.

        Args:
            query: User query string
            top_k: Number of results to return
            filters: Optional filter conditions
            mode: Retrieval mode (vector/bm25/hybrid)

        Returns:
            List of RetrievalResult objects

        Raises:
            RetrievalError: If retrieval fails
        """
        logger.info(f"Retrieval params: query={query[:50]}..., top_k={top_k}, mode={mode}")

        try:
            # Call tool layer search with trace_id
            results = self.retriever.search(
                query=query,
                top_k=top_k,
                mode=mode,
                filters=filters,
                trace_id=get_trace_id()
            )

            # Convert dict results to RetrievalResult if needed
            if results and isinstance(results[0], dict):
                results = [RetrievalResult(**r) for r in results]

            logger.info(f"Retrieval succeeded, returned {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            raise RetrievalError(f"Retrieval service unavailable: {e}")