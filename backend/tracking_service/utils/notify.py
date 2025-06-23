import aio_pika
import json
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / ".env"

load_dotenv(dotenv_path=env_path)

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
QUEUE_NAME = os.getenv("QUEUE_NAME", "parcel_status_updates")


async def send_status_update(parcel):
    try:
        connection = await aio_pika.connect_robust(RABBITMQ_URL)
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)

        message_body = {
            "telegram_id": parcel.owner_telegram_id,
            "tracking_number": parcel.tracking_number,
            "new_status": parcel.status,
            "carrier": parcel.carrier or "Unknown",
            "last_update": str(parcel.last_update)
        }

        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(message_body).encode()),
            routing_key=QUEUE_NAME
        )

        await connection.close()
    except Exception as e:
        print(f"[!] Ошибка при отправке уведомления: {e}")
