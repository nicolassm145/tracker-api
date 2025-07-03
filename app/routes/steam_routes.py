from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import Response
import json
from sqlalchemy.orm import Session
from app.routes.user_routes import get_current_user, get_db
from app.services.user_service import update_steam_id
from app.models.user_model import User
from app.services.steam_service import (
    getPlayerSummary, 
    getOwnedGames, 
    getPlayerProfileInfo, 
    getPlayerStats,
    resolveVanityURL
)

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

@router.get("/profile/complete")
def complete_profile(profile_url: str = Query(..., description="URL completa do perfil Steam")):
    """
    Obtém informações completas do perfil Steam a partir da URL
    """
    profile_data = getPlayerProfileInfo(profile_url)
    
    if "error" in profile_data:
        raise HTTPException(status_code=400, detail=profile_data["error"])
    
    return Response(
        content=json.dumps(profile_data, indent=2, ensure_ascii=False), 
        media_type="application/json"
    )

@router.get("/profile/stats/{steamid}")
def player_stats(steamid: str):
    """
    Obtém estatísticas básicas do jogador
    """
    stats = getPlayerStats(steamid)
    
    if "error" in stats:
        raise HTTPException(status_code=400, detail=stats["error"])
    
    return Response(
        content=json.dumps(stats, indent=2, ensure_ascii=False), 
        media_type="application/json"
    )

@router.post("/save-steamid")
def save_steamid_from_vanity(
    vanity_url: str = Query(..., description="Vanity URL do perfil Steam"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Resolve uma vanity URL, salva o SteamID no usuário autenticado e retorna o steam_id salvo.
    """
    steamid = resolveVanityURL(vanity_url)
    if not steamid:
        raise HTTPException(status_code=404, detail="Vanity URL não encontrada")
    update_steam_id(db, current_user, steamid)
    return {"steamid": steamid}
