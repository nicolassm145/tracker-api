from fastapi import FastAPI
from fastapi.responses import RedirectResponse 
from app.routes import steam_routes, playstation_routes, xbox_routes

app = FastAPI()

app.include_router(steam_routes.router)
app.include_router(playstation_routes.router)
app.include_router(xbox_routes.router)

# @app.get("/", include_in_schema=False)
# def root():
#     return RedirectResponse(url="/users")