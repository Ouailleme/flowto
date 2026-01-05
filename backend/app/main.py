"""FastAPI main application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.core.database import init_db, close_db
from app.api.v1 import auth

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info(f"Starting {settings.APP_NAME}...")
    await init_db()
    logger.info("Database initialized")
    yield
    # Shutdown
    logger.info("Shutting down...")
    await close_db()
    logger.info("Database connections closed")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Automatisation comptable pour PME avec IA",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Health check
@app.get("/", tags=["health"])
async def root():
    """Root endpoint - health check"""
    return {
        "app": settings.APP_NAME,
        "status": "ok",
        "version": "1.0.0",
        "environment": settings.APP_ENV
    }


@app.get("/health", tags=["health"])
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV
    }


# Include routers
app.include_router(auth.router, prefix="/api/v1")


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return {
        "detail": "Endpoint not found",
        "status_code": 404
    }


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler"""
    logger.error(f"Internal server error: {exc}")
    return {
        "detail": "Internal server error",
        "status_code": 500
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

