from fastapi import FastAPI
from app.api.v1.routes import router as api_router
from app.services.database import engine
from app.models.base import Base
import app.models.board

app = FastAPI(title="LocalHub API", version="0.1.0")

app.include_router(api_router, prefix="/api/v1")

# Create database tables on import/startup (SQLite)
Base.metadata.create_all(bind=engine)
