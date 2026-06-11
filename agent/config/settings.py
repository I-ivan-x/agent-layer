# agent/config/settings.py
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # 应用配置
    APP_NAME: str = Field(default="Agent Layer")
    DEBUG: bool = Field(default=True)
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    
    # Agent 配置
    USE_MOCK_RETRIEVAL: bool = Field(default=True)
    USE_MOCK_LLM: bool = Field(default=True)
    DEFAULT_TOP_K: int = Field(default=5, ge=1, le=20)
    MIN_RETRIEVAL_SCORE: float = Field(default=0.0, ge=0.0, le=1.0)
    
    # 日志配置
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE: Optional[str] = Field(default=None)
    
    # LLM 配置
    LLM_MODEL: str = Field(default="gpt-3.5-turbo")
    LLM_TEMPERATURE: float = Field(default=0.1)
    LLM_MAX_TOKENS: int = Field(default=2000)
    LLM_TIMEOUT: int = Field(default=30)
    
    @property
    def is_mock_mode(self) -> bool:
        """是否为 Mock 模式"""
        return self.USE_MOCK_RETRIEVAL and self.USE_MOCK_LLM
    
    @property
    def is_production(self) -> bool:
        """是否为生产环境"""
        return not self.DEBUG


settings = Settings()