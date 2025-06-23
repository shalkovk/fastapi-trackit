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
                    if parcel_data:
                        parcel.status = parcel_data["status"]
                        parcel.last_update = parcel_data["last_update"]
                        parcel.carrier = parcel_data["carrier"]

                        await send_status_update(parcel)
                except Exception as e:
                    print(
                        f"Ошибка при обновлении {parcel.tracking_number}: {str(e)}")

            await db.commit()
        except Exception as e:
            print(f"Ошибка во время обновления всех посылок: {str(e)}")
