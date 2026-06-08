from pydantic import BaseModel


class Settings(BaseModel):
    USE_MOCK_RETRIEVAL: bool = True
    USE_MOCK_LLM: bool = True
    DEFAULT_TOP_K: int = 5
    MIN_RETRIEVAL_SCORE: float = 0.0
    LOG_LEVEL: str = "INFO"


settings = Settings()

