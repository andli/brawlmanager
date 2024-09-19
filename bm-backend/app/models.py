from sqlalchemy import Column, Integer, String, UUID, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped
from sqlalchemy.dialects.postgresql import ARRAY
from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
)
from typing import List
import uuid
from datetime import datetime, timezone, timedelta

class Base(DeclarativeBase):
    pass

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4())) 
    session_data = Column(JSON, nullable=False)  
    expires_at = Column(DateTime(timezone=True), nullable=False) 

    def is_expired(self):
        return datetime.now(timezone.utc) > self.expires_at

class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    __tablename__ = "oauth_account"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="oauth_accounts")

class User(Base, SQLAlchemyBaseUserTableUUID):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True) 
    name = Column(String, nullable=True)
    picture = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    access_token_expiry = Column(DateTime(timezone=True), nullable=True)
    oauth_accounts: Mapped[List[OAuthAccount]] = relationship(
        "OAuthAccount", back_populates="user", lazy="joined"
    )
    teams = relationship("Team", back_populates="owner")



class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    race = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="teams")
    players = relationship("Player", back_populates="team")

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    role = Column(String, nullable=True)
    race = Column(String, nullable=True)
    stats = Column(ARRAY(Integer), nullable=True)
    team_id = Column(Integer, ForeignKey('teams.id'))

    team = relationship("Team", back_populates="players")

class MatchResult(Base):
    __tablename__ = "match_results"
    
    id = Column(Integer, primary_key=True, index=True)
    home_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    away_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    home_score = Column(Integer, nullable=False)
    away_score = Column(Integer, nullable=False)
    finished_at = Column(DateTime, default=datetime.now(timezone.utc))

    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])