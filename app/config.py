from dotenv import load_dotenv
import os

load_dotenv()

STEAM_API_KEY = os.getenv("STEAM_API_KEY")
DEBUG = os.getenv("DEBUG") == "True"