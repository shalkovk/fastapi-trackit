from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import httpx
import os
from redis_client import redis_client as redis


router = Router()

TRACKING_SERVICE_URL = os.getenv(
    "TRACKING_SERVICE_URL", "http://tracking_service:8001")


@router.message(Command("list"))
async def list_handler(message: Message):
    telegram_id = message.from_user.id
    token = await redis.get(f"token:{telegram_id}")
    if not token:
        await message.answer(f"Вы не авторизованы. Сначала выполните /start")
        return

    header = {
        "Authorization": f"Bearer {token}"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{TRACKING_SERVICE_URL}/parcels/list", headers=header)
        if response.status_code == 200:
            parcels = response.json()
            if not parcels:
                await message.answer("У вас нет активных посылок.")
                return

            text = "Ваши посылки:\n"
            for parcel in parcels:
                text += f"📦 {parcel['tracking_number']} — {parcel.get('status')}\n"
            await message.answer(text)
        else:
            await message.answer("Не удалось получить список посылок.")
    except Exception as e:
        await message.answer(f"Ошибка подключения к tracking-сервису:\n{str(e)}")
