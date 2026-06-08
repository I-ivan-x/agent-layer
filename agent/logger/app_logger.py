import logging

from agent.config.settings import settings

logger = logging.getLogger("agent-layer")
logging.basicConfig(level=settings.LOG_LEVEL, format="%(asctime)s %(levelname)s %(message)s")


def log_chat_result(trace_id: str, query: str, retrieval_count: int, status: str) -> None:
    logger.info(
        "trace_id=%s query=%s retrieval_count=%s status=%s",
        trace_id,
        query,
        retrieval_count,
        status,
    )

