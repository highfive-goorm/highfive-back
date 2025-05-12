from fastapi import APIRouter, HTTPException, FastAPI, Depends
import hashlib
from datetime import datetime, timedelta
from jose import jwt
from requests import Session

from admin.app.database import SessionLocal
from admin.app.models import Admin
from admin.app.schemas import TokenResponse, AdminLogin

app = FastAPI()
router = APIRouter()

SECRET_KEY = 'django-insecure-=#ztpi!p#7h6ud@omrn$yjd%jxp(__+1*+0wew+55g!(^%wsfd'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=TokenResponse)
def admin_login(login_data: AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.account == login_data.account).first()
    if not admin or not verify_password(login_data.password, admin.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"id": admin.id, "account": admin.account})
    return {"access": token}
