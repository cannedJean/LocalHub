from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "LocalHub"
    api_prefix: str = "/api"
    database_url: str = "sqlite:///./localhub.db"
    allowed_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    openai_api_key: SecretStr | None = None
    openai_model: str = "gpt-5-mini"
    openai_timeout_seconds: float = 20.0
    openai_max_output_tokens: int = 800
    openai_reasoning_effort: Literal["minimal", "low", "medium", "high"] = "minimal"
    weather_api_key: SecretStr | None = None
    weather_timeout_seconds: float = 10.0

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


@lru_cache()
def get_settings() -> Settings:
    return Settings()
