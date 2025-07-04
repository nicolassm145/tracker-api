from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class GeneralStatsBase(BaseModel):
    total_games: int = 0
    total_platinums: int = 0
    recent_games: int = 0
    total_achievements: int = 0
    total_hours: int = 0
    avg_platinums: int = 0

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    steam_id: str | None = None
    xbox_id: str | None = None
    psn_id: str | None = None
    general_stats: GeneralStatsBase | None = None

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    login: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

