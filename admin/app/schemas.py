# admin/app/schemas.py
from pydantic import BaseModel

class AdminLogin(BaseModel):
    account: str
    password: str
