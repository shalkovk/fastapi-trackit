from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from dotenv import load_dotenv
import asyncio
import os

from handlers.start import router as start_router

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

dp.include_router(start_router)


async def main():
    await bot.set_my_commands([
        BotCommand(command="start", description="Начать")
    ])
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
