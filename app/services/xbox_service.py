import requests
from app.config import XBOX_API_KEY

BASE_URL = "https://xbl.io/api/v2"

def getAccountInfo(gamertag: str) -> dict:
    url = f"{BASE_URL}/search/{gamertag}"
    headers = {
        "X-Authorization": XBOX_API_KEY
    }

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    people = data.get("people", [])
    return people[0] if people else {}