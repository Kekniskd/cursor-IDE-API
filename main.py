from fastapi import FastAPI
from src.router.name_router import router as name_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from cursor-learn!"}

app.include_router(name_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
