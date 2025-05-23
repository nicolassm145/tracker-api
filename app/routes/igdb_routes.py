from fastapi import APIRouter, HTTPException
from app.services.igdb_service import get_trending_games

router = APIRouter(prefix="/igdb", tags=["IGDB"])

@router.get("/trending")
def trending_games():
    try:
        games = get_trending_games()
        return games
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
