import requests
from app.config import XBOX_API_KEY

BASE_URL = "https://xbl.io/api/v2"

def getPlayerXUID(gamertag: str) -> dict:
    url = f"{BASE_URL}/search/{gamertag}"
    headers = {
        "X-Authorization": XBOX_API_KEY
    }
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data.get("people", [])[0] if data.get("people") else {}
    except requests.RequestException as e:
        print(f"Erro ao buscar XUID: {e}")
        return {}

def getPlayerAchievements(xuid: str) -> dict:
    url = f"{BASE_URL}/achievements/player/{xuid}"
    headers = {
        "X-Authorization": XBOX_API_KEY
    }
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data
    except requests.RequestException as e:
        return {}