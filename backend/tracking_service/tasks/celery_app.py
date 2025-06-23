from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery("tracking_serive", broker=os.getenv(
    "CELERY_BROKER_URL"), backend=os.getenv("CELERY_RESULT_BACKEND"))

celery_app.conf.timezone = "UTC"

celery_app.conf.beat_schedule = {
    "update-parcels-every-30min": {
        "task": "tasks.update_parcels.update_parcels",
        "schedule": 60 * 30
    }
}
