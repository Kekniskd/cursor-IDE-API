from fastapi import FastAPI
from src.router.post_router import router as post_router
from src.database.config import engine
from src.database.models import Base
from src.database.test_data import insert_sample_data

app = FastAPI(
    title="Post Management API",
    description="A simple FastAPI application for managing posts with SQLite backend",
    version="1.0.0"
)

# Create database tables on startup
Base.metadata.create_all(bind=engine)

# Insert sample data
insert_sample_data()

@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Welcome to Post Management API",
        "docs_url": "/docs",
        "endpoints": {
            "posts": "/posts",
            "documentation": "/docs",
            "openapi": "/openapi.json"
        }
    }

app.include_router(post_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
