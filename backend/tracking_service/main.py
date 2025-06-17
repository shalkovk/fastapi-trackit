from fastapi import FastAPI
from api.routes.parcels import router as parcels_router
from db.database import engine, Base
from db.models import models

app = FastAPI()

app.include_router(parcels_router)


@app.on_event("startup")
async def on_startup():
    from db.models import models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
