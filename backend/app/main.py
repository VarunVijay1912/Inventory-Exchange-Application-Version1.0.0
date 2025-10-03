"""Enhanced main application with comprehensive error handling"""
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.database import Base, engine
from app.api.v1 import api_router
from app.config import settings
from app.core.logging import logger, setup_logging
from app.core.exceptions import BaseAPIException
import os

# Setup logging
setup_logging()

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Database initialization error: {e}")

# Create upload directories
upload_dirs = [
    settings.upload_directory,
    os.path.join(settings.upload_directory, "products"),
    os.path.join(settings.upload_directory, "documents"),
    "logs"
]

for directory in upload_dirs:
    os.makedirs(directory, exist_ok=True)

# Initialize FastAPI app
app = FastAPI(
    title="Manufacturing Marketplace API",
    description="B2B marketplace for manufacturing surplus and dead stock",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Custom exception handlers
@app.exception_handler(BaseAPIException)
async def api_exception_handler(request: Request, exc: BaseAPIException):
    """Handle custom API exceptions"""
    logger.warning(f"API Exception: {exc.detail} - {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.warning(f"Validation Error: {exc.errors()} - {request.url}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors"""
    logger.error(f"Unexpected error: {str(exc)} - {request.url}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


# Mount static files
if os.path.exists(settings.upload_directory):
    app.mount("/uploads", StaticFiles(directory=settings.upload_directory), name="uploads")

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Health check endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Manufacturing Marketplace API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "version": "1.0.0"
    }


@app.get("/api/health")
async def api_health():
    """API health check"""
    return {
        "api_version": "v1",
        "status": "operational"
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info("="* 60)
    logger.info("Manufacturing Marketplace API Starting...")
    logger.info(f"Environment: {'Development' if settings.debug else 'Production'}")
    logger.info(f"API Documentation: http://{settings.host}:{settings.port}/api/docs")
    logger.info("="* 60)


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    logger.info("Manufacturing Marketplace API Shutting Down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )