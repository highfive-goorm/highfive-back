# alert/app/schemas.py
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class AlertBase(BaseModel):
    title: str
    content: str
    user_id: str
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
    updated_at: datetime

    model_config = ConfigDict(
        validate_by_name=True,
        from_attributes=True
    )
