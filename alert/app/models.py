# alert/app/models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, TEXT
from datetime import datetime
from .database import Base


class Alert(Base):
    __tablename__ = "alert"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(TEXT(), nullable=False)
    content = Column(TEXT(), nullable=False)
    user_id = Column(String(36), nullable=False)  # UUID 형식으로 수정
    is_global = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    class Config:
        orm_mode=True