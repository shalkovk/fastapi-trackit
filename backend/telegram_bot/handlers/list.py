from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import httpx
import os
from redis_client import redis_client as redis


router = Router()


@router.message(Command("list"))
async def list_handler(message: Message):
    telegram_id = message.from_user.id
    token = await redis.get(f"token:{telegram_id}")
    if not token:
        await message.answer(f"Вы не авторизованы. Сначала выполните /start")
        return

    header = {
        "Authorizatin": f"Bearer {token}"
    }

    payload = {

    }
