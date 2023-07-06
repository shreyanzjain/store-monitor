from .database import Base
from sqlalchemy import Column, Integer, String, DateTime


class StatusByTime(Base):
    __tablename__ = "status_by_time"

    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer)
    timestamp_utc = Column(DateTime)
    status = Column(String)
