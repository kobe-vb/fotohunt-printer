from fastapi import APIRouter
from .games import router as games_router
from .teams import router as teams_router
from .teams import team_router
from .task import router as task_router
from .shop import router as shop_router
from .qrcode import router as qrcode_router

api_router = APIRouter(prefix="/api", tags=["api"])

api_router.include_router(games_router)
api_router.include_router(teams_router)
api_router.include_router(team_router)
api_router.include_router(task_router)
api_router.include_router(shop_router)
api_router.include_router(qrcode_router)

