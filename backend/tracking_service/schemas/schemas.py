from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ParcelCreate(BaseModel):
    tracking_number: str


class ParcelRead(BaseModel):
    id: int
    tracking_number: str
    carrier: Optional[str] | None
    status: Optional[str]
    last_update: datetime
    owner_telegram_id: int
