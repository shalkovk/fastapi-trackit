from fastapi import FastAPI
from db.database import Base, engine
from db.models import models

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    print("⏳ Running create_all...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created.")


@app.get("/ping")
async def ping():
    return {"ok": True, "message": "Pong"}
