import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def _load_env() -> None:
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./localhub.db")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
SELECTED_REGION = os.getenv("SELECTED_REGION", "대전_충청권")
PASSWORD_SALT = os.getenv("PASSWORD_SALT", "localhub-secret-salt")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")