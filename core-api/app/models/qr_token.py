from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.database import Base

class QRToken(Base):
    __tablename__ = "qr_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token_hash = Column(String(64), unique=True, nullable=False, index=True)
    business_id = Column(String(32), ForeignKey("businesses.id"), nullable=False)
    barista_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used_at = Column(DateTime(timezone=True), nullable=True)
    used_by = Column(BigInteger, nullable=True)
    is_used = Column(Boolean, default=False)
