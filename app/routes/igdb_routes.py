from fastapi import APIRouter, HTTPException
import requests
from app.services.igdb_service import get_trending_games, get_upcoming_games, get_anticipated_games, get_game_details

router = APIRouter(prefix="/igdb", tags=["IGDB"])

@router.get("/trending")
def trending_games():
    try:
        games = get_trending_games()
        return games
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/upcoming")
def upcoming_games():
    try:
        games = get_upcoming_games()
        return games
    except requests.HTTPError as err:
        raise HTTPException(status_code=502, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Erro interno: {err}")
    
@router.get("/anticipated")
def anticipated_games():
    try:
        games = get_anticipated_games()
        return games
    except requests.HTTPError as err:
        raise HTTPException(status_code=502, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Erro interno: {err}")
    

