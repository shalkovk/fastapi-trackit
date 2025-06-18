from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from sqlalchemy.future import select
from db.models.models import Parcel
from schemas.schemas import ParcelCreate, ParcelRead
from utils.auth import get_current_user

router = APIRouter(
    prefix="/parcels",
    tags=["Parcels 📦"]
)


@router.post("/")
async def create_parcel(parcel: ParcelCreate, telegram_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Parcel).where(Parcel.tracking_number == parcel.tracking_number))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=400, detail="Tracking number already exists")
    new_parcel = Parcel(tracking_number=parcel.tracking_number, carrier=None,
                        owner_telegram_id=telegram_id, status="created")
    db.add(new_parcel)
    await db.commit()
    await db.refresh(new_parcel)
    return new_parcel


@router.get("/list")
async def get_user_parcels(telegram_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Parcel).where(Parcel.owner_telegram_id == telegram_id))
    parcels = result.scalars().all()
    if not parcels:
        raise HTTPException(status_code=404, detail="Parcels not found")
    return parcels


@router.patch("/{tracking_number}/status")
async def update_status(tracking_number: str, status: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Parcel).where(Parcel.tracking_number == tracking_number))
    parcel = result.scalar_one_or_none()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")
    parcel.status = status
    await db.commit()
    return {"ok": True, "message": "Status updated"}


@router.delete("/")
async def delete_parcels(tracking_number: str, telegram_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Parcel).where(Parcel.tracking_number == tracking_number))
    parcel = result.scalar_one_or_none()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")
    await db.delete(parcel)
    await db.commit()
    return {"ok": True, "message": "Parcel deleted"}
