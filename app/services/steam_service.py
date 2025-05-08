import requests
from app.config import STEAM_API_KEY

BASE_URL = "https://api.steampowered.com"

def getPlayerSummary(steamid: str) -> dict:
    
    url = f"{BASE_URL}/ISteamUser/GetPlayerSummaries/v2"
    params = {
        "key": STEAM_API_KEY,
        "steamids": steamid
    }

    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json().get("response", {})
    # players = data.get("players", [])
    # return players[0] if players else {}