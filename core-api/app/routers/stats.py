from fastapi import APIRouter

router = APIRouter()

@router.get("/simple")
async def simple_stats():
    return {"message": "Simple stats - TODO Day 4"}
