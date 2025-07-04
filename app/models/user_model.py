from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
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

    general_stats_id = Column(Integer, ForeignKey("general_stats.id"), nullable=True)
    general_stats = relationship("GeneralStats", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"

class GeneralStats(Base):
    __tablename__ = "general_stats"

    id = Column(Integer, primary_key=True, index=True)
    total_games = Column(Integer, default=0)
    total_platinums = Column(Integer, default=0)
    recent_games = Column(Integer, default=0)
    total_achievements = Column(Integer, default=0)
    total_hours = Column(Integer, default=0)
    avg_platinums = Column(Integer, default=0)

    user = relationship("User", back_populates="general_stats", uselist=False)

