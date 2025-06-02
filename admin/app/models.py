# admin/app/models.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from .database import Base


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    account = Column(String(50), nullable=False, unique=True)
    password = Column(String(200), nullable=False)  # 평문 비밀번호 저장
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
