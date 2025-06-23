import os
import asyncio
import json
from aio_pika import connect_robust, IncomingMessage
from dotenv import load_dotenv
import httpx

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
QUEUE_NAME = os.getenv("QUEUE_NAME", "parcel_status_updates")


async def send_telegram_message(telegram_id: int, message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": telegram_id,
        "text": message
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
        except Exception as e:
            print(f"[!] Ошибка при отправке Telegram-сообщения: {e}")


async def handle_message(message: IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body.decode())
            telegram_id = data["telegram_id"]
            tracking_number = data["tracking_number"]
            status = data["new_status"]
            carrier = data.get("carrier", "Unknown")
            last_update = data.get("last_update", "")

            text = (
                f"📦 Обновление по посылке `{tracking_number}`\n\n"
                f"🗂 Статус: *{status.upper()}*\n"
                f"🚛 Перевозчик: {carrier}\n"
                f"🕒 Обновлено: {last_update}"
            )

            await send_telegram_message(telegram_id, text)
            print(f"[+] Уведомление отправлено пользователю {telegram_id}")
        except Exception as e:
            print(f"[!] Ошибка обработки сообщения: {e}")


async def main():
    print("[*] Notification service запущен.", flush=True)
    connection = await connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    print(f"[*] Слушаем очередь {QUEUE_NAME}...", flush=True)

    await queue.consume(handle_message)
    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
