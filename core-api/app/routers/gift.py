from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import os

from app.database import get_db
from app.services.qr_service import qr_service
from app.services.gift_engine import gift_engine
from app.services.budget_service import budget_service
from app.services.telegram_gifts import telegram_gift_service
from app.models.qr_token import QRToken
from app.models.gift_history import GiftHistory

router = APIRouter()

@router.post("/send")
async def send_gift(
    user_id: int,
    qr_token: str,
    telegram_username: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Отправка подарка клиенту"""

    # 1. Валидируем QR
    validation = await qr_service.validate_token(qr_token)
    if not validation:
        raise HTTPException(status_code=400, detail="Invalid or expired QR token")

    # 2. Проверяем в БД
    result = await db.execute(
        select(QRToken).where(QRToken.token_hash == validation["token_hash"])
    )
    db_token = result.scalar_one_or_none()

    if not db_token or db_token.is_used:
        raise HTTPException(status_code=400, detail="Token already used or not found")

    # 3. Определяем подарок
    gift_drop = gift_engine.calculate_drop()
    stars_needed = gift_drop["stars"]

    # 4. Проверяем бюджет
    has_budget = await budget_service.check_budget(
        validation["business_id"], 
        stars_needed, 
        db
    )

    if not has_budget:
        raise HTTPException(status_code=402, detail="Insufficient budget")

    # 5. Списываем бюджет
    spent = await budget_service.spend_budget(
        validation["business_id"],
        stars_needed,
        db
    )

    if not spent:
        raise HTTPException(status_code=500, detail="Failed to process budget")

    # 6. Отправляем подарок (mock)
    gift_result = await telegram_gift_service.send_gift(
        user_id, 
        gift_drop["rarity"]
    )

    # 7. Помечаем QR как использованный
    await qr_service.mark_used(validation["token_hash"], user_id)

    # 8. Обновляем в БД
    db_token.is_used = True
    db_token.used_at = datetime.utcnow()
    db_token.used_by = user_id

    # 9. Сохраняем историю
    history = GiftHistory(
        business_id=validation["business_id"],
        qr_token_id=db_token.id,
        user_id=user_id,
        telegram_username=telegram_username,
        rarity=gift_drop["rarity"],
        stars_spent=stars_needed,
        gift_telegram_id=gift_result.get("gift_telegram_id"),
        status="sent" if gift_result["success"] else "failed"
    )
    db.add(history)
    await db.commit()

    return {
        "success": True,
        "rarity": gift_drop["rarity"],
        "name": gift_drop["name"],
        "emoji": gift_drop["emoji"],
        "stars_spent": stars_needed,
        "gift_telegram_id": gift_result.get("gift_telegram_id"),
        "message": f"{gift_drop['emoji']} Вы получили: {gift_drop['name']}!"
    }
