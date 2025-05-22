# admin/app/schemas.py
from pydantic import BaseModel


class AdminLogin(BaseModel):
    account: str
    password: str

    class Config:
        orm_mode=True
class AdminRespLogin(BaseModel):
    id: int
    account: str

    class Config:
        orm_mode = True
