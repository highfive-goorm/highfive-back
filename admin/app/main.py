# admin/app/main.py
from fastapi import HTTPException, FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Admin
from schemas import AdminLogin

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/admin/login")
def admin_login(login_data: AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.account == login_data.account).first()
    if not admin or admin.password != login_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"id": admin.id, "account": admin.account}
