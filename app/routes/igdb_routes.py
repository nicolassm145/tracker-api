from fastapi import APIRouter, HTTPException
import requests
from app.services.igdb_service import get_game_by_id, get_trending_games, get_upcoming_games, get_anticipated_games

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
  
@router.get("/games/{game_id}")
def get_game_details(game_id: int):
    try:
        game = get_game_by_id(game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        return game
    except requests.HTTPError as err:
        raise HTTPException(status_code=502, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Internal error: {err}")


