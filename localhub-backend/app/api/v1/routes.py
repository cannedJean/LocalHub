from fastapi import APIRouter

from app.api.v1.endpoints import board, chatbot, health, tourism, weather

router = APIRouter()

router.include_router(health.router, prefix="", tags=["health"])
router.include_router(tourism.router, prefix="/tourism", tags=["tourism"])
router.include_router(board.router, prefix="/board", tags=["board"])
router.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
router.include_router(weather.router, prefix="/weather", tags=["weather"])
