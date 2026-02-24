from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.database import Base

class GiftHistory(Base):
    __tablename__ = "gift_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(String(32), ForeignKey("businesses.id"), nullable=False)
    qr_token_id = Column(UUID(as_uuid=True), ForeignKey("qr_tokens.id"))
    user_id = Column(BigInteger, nullable=False, index=True)
    telegram_username = Column(String(64), nullable=True)
    rarity = Column(String(20), nullable=False)
    stars_spent = Column(Integer, nullable=False)
    gift_telegram_id = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default="pending")
