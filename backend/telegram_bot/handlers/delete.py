from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import httpx
import os
from redis_client import redis_client as redis


router = Router()

TRACKING_SERVICE_URL = os.getenv(
    "TRACKING_SERVICE_URL", "http://tracking_service:8000")


@router.message(Command("delete"))
async def delete_handler(message: Message):
    telegram_id = message.from_user.id
    parts = message.text.strip().split(maxsplit=1)
    if len(parts) != 2:
        await message.answer("Укажите трек-номер: /delete <номер>")
        return

    tracking_number = parts[1]

    token = await redis.get(f"token:{telegram_id}")
    if not token:
        await message.answer(f"Вы не авторизованы. Сначала выполните /start")
        return

    header = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "tracking_number": tracking_number
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(f"{TRACKING_SERVICE_URL}/parcels/", headers=header, params=params)
        if response.status_code == 200:
            await message.answer("Посылка успешно удалена из списка отслеживания.\nДля просмотра списка посылок выполните /list")
        elif response.status_code == 404:
            await message.answer("Такой посылки не существует в вашем списке.")
        else:
            await message.answer("Не удалось удалить посылку. Повторите попытку позже.")
    except Exception as e:
        await message.answer(f"Ошибка подключения к tracking-сервису:\n{str(e)}")
    return
