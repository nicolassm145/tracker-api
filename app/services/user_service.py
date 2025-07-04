from sqlalchemy.orm import Session
from app.models.user_model import User, GeneralStats
from app.schemas.user_schema import UserCreate
from app.utils.security import hash_password

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Cria as estatísticas gerais e associa ao usuário
    create_general_stats(db, db_user)

    return db_user

def get_user_by_email(db: Session, email: str) -> User | None:

    return db.query(User).filter(User.email == email).first()

def get_user_by_login(login: str, db: Session):
    return db.query(User).filter((User.email == login) | (User.username == login)).first()

def update_steam_id(db: Session, user: User, steam_id: str) -> User:

    user.steam_id = steam_id # type: ignore
    db.commit()
    db.refresh(user)
    return user

def create_general_stats(db: Session, user: User) -> GeneralStats:
    stats = GeneralStats()
    db.add(stats)
    db.commit()
    db.refresh(stats)
    user.general_stats_id = stats.id
    db.commit()
    db.refresh(user)
    return stats

def get_general_stats_by_id(db: Session, stats_id: int) -> GeneralStats | None:
    return db.query(GeneralStats).filter(GeneralStats.id == stats_id).first()

def update_general_stats(db: Session, stats: GeneralStats, **kwargs) -> GeneralStats:
    for key, value in kwargs.items():
        if hasattr(stats, key):
            setattr(stats, key, value)
    db.commit()
    db.refresh(stats)
    return stats