from sqlalchemy import Column, String, Integer, DateTime, Numeric
from sqlalchemy.sql import func
from app.database import Base

class Business(Base):
    __tablename__ = "businesses"

    id = Column(String(32), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    total_deposited = Column(Numeric(12, 2), default=0)
    spent = Column(Numeric(12, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    @property
    def available(self):
        return float(self.total_deposited or 0) - float(self.spent or 0)
