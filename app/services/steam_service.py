import requests
import re
from typing import Dict, List, Optional
from app.config import STEAM_API_KEY

BASE_URL = "https://api.steampowered.com"

def resolveVanityURL(vanity_url: str) -> Optional[str]:
    """
    Resolve uma URL personalizada do Steam para obter o Steam ID
    """
    url = f"{BASE_URL}/ISteamUser/ResolveVanityURL/v1"
    params = {
        "key": STEAM_API_KEY,
        "vanityurl": vanity_url
    }
    
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json().get("response", {})
        
        if data.get("success") == 1:
            return data.get("steamid")
        return None
    except requests.RequestException:
        return None

def extractVanityFromURL(profile_url: str) -> Optional[str]:
    """
    Extrai o vanity URL de uma URL completa do perfil Steam
    """
    # Padrões comuns de URLs do Steam
    patterns = [
        r"steamcommunity\.com/id/([^/]+)",
        r"steamcommunity\.com/profiles/(\d+)",
        r"steamcommunity\.com/user/([^/]+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, profile_url)
        if match:
            return match.group(1)
    
    return None

def getPlayerSummary(steamid: str) -> dict:
    url = f"{BASE_URL}/ISteamUser/GetPlayerSummaries/v2"
    params = {
        "key": STEAM_API_KEY,
        "steamids": steamid
    }

    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json().get("response", {})
    players = data.get("players", [])
    return players[0] if players else {}

def getOwnedGames(steamid: str) -> dict:
    url = f"{BASE_URL}/IPlayerService/GetOwnedGames/v1"
    params = {
        "key": STEAM_API_KEY,
        "steamid": steamid,
        "include_appinfo": True,
        "include_played_free_games": True,
        "appsids_filter": None
    }

    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json().get("response", {})

def getPlayerAchievements(steamid: str, appid: int) -> dict:
    """
    Obtém conquistas de um jogo específico para um usuário
    """
    url = f"{BASE_URL}/ISteamUserStats/GetPlayerAchievements/v1"
    params = {
        "key": STEAM_API_KEY,
        "steamid": steamid,
        "appid": appid,
        "l": "portuguese"  # Idioma para descrições
    }
    
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json().get("playerstats", {})
    except requests.RequestException:
        return {}

def getGameAchievementSchema(appid: int) -> list:
    """
    Retorna o schema de conquistas de um jogo, incluindo ícones.
    """
    url = f"{BASE_URL}/ISteamUserStats/GetSchemaForGame/v2/"
    params = {
        "key": STEAM_API_KEY,
        "appid": appid,
        "l": "portuguese" 
    }

    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json().get("game", {}).get("availableGameStats", {}).get("achievements", [])
    except requests.RequestException:
        return []

def getGlobalAchievementPercentagesForApp(appid: int) -> dict:
    """
    Obtém estatísticas globais de conquistas para um jogo
    """
    url = f"{BASE_URL}/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2"
    params = {
        "gameid": appid
    }
    
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        return resp.json().get("achievementpercentages", {})
    except requests.RequestException:
        return {}

def getPlayerProfileInfo(profile_url: str) -> Dict:
    """
    Função principal que obtém informações completas do perfil Steam
    """
    try:
        # Extrair vanity URL da URL completa
        vanity_url = extractVanityFromURL(profile_url)
        if not vanity_url:
            return {"error": "URL do perfil inválida"}
        
        # Resolver vanity URL para Steam ID
        steamid = resolveVanityURL(vanity_url)
        if not steamid:
            return {"error": "Perfil não encontrado"}
        
        # Obter informações básicas do perfil
        player_summary = getPlayerSummary(steamid)
        if not player_summary:
            return {"error": "Não foi possível obter informações do perfil"}
        
        # Obter jogos possuídos
        owned_games = getOwnedGames(steamid)
        games = owned_games.get("games", [])
        
        # Calcular estatísticas
        total_games = len(games)
        total_playtime = sum(game.get("playtime_forever", 0) for game in games)
        
        # Obter conquistas dos jogos mais jogados (top 5)
        top_games = sorted(games, key=lambda x: x.get("playtime_forever", 0), reverse=True)[:5]
        achievements_data = []
        
        for game in top_games:
            appid = game.get("appid")
            if appid:
                achievements = getPlayerAchievements(steamid, appid)
                if achievements:
                    achievements_data.append({
                        "appid": appid,
                        "name": game.get("name", "Desconhecido"),
                        "achievements": achievements.get("achievements", []),
                        "total_achievements": len(achievements.get("achievements", [])),
                        "achieved_achievements": len([a for a in achievements.get("achievements", []) if a.get("achieved") == 1])
                    })
        
        # Calcular total de conquistas
        total_achievements = sum(game["achieved_achievements"] for game in achievements_data)
        total_possible_achievements = sum(game["total_achievements"] for game in achievements_data)
        
        return {
            "steamid": steamid,
            "profile_info": {
                "personaname": player_summary.get("personaname"),
                "avatarfull": player_summary.get("avatarfull"),
                "profileurl": player_summary.get("profileurl"),
                "realname": player_summary.get("realname"),
                "loccountrycode": player_summary.get("loccountrycode"),
                "timecreated": player_summary.get("timecreated")
            },
            "statistics": {
                "total_games": total_games,
                "total_playtime_minutes": total_playtime,
                "total_playtime_hours": round(total_playtime / 60, 2),
                "total_achievements": total_achievements,
                "total_possible_achievements": total_possible_achievements,
                "achievement_percentage": round((total_achievements / total_possible_achievements * 100) if total_possible_achievements > 0 else 0, 2)
            },
            "games": games,
            "top_games_achievements": achievements_data
        }
        
    except Exception as e:
        return {"error": f"Erro ao processar perfil: {str(e)}"}

def getPlayerStats(steamid: str) -> Dict:
    """
    Função simplificada para obter apenas estatísticas básicas
    """
    try:
        owned_games = getOwnedGames(steamid)
        games = owned_games.get("games", [])
        
        total_games = len(games)
        total_playtime = sum(game.get("playtime_forever", 0) for game in games)
        
        return {
            "total_games": total_games,
            "total_playtime_minutes": total_playtime,
            "total_playtime_hours": round(total_playtime / 60, 2),
            "games_count": total_games
        }
        
    except Exception as e:
        return {"error": f"Erro ao obter estatísticas: {str(e)}"}
