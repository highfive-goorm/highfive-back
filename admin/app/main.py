# admin/app/main.py
from fastapi import HTTPException, FastAPI, Depends, Body
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Admin
from .schemas import AdminLogin, AdminRespLogin

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/admin", response_model=AdminRespLogin, status_code=201)
def admin_login(login_data: AdminLogin = Body(...), db: Session = Depends(get_db)):
    admin = db.query(Admin).filter_by(
        account=login_data.account, password=login_data.password).first()
    if admin is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        return admin
