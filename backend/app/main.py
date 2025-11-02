from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from .config import settings
from .database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle-Events"""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend statisch ausliefern
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# API-Router
from .api import device, camera, album
app.include_router(device.router, prefix="/api/device", tags=["device"])
app.include_router(camera.router, prefix="/api/camera", tags=["camera"])
app.include_router(album.router, prefix="/api/album", tags=["album"])
# app.include_router(astro.router, prefix="/api/astro", tags=["astro"])
# app.include_router(focus.router, prefix="/api/focus", tags=["focus"])
# app.include_router(motor.router, prefix="/api/motor", tags=["motor"])


@app.get("/")
async def root():
    """Root-Endpoint"""
    return {
        "message": "DWARF II Control API",
        "version": settings.api_version,
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health-Check"""
    return {"status": "ok"}
