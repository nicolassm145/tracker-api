import requests
from app.config import IGDB_CLIENT_ID, IGDB_ACCESS_TOKEN
import os

def get_trending_games() -> list:
    url = "https://api.igdb.com/v4/games"
    headers = {
        "Client-ID": IGDB_CLIENT_ID,
        "Authorization": f"Bearer {IGDB_ACCESS_TOKEN}"
    }

    body = """
    fields name, cover.image_id, total_rating, total_rating_count;
    sort total_rating_count desc;
    where cover != null & total_rating != null;
    limit 6;
    """

    response = requests.post(url, headers=headers, data=body)
    response.raise_for_status()
    games = response.json()

    # Monta a URL da capa usando image_id
    for game in games:
        if "cover" in game:
            game["cover_url"] = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{game['cover']['image_id']}.jpg"

    return games