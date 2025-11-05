from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api import files
from app.config import get_settings
from app.services.storage import storage_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for the application"""
    settings = get_settings()
    logger.info("Starting application...")

    # Initialize storage service
    try:
        storage_service.initialize()
        logger.info("Storage service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize storage service: {e}")
        raise

    yield

    # Cleanup
    logger.info("Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title="Google Drive Clone API",
    description="API for file storage and management",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(files.router, prefix="/api/files", tags=["files"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Google Drive Clone API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
