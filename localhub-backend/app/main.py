from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import router as api_router
from app.services.database import engine
from app.models.base import Base
from app.core.config import get_settings
import app.models.board  # noqa: F401  (register model before create_all)

app = FastAPI(title="LocalHub API", version="0.1.0")

# Read allowed origins from settings (comma-separated string) so production Netlify
# origins can be configured via .env. Defaults allow local dev origins.
settings = get_settings()
allowed = [o.strip().rstrip("/") for o in settings.allowed_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend calls ${VITE_API_BASE_URL}/api/...; keep the prefix configurable for tests/deployment.
app.include_router(api_router, prefix=settings.api_prefix)

# Create database tables on import/startup (SQLite)
Base.metadata.create_all(bind=engine)
