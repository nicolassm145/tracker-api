from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
import json
from app.services.xbox_service import getAccountInfo

router = APIRouter(prefix="/xbox", tags=["Xbox"])

@router.get("/profile/{gamertag}")
def xbox_profile(gamertag : str):
    profile = getAccountInfo(gamertag)
    if not profile:
        raise HTTPException(status_code=404, detail="Usuário Xbox não encontrado")
    return Response(content=json.dumps(profile, indent=2, ensure_ascii=False))
