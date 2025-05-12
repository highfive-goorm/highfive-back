from pydantic import BaseModel, EmailStr

class AdminLogin(BaseModel):
    id:int
    account:str
    password: str

class TokenResponse(BaseModel):
    access_token: str