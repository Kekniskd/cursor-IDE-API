from fastapi import APIRouter
from pydantic import BaseModel
from src.utils.letter_counter import count_letters

router = APIRouter()

class NamePayload(BaseModel):
    name: str

@router.post("/name")
async def process_name(payload: NamePayload):
    letter_counts = count_letters(payload.name)
    return {
        "message": f"Hello, {payload.name}!",
        "letter_counts": letter_counts
    } 