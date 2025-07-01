from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.utils.security import hash_password

def create_user(db: Session, user: UserCreate) -> User:
    """
    Cria um novo usuário no banco de dados.
    
    :param db: Sessão do banco de dados.
    :param user: Dados do usuário a serem criados.
    :return: O usuário criado.
    """
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Obtém um usuário pelo email.
    
    :param db: Sessão do banco de dados.
    :param email: Email do usuário a ser buscado.
    :return: O usuário encontrado ou None se não existir.
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_login(login: str, db: Session):
    return db.query(User).filter((User.email == login) | (User.username == login)).first()