from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from app.database import engine, Base
from app.routers.qr import router as qr_router
from app.routers.gift import router as gift_router
from app.routers.budget import router as budget_router
from app.routers.stats import router as stats_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized")
    yield
    logger.info("Shutting down...")
    await engine.dispose()

app = FastAPI(
    title="GiftForge API",
    description="API для системы подарков Telegram Stars",
    version="0.1.0",
    lifespan=lifespan
)

# Подключаем роутеры
app.include_router(qr_router, prefix="/qr", tags=["QR Codes"])
app.include_router(gift_router, prefix="/gift", tags=["Gifts"])
app.include_router(budget_router, prefix="/budget", tags=["Budget"])
app.include_router(stats_router, prefix="/stats", tags=["Statistics"])

logger.info("Routers registered: /qr, /gift, /budget, /stats")

@app.get("/")
async def root():
    return {"message": "GiftForge API MVP", "version": "0.1.0"}

@app.get("/health")
async def health():
    return {"status": "ok"}
