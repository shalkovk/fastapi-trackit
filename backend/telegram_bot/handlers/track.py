from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import httpx
import os
from handlers.utils.validators import is_valid_tracking_number
from redis_client import redis_client as redis

router = Router()

TRACKING_SERVICE_URL = os.getenv(
    "TRACKING_SERVICE_URL", "http://tracking_service:8001")


@router.message(Command("track"))
async def track_parcel(message: Message):
    telegram_id = message.from_user.id
    parts = message.text.strip().split(maxsplit=1)
    if len(parts) != 2:
        await message.answer("Укажите трек-номер: /track <номер>")
        return

    tracking_number = parts[1]

    if not is_valid_tracking_number(tracking_number):
        await message.answer("Неверный формат трек-номера. Проверьте его и повторите попытку.")
        return

    token = await redis.get(f"token:{telegram_id}")
    if not token:
        await message.answer("Вы не авторизованы. Сначала выполните /start")
        return

    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "tracking_number": tracking_number
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{TRACKING_SERVICE_URL}/parcels/", json=payload, headers=headers)

        if response.status_code == 200:
            await message.answer("Посылка успешно добавлена для отслеживания. Для просмотра статуса выполните /list")
        elif response.status_code == 400:
            await message.answer("Такая посылка уже отслеживается.")
        else:
            await message.answer("Не удалось добавить посылку. Повторите попытку позже.")
    except Exception as e:
        await message.answer(f"Ошибка подключения к tracking-сервису:\n{str(e)}")
