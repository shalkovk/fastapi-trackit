from tasks.celery_app import celery_app
from db.database import get_db, SessionLocal
from db.models.models import Parcel
from sqlalchemy.future import select
from utils.track24 import get_parcel_status
from utils.notify import send_status_update


@celery_app.task(name="tasks.update_parcels.update_parcels")
def update_parcels():
    import asyncio
    asyncio.run(_update_parcels_async())


async def _update_parcels_async():
    async with SessionLocal() as db:
        try:
            result = await db.execute(select(Parcel))
            parcels = result.scalars().all()

            for parcel in parcels:
                try:
                    parcel_data = await get_parcel_status(parcel.tracking_number)
                    if not parcel_data:
                        continue

                    status_changed = parcel.status != parcel_data["status"]
                    carrier_changed = parcel.carrier != parcel_data["carrier"]

                    if status_changed or carrier_changed:
                        parcel.status = parcel_data["status"]
                        parcel.carrier = parcel_data["carrier"]
                        parcel.last_update = parcel_data["last_update"]

                        if getattr(parcel, "owner_telegram_id", None):
                            await send_status_update(parcel)

                except Exception as e:
                    print(
                        f"[!] Ошибка при обновлении {parcel.tracking_number}: {e}")

            await db.commit()

        except Exception as e:
            print(f"[!] Ошибка общей обработки посылок: {e}")
