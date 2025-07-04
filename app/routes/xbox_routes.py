from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
import json
from app.services.xbox_service import getPlayerXUID, getPlayerAchievements
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
    if not achievements:
        raise HTTPException(status_code=404, detail="Conquistas não encontradas")
    
    # Retornar a resposta completa para debug
    return Response(
        content=json.dumps(achievements, indent=2, ensure_ascii=False),
        media_type="application/json"
    )