from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.database import get_db
from db.models.models import TelegramUser
from utils.jwt import create_access_token
from redis_client import redis_client

router = APIRouter(
    prefix="/auth",
    tags=["Authentication 🔐"]
)


@router.post("/telegram-login")
async def telegram_login(telegram_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TelegramUser).where(TelegramUser.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if not user:
        user = TelegramUser(telegram_id=telegram_id)
        db.add(user)
        await db.commit()
        await db.refresh(user)
    token = create_access_token({"sub": str(user.telegram_id)})
    await redis_client.set(f"token:{user.telegram_id}", token, ex=60 * 60 * 24 * 7)
    return {"access_token": token, "token_type": "bearer"}
