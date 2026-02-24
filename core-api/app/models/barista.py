from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, BigInteger
from sqlalchemy.sql import func
from app.database import Base

class Barista(Base):
    __tablename__ = "baristas"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(64), nullable=True)
    full_name = Column(String(128), nullable=True)
    business_id = Column(String(32), ForeignKey("businesses.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
