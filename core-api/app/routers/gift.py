from fastapi import APIRouter

router = APIRouter()

@router.post("/send")
async def send_gift():
    return {"message": "Gift sending - TODO Day 3"}
