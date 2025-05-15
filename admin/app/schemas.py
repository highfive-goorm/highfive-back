from pydantic import BaseModel


class AdminLogin(BaseModel):
    id: int
    account: str
    password: str
