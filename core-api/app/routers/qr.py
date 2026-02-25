from fastapi import APIRouter, HTTPException, Depends, Header, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.database import get_db
from app.services.qr_service import qr_service
from app.models.qr_token import QRToken
from app.models.barista import Barista
from datetime import datetime
import os

router = APIRouter()


@router.get("/claim", response_class=HTMLResponse)
async def claim_qr(token: str = Query(..., description="QR token, prefixed with qr_")):
        """Claim endpoint: logs the click and returns an HTML page that attempts
        to open the Telegram app via tg:// and provides a fallback link to t.me.
        """
        client_bot_username = os.getenv("CLIENT_BOT_USERNAME", "Gift_Forge_Client_bot")
        # Log for analytics/debug
        print(f"QR claim requested: {token}")

        # Ensure token is URL-encoded when inserted into links
        from urllib.parse import quote
        encoded = quote(token, safe="")

        tg_deep = f"tg://resolve?domain={client_bot_username}&start={encoded}"
        web_link = f"https://t.me/{client_bot_username}?start={encoded}"

        html = f"""
        <!doctype html>
        <html>
            <head>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width,initial-scale=1">
                <title>Open in Telegram</title>
            </head>
            <body>
                <p>Открывается Telegram… Если приложение не открылось автоматически, нажмите кнопку:</p>
                <p><a id="open" href="{web_link}">Открыть в Telegram</a></p>
                <script>
                    // Try to open tg:// first (mobile deep link). If it fails, user can click the web link.
                    window.location = "{tg_deep}";
                    // After a short delay, ensure the web link is visible
                    setTimeout(function() {{ document.getElementById('open').style.display = 'inline'; }}, 1000);
                </script>
            </body>
        </html>
        """

        return HTMLResponse(content=html)

async def verify_admin_key(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("ADMIN_API_KEY", "dev-key"):
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key

@router.post("/generate")
async def generate_qr(
    barista_id: int,
    business_id: str = os.getenv("DEFAULT_BUSINESS_ID", "COFFEE_001"),
    db: AsyncSession = Depends(get_db),
    api_key: str = Depends(verify_admin_key)
):
    """Генерация QR кода для подарка"""

    result = await db.execute(
        select(Barista).where(Barista.telegram_id == barista_id)
    )
    barista = result.scalar_one_or_none()

    if not barista:
        raise HTTPException(status_code=404, detail="Barista not found")

    qr_data = qr_service.generate_token(barista_id, business_id)

    db_token = QRToken(
        token_hash=qr_data["token_hash"],
        business_id=business_id,
        barista_id=barista_id,
        expires_at=datetime.fromisoformat(qr_data["expires_at"])
    )
    db.add(db_token)
    await db.commit()

    return {
        "success": True,
        "token": qr_data["token"],
        "qr_url": qr_data["qr_url"],
        "expires_at": qr_data["expires_at"],
        "ttl_seconds": qr_data["ttl_seconds"]
    }

@router.get("/validate/{token}")
async def validate_qr(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    """Валидация QR токена"""

    validation = await qr_service.validate_token(token)

    if not validation:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    result = await db.execute(
        select(QRToken).where(QRToken.token_hash == validation["token_hash"])
    )
    db_token = result.scalar_one_or_none()

    if not db_token:
        raise HTTPException(status_code=404, detail="Token not found in database")

    if db_token.is_used:
        raise HTTPException(status_code=400, detail="Token already used")

    return {
        "valid": True,
        "business_id": validation["business_id"],
        "barista_id": validation["barista_id"],
        "token_hash": validation["token_hash"]
    }
