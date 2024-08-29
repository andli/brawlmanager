from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User, Team, Player

router = APIRouter()

@router.get("/user")
def get_user(db: Session = Depends(get_db)):
    # Replace with logic to get the authenticated user's ID
    user_id = 1
    user = db.query(User).filter(User.id == user_id).first()
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "picture": user.picture,
        "teams": [{"id": team.id, "name": team.name} for team in user.teams]
    }

@router.get("/teams")
def get_teams(db: Session = Depends(get_db)):
    user_id = 1  # Replace with logic to get the authenticated user's ID
    teams = db.query(Team).filter(Team.owner_id == user_id).all()
    return [{
        "id": team.id,
        "name": team.name,
        "race": team.race,
        "players": [{
            "id": player.id,
            "name": player.name,
            "role": player.role,
            "race": player.race,
            "stats": player.stats
        } for player in team.players]
    } for team in teams]
