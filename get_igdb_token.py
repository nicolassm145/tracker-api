import os
import requests
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("IGDB_CLIENT_ID")
client_secret = os.getenv("TWITCH_CLIENT_SECRET")

def generate_access_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    response = requests.post(url, data=params)

    if response.status_code == 200:
        data = response.json()
        print("\n✅ Access token gerado com sucesso:")
        print(f"IGDB_ACCESS_TOKEN={data['access_token']}")
        print(f"(Expira em {data['expires_in']} segundos)\n")
    else:
        print("❌ Erro ao gerar o token:")
        print(response.status_code, response.text)

if __name__ == "__main__":
    generate_access_token()
