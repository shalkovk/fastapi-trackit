from fastapi import FastAPI
from api.routes.auth import router as auth_router
from db.database import engine, Base

app = FastAPI()

app.include_router(auth_router)


@app.on_event("startup")
async def on_startup():
    from db.models import models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
