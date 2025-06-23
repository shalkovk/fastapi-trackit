from fastapi import FastAPI
from api.routes.parcels import router as parcels_router

app = FastAPI()

app.include_router(parcels_router)
