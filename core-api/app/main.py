from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routers import qr, gift, budget, stats

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="GiftForge API",
    description="API для системы подарков Telegram Stars",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(qr.router, prefix="/qr", tags=["QR Codes"])
app.include_router(gift.router, prefix="/gift", tags=["Gifts"])
app.include_router(budget.router, prefix="/budget", tags=["Budget"])
app.include_router(stats.router, prefix="/stats", tags=["Statistics"])

@app.get("/")
async def root():
    return {"message": "GiftForge API MVP", "version": "0.1.0"}

@app.get("/health")
async def health():
    return {"status": "ok"}
