from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import httpx
import os

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    telegram_id = message.from_user.id
    api_url = os.getenv("AUTH_SERVICE_URL", "http://localhost:8000")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{api_url}/auth/telegram-login",
                params={"telegram_id": telegram_id}
            )
            if response.status_code == 200:
                await message.answer(f"Вы авторизованы! \nВаш токен записан.", parse_mode="Markdown")
            else:
                await message.answer(f"Ошибка авторизации. Попробуйте позже.")
    except Exception as e:
        await message.answer(f"Ошибка подключения к auth-сервису:\n{str(e)}")
