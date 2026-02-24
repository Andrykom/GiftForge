from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models.business import Business

class BudgetService:
    @staticmethod
    async def check_budget(business_id: str, amount: int, db: AsyncSession) -> bool:
        result = await db.execute(
            select(Business).where(Business.id == business_id)
        )
        business = result.scalar_one_or_none()

        if not business:
            return False

        return business.available >= amount

    @staticmethod
    async def spend_budget(business_id: str, amount: int, db: AsyncSession) -> bool:
        result = await db.execute(
            select(Business)
            .where(Business.id == business_id)
            .with_for_update()
        )
        business = result.scalar_one_or_none()

        if not business or business.available < amount:
            return False

        business.spent = float(business.spent or 0) + amount
        await db.commit()
        return True

    @staticmethod
    async def get_status(business_id: str, db: AsyncSession) -> Optional[dict]:
        result = await db.execute(
            select(Business).where(Business.id == business_id)
        )
        business = result.scalar_one_or_none()

        if not business:
            return None

        return {
            "business_id": business.id,
            "name": business.name,
            "total_deposited": float(business.total_deposited),
            "spent": float(business.spent),
            "available": business.available
        }

budget_service = BudgetService()
