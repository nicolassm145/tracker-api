from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
import json
from app.services.xbox_service import getPlayerXUID, getPlayerAchievements, getPlayerAchievementsByGame
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

# Retorna as conquistas do usuário Xbox
@router.get("/profile/achievements/{xuid}")
def xbox_achievements(xuid: str):
    achievements = getPlayerAchievements(xuid)
    if not achievements or "titles" not in achievements:
        raise HTTPException(status_code=404, detail="Conquistas não encontradas")
    
    jogos_filtrados = []
    for jogo in achievements["titles"]:
        jogos_filtrados.append({
            "nome": jogo.get("name"),
            "titleId": jogo.get("titleId"),
            "ultimaVezJogado": jogo.get("titleHistory", {}).get("lastTimePlayed"),
            "conquistas": jogo.get("achievement", {}).get("currentAchievements"),
            "totalConquistas": jogo.get("achievement", {}).get("totalAchievements"),
            "icone": jogo.get("displayImage"),
            "horasJogadas": None,  # Não disponível no retorno
            "horasTotais": None    # Não disponível no retorno
        })
    return {"jogos": jogos_filtrados}

# Retorna as conquistas de um jogo específico do usuário Xbox
@router.get("/profile/achievements/game/{xuid}/{game_id}")
def xbox_achievements_by_game(xuid: str, game_id: str):
    achievements = getPlayerAchievementsByGame(xuid, game_id)
    if not achievements:
        raise HTTPException(status_code=404, detail="Conquistas não encontradas")
    return {"achievements": achievements}