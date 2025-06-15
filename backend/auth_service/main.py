from fastapi import FastAPI
from db.database import Base, engine

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/ping")
async def ping():
    return {"ok": True, "message": "Pong"}
