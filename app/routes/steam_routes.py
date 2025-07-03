from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import Response
import json
from sqlalchemy.orm import Session
from app.routes.user_routes import get_current_user, get_db
from app.services.user_service import update_steam_id, update_general_stats, get_general_stats_by_id
from app.models.user_model import User
from app.services.steam_service import (
    getPlayerSummary, 
    getOwnedGames,
    getPlayerStats,
    resolveVanityURL,
    getPlayerAchievements,
    getGameAchievementSchema,
    getGlobalAchievementPercentagesForApp
)

router = APIRouter(prefix="/steam", tags=["Steam"])

# Obtém informações básicas do perfil Steam a partir do steamid.
@router.get("/profile/{steamid}")
def steam_profile(steamid):
    profile = getPlayerSummary(steamid)
    if not profile:
        raise HTTPException(status_code=404, detail="Usuário Steam não encontrado")
    return Response(content=json.dumps(profile, indent=2, ensure_ascii=False), media_type="application/json")

# Obtém todos os jogos do usuário a partir do steamid.
@router.get("/profile/games/{steamid}")
def profile_games(steamid):
    games = getOwnedGames(steamid)
    if not games:
        raise HTTPException(status_code=404, detail="Usuário Steam não encontrado")
    return Response(content=json.dumps(games, indent=2, ensure_ascii=False))

# Obtém estatísticas básicas do jogador
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
# Salva o SteamID no usuário autenticado.
@router.post("/save-steamid")
def save_steamid_from_vanity(
    vanity_url: str = Query(..., description="Vanity URL do perfil Steam"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    steamid = resolveVanityURL(vanity_url)
    if not steamid:
        raise HTTPException(status_code=404, detail="Vanity URL não encontrada")
    update_steam_id(db, current_user, steamid)
    return {"steamid": steamid}

# Retorna as conquistas de todos os jogos do usuário a partir do steamid, incluindo ícones.
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

# Atualiza as estatísticas gerais do usuário baseado nos dados do Steam.
@router.post("/update-general-stats")
def update_steam_general_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza as estatísticas gerais do usuário baseado nos dados do Steam.
    """
    if not current_user.steam_id:  # type: ignore
        raise HTTPException(status_code=400, detail="Usuário não possui Steam ID configurado")
    
    if not current_user.general_stats_id:  # type: ignore
        raise HTTPException(status_code=400, detail="Estatísticas gerais não encontradas")
    
    # Buscar estatísticas atuais
    stats = get_general_stats_by_id(db, current_user.general_stats_id)  # type: ignore
    if not stats:
        raise HTTPException(status_code=404, detail="Estatísticas gerais não encontradas")
    
    # Obter dados do Steam
    owned_games = getOwnedGames(current_user.steam_id)  # type: ignore
    games = owned_games.get("games", [])
    
    # Calcular estatísticas
    total_games = len(games)
    total_hours = sum(game.get("playtime_forever", 0) for game in games)
    total_achievements = 0
    total_platinums = 0
    
    # Contar conquistas e platinums
    for game in games:
        appid = game.get("appid")
        if appid:
            achievements = getPlayerAchievements(current_user.steam_id, appid)  # type: ignore
            game_achievements = achievements.get("achievements", [])
            total_achievements += len(game_achievements)
            
            # Considerar platinum se 100% das conquistas foram obtidas
            if game_achievements:
                achieved_count = len([a for a in game_achievements if a.get("achieved") == 1])
                if achieved_count == len(game_achievements):
                    total_platinums += 1
    
    # Jogos recentes (últimos 30 dias - simplificado como jogos com playtime > 0)
    recent_games = len([game for game in games if game.get("playtime_2weeks", 0) > 0])
    
    # Média de platinums (porcentagem de jogos platinados)
    avg_platinums = round((total_platinums / total_games * 100) if total_games > 0 else 0)
    
    # Atualizar estatísticas
    update_general_stats(db, stats,
        total_games=total_games,
        total_platinums=total_platinums,
        recent_games=recent_games,
        total_achievements=total_achievements,
        total_hours=total_hours,
        avg_platinums=avg_platinums
    )
    
    return {
        "message": "Estatísticas atualizadas com sucesso",
        "stats": {
            "total_games": total_games,
            "total_platinums": total_platinums,
            "recent_games": recent_games,
            "total_achievements": total_achievements,
            "total_hours": total_hours,
            "avg_platinums": avg_platinums
        }
    }

# Retorna as estatísticas gerais calculadas a partir do Steam ID. SOMENTE PARA TESTES
@router.get("/general-stats/{steamid}")
def get_steam_general_stats(steamid: str):
    """
    Retorna as estatísticas gerais calculadas a partir do Steam ID.
    """
    # Obter dados do Steam
    owned_games = getOwnedGames(steamid)
    games = owned_games.get("games", [])
    
    # Calcular estatísticas
    total_games = len(games)
    total_hours = sum(game.get("playtime_forever", 0) for game in games)
    total_achievements = 0
    total_platinums = 0
    
    # Contar conquistas e platinums
    for game in games:
        appid = game.get("appid")
        if appid:
            achievements = getPlayerAchievements(steamid, appid)
            game_achievements = achievements.get("achievements", [])
            total_achievements += len(game_achievements)
            
            # Considerar platinum se 100% das conquistas foram obtidas
            if game_achievements:
                achieved_count = len([a for a in game_achievements if a.get("achieved") == 1])
                if achieved_count == len(game_achievements):
                    total_platinums += 1
    
    # Jogos recentes (últimos 30 dias - simplificado como jogos com playtime > 0)
    recent_games = len([game for game in games if game.get("playtime_2weeks", 0) > 0])
    
    # Média de platinums (porcentagem de jogos platinados)
    avg_platinums = round((total_platinums / total_games * 100) if total_games > 0 else 0)
    
    return {
        "steam_id": steamid,
        "general_stats": {
            "total_games": total_games,
            "total_platinums": total_platinums,
            "recent_games": recent_games,
            "total_achievements": total_achievements,
            "total_hours": total_hours,
            "avg_platinums": avg_platinums
        }
    }

@router.get("/rare-achievements/{steamid}")
def get_rare_achievements(steamid: str, rarity_threshold: float = 10.0):

    # Obter jogos do usuário
    owned_games = getOwnedGames(steamid)
    games = owned_games.get("games", [])
    
    all_rare_achievements = []
    
    for game in games:
        appid = game.get("appid")
        name = game.get("name", "Desconhecido")
        
        if appid:
            # Conquistas do jogador
            player_achievements = getPlayerAchievements(steamid, appid)
            player_achs = player_achievements.get("achievements", [])
            
            # Schema de conquistas do jogo (para obter ícones)
            game_schema = getGameAchievementSchema(appid)
            
            # Porcentagem global de cada conquista
            global_percentages = getGlobalAchievementPercentagesForApp(appid)
            global_achs = global_percentages.get("achievements", [])
            
            # Filtrar conquistas raras
            game_rare_achievements = []
            for achievement in player_achs:
                if achievement.get("achieved") == 1:  # Se o jogador tem
                    apiname = achievement.get("apiname")
                    
                    # Buscar porcentagem global
                    for global_ach in global_achs:
                        if global_ach.get("name") == apiname:
                            percentage = global_ach.get("percent", 100.0)
                            if float(percentage) < float(rarity_threshold):
                                # Buscar ícones no schema do jogo
                                icon_url = None
                                icongray_url = None
                                for schema_ach in game_schema:
                                    if schema_ach.get("name") == apiname:
                                        icon_url = schema_ach.get("icon")
                                        icongray_url = schema_ach.get("icongray")
                                        break
                                
                                game_rare_achievements.append({
                                    "apiname": apiname,
                                    "name": achievement.get("name"),
                                    "description": achievement.get("description"),
                                    "icon": icon_url,
                                    "icongray": icongray_url,
                                    "unlocktime": achievement.get("unlocktime"),
                                    "global_percentage": percentage
                                })
                            break
            
            if game_rare_achievements:
                all_rare_achievements.append({
                    "appid": appid,
                    "game_name": name,
                    "rare_achievements": game_rare_achievements,
                    "total_rare": len(game_rare_achievements)
                })
    
    response_data = {
        "steam_id": steamid,
        "rarity_threshold": f"< {rarity_threshold}%",
        "total_games_with_rare": len(all_rare_achievements),
        "total_rare_achievements": sum(game["total_rare"] for game in all_rare_achievements),
        "games": all_rare_achievements
    }
    
    return Response(
        content=json.dumps(response_data, indent=2, ensure_ascii=False), 
        media_type="application/json"
    )
