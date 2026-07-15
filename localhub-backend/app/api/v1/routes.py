from fastapi import APIRouter

from app.api.v1.endpoints import chat, health, locations, posts, weather

router = APIRouter()

# All paths below are mounted under /api by app.main, matching the frontend contract.
router.include_router(health.router, tags=["health"])
router.include_router(locations.router, tags=["locations"])
router.include_router(posts.router, prefix="/posts", tags=["posts"])
router.include_router(chat.router, tags=["chat"])
router.include_router(weather.router, tags=["weather"])
