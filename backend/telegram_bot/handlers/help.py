from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from redis_client import redis_client as redis


router = Router()


@router.message(Command("help"))
async def handler_help(message: Message):
    telegram_id = message.from_user.id
    token = redis.get(f"token:{telegram_id}")
    if not token:
        await message.answer(f"Вы не авторизованы. Сначала выполните /start")
        return
    text = f"Возможности бота TrackIt 🤖\n1) /start - выполнить авторизацию (сперва выолните эту команду, чтобы пользоваться ботом);\n2) /help - просмотр всех возможностей бота (это сообщение - результат команды /help);\n3) /list - просмотр списка всех отслеживаемых Вами посылок;\n4) /track <трек-номер> - отслеживать статус посылки (убедитесь в валидности/корректности трек-номера перед использованием команды);\n5) /delete <трек-номер> - удалить посылку из списка отслеживаемых посылок."
    await message.answer(text)
