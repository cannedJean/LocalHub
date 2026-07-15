from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import router as api_router
from app.services.database import engine
from app.models.base import Base
import app.models.board  # noqa: F401  (register model before create_all)

app = FastAPI(title="LocalHub API", version="0.1.0")

# The Vue dev server runs on 5173; allow it (and the 127.0.0.1 alias) for local integration.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend calls ${VITE_API_BASE_URL}/api/... so the whole API is mounted under /api.
app.include_router(api_router, prefix="/api")

# Create database tables on import/startup (SQLite)
Base.metadata.create_all(bind=engine)
