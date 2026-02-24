#!/usr/bin/env python3
"""Тестирование API GiftForge"""

import httpx
import asyncio
import sys

BASE_URL = "http://localhost:8000"
ADMIN_API_KEY = "dev-key"

async def test_health():
    """Тест health check"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        print(f"Health: {response.status_code} - {response.json()}")
        return response.status_code == 200

async def test_generate_qr():
    """Тест генерации QR"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/qr/generate",
            params={"barista_id": 123456789, "business_id": "COFFEE_001"},
            headers={"X-API-Key": ADMIN_API_KEY}
        )
        print(f"Generate QR: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Token: {data['token'][:50]}...")
            print(f"  URL: {data['qr_url'][:80]}...")
            return data['token']
        else:
            print(f"  Error: {response.text}")
            return None

async def test_validate_qr(token: str):
    """Тест валидации QR"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/qr/validate/{token}")
        print(f"Validate QR: {response.status_code} - {response.json()}")
        return response.status_code == 200

async def test_budget_status():
    """Тест статуса бюджета"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/budget/status",
            params={"business_id": "COFFEE_001"}
        )
        print(f"Budget Status: {response.status_code}")
        if response.status_code == 200:
            print(f"  {response.json()}")

async def test_stats():
    """Тест статистики"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/stats/simple",
            params={"business_id": "COFFEE_001"}
        )
        print(f"Stats: {response.status_code}")
        if response.status_code == 200:
            print(f"  {response.json()}")

async def main():
    print("🧪 Тестирование GiftForge API")
    print("=" * 50)

    # Health check
    if not await test_health():
        print("❌ API не доступен")
        sys.exit(1)

    print()

    # Budget
    await test_budget_status()
    print()

    # Stats
    await test_stats()
    print()

    # Generate QR
    token = await test_generate_qr()
    if token:
        print()
        # Validate QR
        await test_validate_qr(token)

    print()
    print("=" * 50)
    print("✅ Тестирование завершено")

if __name__ == "__main__":
    asyncio.run(main())
