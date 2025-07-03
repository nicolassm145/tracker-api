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
    resolveVanityURL,
    getPlayerAchievements,
    getGameAchievementSchema
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

@router.get("/profile/achievements/{steamid}")
def all_games_achievements(steamid: str):
    owned_games = getOwnedGames(steamid)
    games = owned_games.get("games", [])
    achievements_list = []

    for game in games:
        appid = game.get("appid")
        name = game.get("name", "Desconhecido")

        if appid:
            # Pega conquistas do jogador
            player_achievements = getPlayerAchievements(steamid, appid).get("achievements", [])
            # Pega o schema com os ícones
            schema_achievements = getGameAchievementSchema(appid)

            # Cria um dicionário para mapear por API name
            schema_map = {a["name"]: a for a in schema_achievements}

            # Enriquecer cada conquista com ícone
            enriched_achievements = []
            for ach in player_achievements:
                schema = schema_map.get(ach.get("apiname"))
                enriched_achievements.append({
                    "name": ach.get("name"),
                    "apiname": ach.get("apiname"),
                    "achieved": ach.get("achieved"),
                    "unlocktime": ach.get("unlocktime"),
                    "icon": schema.get("icon") if schema else None,
                    "icongray": schema.get("icongray") if schema else None,
                    "description": schema.get("description") if schema else "",
                })

            achievements_list.append({
                "appid": appid,
                "name": name,
                "achievements": enriched_achievements,
                "total_achievements": len(enriched_achievements),
                "achieved_achievements": len([a for a in enriched_achievements if a["achieved"] == 1])
            })

    return Response(content=json.dumps(achievements_list, indent=2, ensure_ascii=False), media_type="application/json")

