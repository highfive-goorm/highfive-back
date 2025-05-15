# alert/app/crud.py
from typing import Optional, List
from sqlalchemy.orm import Session
from .models import Alert
from .schemas import AlertCreate, AlertUpdate
from datetime import datetime

class CRUDAlert:
    def create_alert(self, db: Session, alert: AlertCreate) -> Alert:
        db_alert = Alert(**alert.dict(), created_at=datetime.utcnow())
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
        return db_alert

    def get_alert(self, db: Session, id: int) -> Optional[Alert]:
        return db.query(Alert).filter(Alert.id == id).first()

    def get_alerts(self, db: Session, user_id: Optional[str] = None) -> List[Alert]:
    if user_id:
        return db.query(Alert).filter((Alert.user_id == user_id) | (Alert.is_global == True)).all()
    # user_id가 없으면 is_global이 True인 것만 반환
    return db.query(Alert).filter(Alert.is_global == True).all()

    def update_alert(self, db: Session, id: int, update_data: AlertUpdate) -> Optional[Alert]:
        alert = db.query(Alert).filter(Alert.id == id).first()
        if alert:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(alert, key, value)
            db.commit()
            db.refresh(alert)
        return alert

    def delete_alert(self, db: Session, id: int) -> bool:
        alert = db.query(Alert).filter(Alert.id == id).first()
        if alert:
            db.delete(alert)
            db.commit()
            return True
        return False