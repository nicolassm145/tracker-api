from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.schemas.user_schema import UserCreate, UserOut
from app.services.user_service import create_user, get_user_by_email

router = APIRouter(prefix="/user", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registra um novo usuário.
    
    :param user: Dados do usuário a serem registrados.
    :param db: Sessão do banco de dados.
    :return: O usuário criado.
    """
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    return create_user(db, user)

