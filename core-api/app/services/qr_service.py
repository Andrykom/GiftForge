import hmac
import hashlib
import secrets
import base64
from datetime import datetime, timedelta
from typing import Optional, Dict
import redis.asyncio as redis
import os

class QRService:
    def __init__(self):
        self.secret = os.getenv("HMAC_SECRET", "change-me-in-production")
        self.ttl = int(os.getenv("QR_TTL_SECONDS", "300"))
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis = None

    async def get_redis(self):
        if self.redis is None:
            self.redis = await redis.from_url(self.redis_url, decode_responses=True)
        return self.redis

    def generate_token(self, barista_id: int, business_id: str) -> Dict:
        """Генерация подписанного QR токена"""
        timestamp = int(datetime.utcnow().timestamp())
        nonce = secrets.token_urlsafe(8)

        payload = f"{barista_id}:{business_id}:{timestamp}:{nonce}"

        signature = hmac.new(
            self.secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()[:16]

        token = f"{payload}:{signature}"
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        expires_at = datetime.utcnow() + timedelta(seconds=self.ttl)

        return {
            "token": token,
            "token_hash": token_hash,
            "qr_url": f"https://t.me/CoffeeShopBot?start=qr_{token}",
            "expires_at": expires_at.isoformat(),
            "ttl_seconds": self.ttl
        }

    async def validate_token(self, token: str) -> Optional[Dict]:
        """Валидация токена"""
        try:
            parts = token.split(":")
            if len(parts) != 5:
                return None

            barista_id, business_id, timestamp_str, nonce, signature = parts

            payload = f"{barista_id}:{business_id}:{timestamp_str}:{nonce}"
            expected_sig = hmac.new(
                self.secret.encode(),
                payload.encode(),
                hashlib.sha256
            ).hexdigest()[:16]

            if not hmac.compare_digest(signature, expected_sig):
                return None

            timestamp = int(timestamp_str)
            if datetime.utcnow().timestamp() > timestamp + self.ttl:
                return None

            r = await self.get_redis()
            token_hash = hashlib.sha256(token.encode()).hexdigest()

            if await r.exists(f"qr:used:{token_hash}"):
                return None

            return {
                "barista_id": int(barista_id),
                "business_id": business_id,
                "token_hash": token_hash,
                "valid": True
            }

        except (ValueError, IndexError):
            return None

    async def mark_used(self, token_hash: str, user_id: int):
        """Пометить токен как использованный"""
        r = await self.get_redis()
        await r.setex(f"qr:used:{token_hash}", self.ttl, str(user_id))

qr_service = QRService()
