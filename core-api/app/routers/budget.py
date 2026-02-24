from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
async def budget_status():
    return {"message": "Budget status - TODO Day 2"}

@router.post("/refill")
async def refill_budget():
    return {"message": "Budget refill - TODO Day 2"}
