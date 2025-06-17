from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from db.database import Base


class Parcel(Base):
    __tablename__ = "parcels"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tracking_number = Column(String, unique=True, nullable=False)
    carrier = Column(String, nullable=True)
    status = Column(String)
    last_update = Column(DateTime, default=datetime.now())
    owner_telegram_id = Column(BigInteger, index=True)
