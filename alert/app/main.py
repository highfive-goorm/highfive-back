# alert/app/main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from .database import SessionLocal
from .crud import CRUDAlert
from typing import List, Optional

app = FastAPI()
# 테이블 자동 생성

crud = CRUDAlert()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/alert", response_model=dict)
def list_alerts(
        user_id: Optional[str] = None,
        page: int = 1,
        size: int = 10,
        db: Session = Depends(get_db)
):
    all_alerts = crud.get_alerts(db, user_id)
    total = len(all_alerts)
    start = (page - 1) * size
    end = start + size
    paginated_alerts = all_alerts[start:end]
    return {"alerts": paginated_alerts, "total": total}
