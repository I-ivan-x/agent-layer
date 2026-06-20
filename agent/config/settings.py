# agent/config/settings.py

from typing import Optional

from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Global settings for Agent Layer."""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application configuration
    APP_NAME: str = Field(default="Agent Layer")
    DEBUG: bool = Field(default=True)
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)

    # Agent configuration
    RETRIEVAL_MODE: str = Field(default="mock")  # mock / real
    USE_MOCK_LLM: bool = Field(default=True)
    DEFAULT_TOP_K: int = Field(default=5, ge=1, le=20)
    MIN_RETRIEVAL_SCORE: float = Field(default=0.0, ge=0.0, le=1.0)

    # Logger configuration
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE: Optional[str] = Field(default=None)

    # LLM configuration
    LLM_MODEL: str = Field(default="gpt-3.5-turbo")
    LLM_TEMPERATURE: float = Field(default=0.1)
    LLM_MAX_TOKENS: int = Field(default=2000)
    LLM_TIMEOUT: int = Field(default=30)

    # Tool Layer configuration
    TOOL_LAYER_IMPORT: str = Field(default="tool_layer")
    TOOL_LAYER_CLASS: str = Field(default="SearchTool")
    TOOL_LAYER_TIMEOUT: int = Field(default=10)

    @property
    def use_mock_retrieval(self) -> bool:
        """Whether to use mock retrieval."""
        return self.RETRIEVAL_MODE.lower() == "mock"

    @property
    def is_mock_mode(self) -> bool:
        """Whether the whole agent runs in mock mode."""
        return self.use_mock_retrieval and self.USE_MOCK_LLM

    @property
    def is_production(self) -> bool:
        """Whether the application is running in production mode."""
        return not self.DEBUG


settings = Settings()