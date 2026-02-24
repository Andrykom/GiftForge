from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import os

from app.database import get_db
from app.models.gift_history import GiftHistory
from app.models.business import Business

router = APIRouter()

@router.get("/simple")
async def simple_stats(
    business_id: str = os.getenv("DEFAULT_BUSINESS_ID", "COFFEE_001"),
    db: AsyncSession = Depends(get_db)
):
    """Простая статистика"""

    result = await db.execute(
        select(
            GiftHistory.rarity,
            func.count(GiftHistory.id).label("count"),
            func.sum(GiftHistory.stars_spent).label("total_stars")
        )
        .where(GiftHistory.business_id == business_id)
        .group_by(GiftHistory.rarity)
    )

    rarity_stats = {}
    for row in result:
        rarity_stats[row.rarity] = {
            "count": row.count,
            "stars": int(row.total_stars or 0)
        }

    total_result = await db.execute(
        select(func.count(GiftHistory.id))
        .where(GiftHistory.business_id == business_id)
    )
    total_gifts = total_result.scalar()

    budget_result = await db.execute(
        select(Business).where(Business.id == business_id)
    )
    business = budget_result.scalar_one_or_none()

    return {
        "business_id": business_id,
        "total_gifts": total_gifts,
        "by_rarity": rarity_stats,
        "budget": {
            "total": float(business.total_deposited) if business else 0,
            "spent": float(business.spent) if business else 0,
            "available": business.available if business else 0
        } if business else None
    }
