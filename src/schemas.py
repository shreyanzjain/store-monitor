from pydantic import BaseModel
from datetime import datetime

class StatusByTimeBase(BaseModel):
    store_id: int

class StatusByTimeCreate(StatusByTimeBase):
    timestamp_utc: datetime
    status: str

class StatusByTime(StatusByTimeBase):
    id: int
    timestamp_utc: datetime
    status: str

    class Config:
        orm_mode = True
