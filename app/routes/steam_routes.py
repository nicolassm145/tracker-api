from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
import json
from app.services.steam_service import getPlayerSummary, getOwnedGames

router = APIRouter(prefix="/steam", tags=["Steam"])

@router.get("/profile/{steamid}")
def steam_profile(steamid):
    profile = getPlayerSummary(steamid)
    if not profile:
        raise HTTPException(status_code=404, detail="Usuário Steam não encontrado")
    return Response(content=json.dumps(profile, indent=2, ensure_ascii=False), media_type="application/json")

@router.get("/profile/games/{steamid}")
def profile_games(steamid):
    games = getOwnedGames(steamid)
    if not games:
        raise HTTPException(status_code=404, detail="Usuário Steam não encontrado")
    return Response(content=json.dumps(games, indent=2, ensure_ascii=False))
