import os
from httpx import AsyncClient, HTTPError
from dotenv import load_dotenv
import httpx
from pathlib import Path
from datetime import datetime, timezone

env_path = Path(__file__).resolve().parents[1] / ".env"

load_dotenv(dotenv_path=env_path)

TRACK24_API_TOKEN = os.getenv("TRACK24_API_TOKEN")
TRACK24_DOMAIN = os.getenv("TRACK24_DOMAIN", "localhost")
TRACK24_API_URL = "https://api.track24.ru/tracking.json.php"


async def get_parcel_status(tracking_number: str) -> dict:
    params = {
        "apiKey": TRACK24_API_TOKEN,
        "domain": TRACK24_DOMAIN,
        "pretty": "true",
        "code": tracking_number
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(TRACK24_API_URL, params=params)
            print(
                f"Track24 raw response for {tracking_number}:", response.text)

        response.raise_for_status()

        json_data = response.json()

        if json_data.get("status") == "ok":
            data = json_data.get("data", {})
            return {
                "status": (
                    "delivered"
                    if data.get("deliveredStatus") == "1"
                    else "awaiting" if data.get("awaitingStatus") == "1"
                    else "in_transit"
                ),
                "carrier": data.get("groupedCompanyNames", ["Unknown"])[0],
                "last_update": datetime.utcnow().replace(tzinfo=None),
            }

        print(
            f"Track24 API error for {tracking_number}: {json_data.get('message')}")
        return None

    except HTTPError as e:
        print(f"HTTP error while requesting Track24: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error while parsing Track24 response: {e}")
        return None
