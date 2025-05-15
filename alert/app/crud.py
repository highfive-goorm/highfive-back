from typing import Optional

from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import Alert
from .schemas import AlertCreate, AlertUpdate
from datetime import datetime


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CRUD(Alert):
    db = get_db()

    def create_alert(db: Session, alert: AlertCreate):
        db_alert = Alert(**alert.dict(), created_at=datetime.utcnow())
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
        return db_alert

    def get_alert(db: Session, id: int):
        return db.query(Alert).filter(Alert.id == id).first()

    def get_alerts(db: Session, user_id: Optional[int] = None):
        if user_id:
            return db.query(Alert).filter((Alert.user_id == user_id) | (Alert.is_global == True)).all()
        return db.query(Alert).all()

    def update_alert(db: Session, id: int, update_data: AlertUpdate):
        alert = db.query(Alert).filter(Alert.id == id).first()
        if alert:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(alert, key, value)
            db.commit()
            db.refresh(alert)
        return alert

    def delete_alert(db: Session, id: int):
        alert = db.query(Alert).filter(Alert.id == id).first()
        if alert:
            db.delete(alert)
            db.commit()
            return True
        return False
