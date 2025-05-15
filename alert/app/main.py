from typing import Optional, List

from fastapi import APIRouter, HTTPException, Query, FastAPI, Depends
from datetime import datetime
from bson import ObjectId
from sqlalchemy.orm import Session
from .crud import CRUD as crud
from .database import SessionLocal
from .schemas import AlertCreate, AlertInDB, AlertUpdate


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.post("/alert", response_model=AlertInDB, status_code=201)
def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    return crud.create_alert(db, alert)


@app.get("/alert", response_model=List[AlertInDB])
def list_alerts(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    return crud.get_alerts(db, user_id)


@app.get("/alert/{id}", response_model=AlertInDB)
def get_alert(id: int, db: Session = Depends(get_db)):
    alert = crud.get_alert(db, id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@app.put("/alert/{id}", response_model=AlertInDB)
def update_alert(id: int, update: AlertUpdate, db: Session = Depends(get_db)):
    alert = crud.update_alert(db, id, update)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@app.delete("/alert/{id}", status_code=204)
def delete_alert(id: int, db: Session = Depends(get_db)):
    if not crud.delete_alert(db, id):
        raise HTTPException(status_code=404, detail="Alert not found")
    return
