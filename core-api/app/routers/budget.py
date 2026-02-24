from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import os

from app.database import get_db
from app.services.budget_service import budget_service
from app.models.business import Business

router = APIRouter()

async def verify_master_key(x_master_key: str = Header(...)):
    if x_master_key != os.getenv("MASTER_API_KEY", "master-key"):
        raise HTTPException(status_code=403, detail="Invalid master key")
    return x_master_key

@router.get("/status")
async def budget_status(
    business_id: str = os.getenv("DEFAULT_BUSINESS_ID", "COFFEE_001"),
    db: AsyncSession = Depends(get_db)
):
    """Получение статуса бюджета"""
    status = await budget_service.get_status(business_id, db)

    if not status:
        raise HTTPException(status_code=404, detail="Business not found")

    return status

@router.post("/refill")
async def refill_budget(
    business_id: str,
    amount: float,
    db: AsyncSession = Depends(get_db),
    master_key: str = Depends(verify_master_key)
):
    """Пополнение бюджета"""
    result = await db.execute(
        select(Business).where(Business.id == business_id)
    )
    business = result.scalar_one_or_none()

    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    business.total_deposited = float(business.total_deposited or 0) + amount
    await db.commit()

    return {
        "success": True,
        "business_id": business_id,
        "amount_added": amount,
        "new_total": float(business.total_deposited),
        "available": business.available
    }
