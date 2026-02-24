#!/usr/bin/env python3
"""Инициализация тестовых данных"""

import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/giftforge")

engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_data():
    async with async_session() as db:
        import sys
        sys.path.append('core-api')
        from app.models.business import Business
        from app.models.barista import Barista

        print("🔄 Инициализация тестовых данных...")

        # Бизнес
        result = await db.execute(select(Business).where(Business.id == "COFFEE_001"))
        business = result.scalar_one_or_none()

        if not business:
            business = Business(
                id="COFFEE_001",
                name="Test Coffee Shop",
                total_deposited=50000.0,
                spent=0.0
            )
            db.add(business)
            print("✅ Создан бизнес: COFFEE_001")
        else:
            print("ℹ️  Бизнес COFFEE_001 уже существует")

        # Бариста
        test_barista_id = 123456789
        result = await db.execute(select(Barista).where(Barista.telegram_id == test_barista_id))
        barista = result.scalar_one_or_none()

        if not barista:
            barista = Barista(
                telegram_id=test_barista_id,
                username="test_barista",
                full_name="Test Barista",
                business_id="COFFEE_001",
                is_active=True
            )
            db.add(barista)
            print(f"✅ Создана бариста: ID {test_barista_id}")
        else:
            print(f"ℹ️  Бариста {test_barista_id} уже существует")

        await db.commit()
        print("\n🎉 Инициализация завершена!")

if __name__ == "__main__":
    asyncio.run(init_data())
