from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
import json
from app.services.playstation_service import getProfileInfo

router = APIRouter(prefix="/psn", tags=["Playstation"])

@router.get("/profile/{psnid}")
def psn_profile(psnid: str):
    info = getProfileInfo(psnid)
    if not info:
        raise HTTPException(status_code=404, detail="Usuário PSN não encontrado")
    return info
