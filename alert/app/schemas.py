from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlertBase(BaseModel):
    title: str
    content: str
    user_id: int
    is_global: Optional[bool] = False

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    is_global: Optional[bool]

class AlertInDB(AlertBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
