import requests
from app.config import PSN_API_KEY
from psnawp_api import PSNAWP

psnawp = PSNAWP(PSN_API_KEY)

client = psnawp.me()

def getProfileInfo(online_id: str) -> dict:
    user = psnawp.user(online_id=online_id)
    if not user or not user.online_id:
        return {}

    return {
        "online_id": user.online_id,
        "account_id": user.account_id,
        "region": user.get_region(),
    }