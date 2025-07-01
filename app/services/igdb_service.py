from fastapi import HTTPException
import requests
from datetime import datetime, timedelta
from app.config import IGDB_CLIENT_ID, IGDB_ACCESS_TOKEN
url = "https://api.igdb.com/v4"
headers = {
    "Client-ID": IGDB_CLIENT_ID,
    "Authorization": f"Bearer {IGDB_ACCESS_TOKEN}"
}

def get_trending_games() -> list:
    
    current_time = int(datetime.now().timestamp())
    someday_time = int((datetime.now() - timedelta(days=30)).timestamp())
    body = f"""
    fields name, cover.image_id, total_rating, total_rating_count, first_release_date;
    where cover != null 
        & total_rating != null
        & first_release_date >= {someday_time}
        & first_release_date <= {current_time};
    sort total_rating_count desc;
    limit 6;
    """
    response = requests.post(f"{url}/games", headers=headers, data=body)
    response.raise_for_status()
    games = response.json()
    for game in games:
        if game.get("cover"):
            image_id = game["cover"]["image_id"]
            game["cover_url"] = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{image_id}.jpg"
    return games

def get_upcoming_games(days_ahead: int = 150, limit: int = 100) -> list:
    now_ts = int(datetime.now().timestamp())
    future_ts = int((datetime.now() + timedelta(days=days_ahead)).timestamp())

    upcoming = []
    seen_ids = set()
    query = f"""
        fields date,
               game.id,
               game.name,
               game.cover.image_id;
        where date > {now_ts}
          & date <= {future_ts}
          & game != null;
        sort date asc;
        limit {limit};
        """
    resp = requests.post(f"{url}/release_dates", headers=headers, data=query)
    resp.raise_for_status()
    entries = resp.json()
        

    for e in entries:
        g = e.get("game") or {}
        gid = g.get("id")
        img = (g.get("cover") or {}).get("image_id")
        if not gid or not img or gid in seen_ids:
            continue
        seen_ids.add(gid)

        upcoming.append({
                "id":           gid,
                "name":         g["name"],
                "release_date": datetime.fromtimestamp(e["date"]).strftime("%Y-%m-%d"),
                "cover_url":    f"https://images.igdb.com/igdb/image/upload/t_cover_big/{img}.jpg"
        })


    return upcoming

def get_anticipated_games(days_ahead: int = 365, limit: int = 100) -> list:
    now_ts = int(datetime.now().timestamp())
    future_ts = int((datetime.now() + timedelta(days=days_ahead)).timestamp())

    body = f"""
    fields name, hypes, cover.image_id, first_release_date;
    where first_release_date > {now_ts}
      & first_release_date <= {future_ts}
      & hypes != null
      & cover != null;
    sort hypes desc;
    limit {limit};
    """

    resp = requests.post(f"{url}/games", headers=headers, data=body)
    resp.raise_for_status()
    games = resp.json()

    anticipated = []
    for game in games:
        image_id = game["cover"]["image_id"]
        anticipated.append({
            "id": game["id"],
            "name": game["name"],
            "hypes": game.get("hypes", 0),
            "release_date": datetime.fromtimestamp(game["first_release_date"]).strftime("%Y-%m-%d"),
            "cover_url": f"https://images.igdb.com/igdb/image/upload/t_cover_big/{image_id}.jpg"
        })

    return anticipated

def get_game_by_id(game_id: int) -> dict:
    body = f"""
    fields name, 
           summary, 
           cover.image_id, 
           first_release_date, 
           genres.name, 
           platforms.name, 
           involved_companies.company.name, 
           screenshots.*, 
           similar_games.name, 
           similar_games.cover.image_id;
    where id = {game_id};
    """
    
    response = requests.post(f"{url}/games", headers=headers, data=body)
    response.raise_for_status()
    games = response.json()
    
    if not games:
        return None
    
    game = games[0]
    
    # Processar imagens
    if game.get("cover"):
        image_id = game["cover"]["image_id"]
        game["cover_url"] = f"https://images.igdb.com/igdb/image/upload/t_cover_big/{image_id}.jpg"
    
    # Processar data de lançamento
    if game.get("first_release_date"):
        game["release_date"] = datetime.fromtimestamp(game["first_release_date"]).strftime("%Y-%m-%d")
    
    # Processar screenshots
    for screenshot in game.get("screenshots", []):
        screenshot["url"] = f"https://images.igdb.com/igdb/image/upload/t_1080p/{screenshot['image_id']}.jpg"

    
    # Processar empresas
    game["companies"] = [comp["company"]["name"] 
                         for comp in game.get("involved_companies", []) 
                         if comp.get("company")]
    
    # Processar jogos similares
    for similar in game.get("similar_games", []):
        if similar.get("cover"):
            similar["cover_url"] = f"https://images.igdb.com/igdb/image/upload/t_cover_small/{similar['cover']['image_id']}.jpg"
    
    return game