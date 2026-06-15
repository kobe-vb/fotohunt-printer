from fastapi import APIRouter
from .games import router as games_router
from .teams import router as teams_router

api_router = APIRouter(prefix="/api", tags=["api"])

api_router.include_router(games_router)
api_router.include_router(teams_router)
