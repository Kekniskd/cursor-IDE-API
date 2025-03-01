from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.router.post_router import router as post_router
from src.database.config import engine
from src.database.models import Base
from src.utils.logger import logger
from datetime import datetime

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Post Management API")
    logger.info("Creating database tables if they don't exist")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise
    yield
    # Shutdown
    logger.info("Shutting down Post Management API")

app = FastAPI(
    title="Post Management API",
    description="A simple FastAPI application for managing posts with SQLite backend",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/", tags=["root"])
async def root():
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to Post Management API",
        "docs_url": "/docs",
        "endpoints": {
            "posts": "/posts",
            "documentation": "/docs",
            "openapi": "/openapi.json"
        }
    }

# Include the post router
app.include_router(post_router)

# Add middleware for request logging
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    duration = datetime.now() - start_time
    
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Duration: {duration.total_seconds():.3f}s"
    )
    return response

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting uvicorn server")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
