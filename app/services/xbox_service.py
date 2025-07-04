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

def getPlayerAchievementsByGame(xuid: str, game_id: str) -> dict:
    url = f"{BASE_URL}/achievements/player/{xuid}/{game_id}"
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


def is_valid_platform_game(devices: list) -> bool:
    """
    Filtra jogos que tenham as plataformas PC, XboxSeries e XboxOne.
    """
    if not devices:
        return False
    
    # Lista de plataformas válidas
    valid_platforms = ["PC", "XboxSeries", "XboxOne"]
    
    # Verifica se pelo menos uma das plataformas válidas está presente
    return any(platform in devices for platform in valid_platforms)


def getPlayerGamesWithFullAchievements(xuid: str, page: int = 1, limit: int = 5) -> list:
    jogos_data = getPlayerAchievements(xuid)
    if not jogos_data or "titles" not in jogos_data:
        return []

    start = (page - 1) * limit
    end = start + limit
    jogos_paginados = jogos_data["titles"][start:end]

    jogos_resultado = []
    for jogo in jogos_paginados:
        title_id = jogo.get("titleId")
        if not title_id:
            continue

        conquistas_data = getPlayerAchievementsByGame(xuid, title_id)
        achievements = conquistas_data.get("achievements", [])

        jogos_resultado.append({
            "name": jogo.get("name"),
            "titleId": title_id,
            "displayImage": jogo.get("displayImage"),
            "lastTimePlayed": jogo.get("titleHistory", {}).get("lastTimePlayed"),
            "achievements": achievements,
        })

    return jogos_resultado