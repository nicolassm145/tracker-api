from fastapi import APIRouter, HTTPException, Query 
from fastapi.responses import Response
import json
from app.services.xbox_service import getPlayerXUID, getPlayerAchievements, getPlayerAchievementsByGame, is_valid_platform_game, getPlayerGamesWithFullAchievements
from app.services.user_service import update_xbox_id
from app.routes.user_routes import get_current_user, get_db
from app.models.user_model import User
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter(prefix="/xbox", tags=["Xbox"])



# Retorna apenas o XUID do usuário Xbox
@router.get("/profile/xuid/{gamertag}")
def xbox_xuid(gamertag : str):
    xuid_data = getPlayerXUID(gamertag)
    if not xuid_data:
        raise HTTPException(status_code=404, detail="XUID não encontrado")
    
    # Extrair apenas o XUID do objeto
    xuid = xuid_data.get("xuid")
    if not xuid:
        raise HTTPException(status_code=404, detail="XUID não encontrado no perfil")
    
    return {"xuid": xuid}

# Salva o XUID no usuário autenticado.
@router.post("/save-xboxid")
def save_xboxid(xboxid: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    update_xbox_id(db, current_user, xboxid)
    return {"xboxid": xboxid}

# Retorna as conquistas do usuário Xbox (apenas PC, XboxSeries e XboxOne)
@router.get("/profile/achievements/{xuid}")
def xbox_achievements(xuid: str):
    achievements = getPlayerAchievements(xuid)
    if not achievements or "titles" not in achievements:
        raise HTTPException(status_code=404, detail="Conquistas não encontradas")
    
    jogos_filtrados = []
    for jogo in achievements["titles"]:
        devices = jogo.get("devices", [])
        
        # Filtra apenas jogos que tenham PC, XboxSeries ou XboxOne
        if is_valid_platform_game(devices):
            jogos_filtrados.append({
                "name": jogo.get("name"),
                "titleId": jogo.get("titleId"),
                "displayImage": jogo.get("displayImage"),
                "lastTimePlayed": jogo.get("titleHistory", {}).get("lastTimePlayed")
            })
    
    return {"jogos": jogos_filtrados}

# Retorna as conquistas de um jogo específico do usuário Xbox
@router.get("/profile/achievements/game/{xuid}/{game_id}")
def xbox_achievements_by_game(xuid: str, game_id: str):
    achievements = getPlayerAchievementsByGame(xuid, game_id)
    if not achievements:
        raise HTTPException(status_code=404, detail="Conquistas não encontradas")
    return {"achievements": achievements}

@router.get("/profile/games-with-full-achievements/{xuid}")
def xbox_games_with_full_achievements(
    xuid: str,
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=50)
):
    jogos = getPlayerGamesWithFullAchievements(xuid, page=page, limit=limit)
    if not jogos:
        raise HTTPException(status_code=404, detail="Jogos ou conquistas não encontradas")
    return {"jogos": jogos}

@router.get("/profile/achievements/all/{xuid}")
def xbox_all_achievements(
    xuid: str,
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=50)
):
    achievements = getPlayerAchievements(xuid)
    if not achievements or "titles" not in achievements:
        raise HTTPException(status_code=404, detail="Conquistas não encontradas")

    jogos_filtrados = []
    for jogo in achievements["titles"]:
        devices = jogo.get("devices", [])
        if is_valid_platform_game(devices):
            jogos_filtrados.append(jogo)
    start = (page - 1) * limit
    end = start + limit
    jogos_paginados = jogos_filtrados[start:end]
    jogos_resultado = []
    for jogo in jogos_paginados:
        title_id = jogo.get("titleId")
        if not title_id:
            continue
        conquistas_data = getPlayerAchievementsByGame(xuid, title_id)
        achievements_list = conquistas_data.get("achievements", [])
        jogos_resultado.append({
            "name": jogo.get("name"),
            "titleId": title_id,
            "displayImage": jogo.get("displayImage"),
            "lastTimePlayed": jogo.get("titleHistory", {}).get("lastTimePlayed"),
            "achievements": achievements_list,
        })
    return {"jogos": jogos_resultado}