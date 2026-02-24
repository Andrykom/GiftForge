import os
import httpx
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        # Используем переменную окружения или дефолт
        self.base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        self.admin_api_key = os.getenv("ADMIN_API_KEY", "dev-key")
        logger.info(f"API Client initialized with base URL: {self.base_url}")

    async def generate_qr(self, barista_id: int) -> Dict:
        """Генерация QR кода"""
        url = f"{self.base_url}/qr/generate"
        logger.info(f"Requesting QR generation at: {url}")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                params={"barista_id": barista_id, "business_id": "COFFEE_001"},
                headers={"X-API-Key": self.admin_api_key},
                timeout=10.0
            )
            logger.info(f"Response status: {response.status_code}")
            response.raise_for_status()
            return response.json()

    async def get_stats(self) -> Dict:
        """Получение статистики"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/stats/simple",
                params={"business_id": "COFFEE_001"},
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()

    async def get_budget(self) -> Dict:
        """Получение бюджета"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/budget/status",
                params={"business_id": "COFFEE_001"},
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()

    async def send_gift(self, user_id: int, qr_token: str, username: str = None) -> Dict:
        """Отправка подарка"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/gift/send",
                json={
                    "user_id": user_id,
                    "qr_token": qr_token,
                    "telegram_username": username
                },
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()

api_client = APIClient()
