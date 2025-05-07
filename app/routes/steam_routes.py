from fastapi import APIRouter, HTTPException
from app.services.steam_service import getPlayerSummary

router = APIRouter(prefix="/steam", tags=["Steam"])

@router.get("/profile/{steamid}")
def steam_profile(steamid):
    profile = getPlayerSummary(steamid)
    if not profile:
        raise HTTPException(status_code=404, detail="Usuário Steam não encontrado")
    return profile
