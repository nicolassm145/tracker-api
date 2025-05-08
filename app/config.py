from dotenv import load_dotenv
import os

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
PSN_API_KEY = os.getenv("PSN_API_KEY")