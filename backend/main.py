import asyncio

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import api_router
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.responses import FileResponse

from services.PrinterQueue import PrinterQueue

from dotenv import load_dotenv
load_dotenv()

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
    allow_origins=["http://localhost:5173", "http://192.168.68.112:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

app.mount("/static", StaticFiles(directory="static"), name="static")



frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"

if frontend_dist.exists():
    # Serve statische bestanden (JS, CSS, images, etc.)
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")
    
    # Serve index.html voor alle andere routes (voor client-side routing)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """
        Serve de frontend. Als het bestand bestaat, serve het.
        Anders serve index.html (voor React Router, Vue Router, etc.)
        """
        # Check of het een specifiek bestand is
        file_path = frontend_dist / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        
        # Anders serve index.html (voor SPA routing)
        index_path = frontend_dist / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
        
        return {"error": "Frontend not built. Run 'npm run build' in frontend folder."}
else:
    @app.get("/")
    async def no_frontend():
        return {
            "error": "Frontend not found",
            "message": "Run 'npm run build' in the frontend directory first",
            "path_checked": str(frontend_dist)
        }

