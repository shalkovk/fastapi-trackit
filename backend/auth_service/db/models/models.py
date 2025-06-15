from sqlalchemy import Column, BigInteger, String,  Boolean, Integer
from db.database import Base


class TelegramUser(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    telegram_id = Column(BigInteger, index=True, unique=True, nullable=False)
    is_active = Column(Boolean, index=True, default=True)
