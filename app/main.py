from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse 
from app.routes import steam_routes, playstation_routes, xbox_routes, igdb_routes
from app.database.database import engine
from app.models import user_model
from app.routes.user_routes import router as user_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://achievement-tracker-shar.onrender.com/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(steam_routes.router)
app.include_router(playstation_routes.router)
app.include_router(xbox_routes.router)
app.include_router(igdb_routes.router)


user_model.Base.metadata.create_all(bind=engine)
app.include_router(user_router)
