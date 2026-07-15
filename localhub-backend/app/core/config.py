from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "LocalHub"
    api_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./localhub.db"

    model_config = {
        "env_file": ".env"
    }


@lru_cache()
def get_settings() -> Settings:
    return Settings()
