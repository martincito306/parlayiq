from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
import app.models  # Ensure all models are registered

from app.api.v1.matches import router as matches_router
from app.api.v1.players import router as players_router
from app.api.v1.parlays import router as parlays_router
from app.api.v1.performance import router as performance_router
from app.api.v1.ai import router as ai_router
from app.api.v1.system import router as system_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create SQLite / PostgreSQL database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="PARLAYIQ Sports Intelligence & Quant Engine API",
    version=settings.VERSION,
    description="Professional Sports Intelligence, Statistical Prediction & AI Parlay Optimization Platform",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register v1 routes
prefix = settings.API_V1_PREFIX
app.include_router(matches_router, prefix=prefix)
app.include_router(players_router, prefix=prefix)
app.include_router(parlays_router, prefix=prefix)
app.include_router(performance_router, prefix=prefix)
app.include_router(ai_router, prefix=prefix)
app.include_router(system_router, prefix=prefix)


@app.get("/")
async def root():
    return {
        "name": "PARLAYIQ API",
        "version": settings.VERSION,
        "status": "ONLINE",
        "docs_url": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
