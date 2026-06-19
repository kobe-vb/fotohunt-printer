import asyncio

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import api_router
from contextlib import asynccontextmanager

from services.PrinterQueue import PrinterQueue

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    init_db()
    
    app.state.printerQueue = PrinterQueue()
    asyncio.create_task(app.state.printerQueue.worker())
    yield
     
app = FastAPI(lifespan=lifespan, title="Fotohunt API", version="0.1.0")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)