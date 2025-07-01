from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    steam_id = Column(String, unique=True, nullable=True)
    xbox_id = Column(String, unique=True, nullable=True)
    psn_id = Column(String, unique=True, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"

