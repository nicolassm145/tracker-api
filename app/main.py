from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse 
from app.routes import steam_routes, playstation_routes, xbox_routes, igdb_routes
from app.database.database import engine
from app.models import user_model
from app.routes.user_routes import router as user_router
import os

app = FastAPI(
    title="Tracker API",
    description="API para rastreamento de jogos e conquistas entre múltiplas plataformas",
    version="1.0.0"
)

# Configure CORS
# Em desenvolvimento aceita localhost, em produção aceita o domínio do frontend
origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite
    "http://localhost:5174",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    # Frontend em produção (Vercel)
    "https://nexus-achievement-tracker.vercel.app",
]

# Se tiver a variável FRONTEND_URL no ambiente, adiciona ela
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

@app.get("/", tags=["Root"])
async def root():
    """Endpoint raiz - Verificar se a API está funcionando"""
    return {
        "message": "Tracker API está rodando!",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "online"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
