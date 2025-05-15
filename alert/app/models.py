from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from .database import Base

class Alert(Base):
    __tablename__ = "alert"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String(1000), nullable=False)
    user_id = Column(Integer, nullable=False)
    is_global = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
