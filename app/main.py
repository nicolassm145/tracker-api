from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse 
from app.routes import steam_routes, playstation_routes, xbox_routes, igdb_routes

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL do seu frontend Vite 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(steam_routes.router)
app.include_router(playstation_routes.router)
app.include_router(xbox_routes.router)
app.include_router(igdb_routes.router)

# @app.get("/", include_in_schema=False)
# def root():
#     return RedirectResponse(url="/users")