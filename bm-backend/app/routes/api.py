from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import oauth

from app.db import get_db, SessionLocal
from sqlalchemy.orm import Session, joinedload

from pydantic import BaseModel
from app.models import Team, User

router = APIRouter()


@router.get("/user")
def get_user(db: Session = Depends(get_db)):
    user_id = 1  # Replace with logic to get the authenticated user's ID
    user = db.query(User).filter(User.id == user_id).first()
    return user

@router.get("/teams")
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(Team).options(joinedload(Team.players)).all()
    print("list teams " + str(teams))
    return teams


# Define the CreateTeamRequest class here
class CreateTeamRequest(BaseModel):
    name: str
    race: str

@router.post("/teams")
def create_team(team_data: CreateTeamRequest, db: Session = Depends(get_db)):
    user_id = 1  # Replace with logic to get the authenticated user's ID
    user = db.query(User).filter(User.id == user_id).first()
    print("got team" + str(team_data))

    # Check if the user already has a team
    existing_team = db.query(Team).filter(Team.owner_id == user_id).first()
    if existing_team:
        raise HTTPException(status_code=400, detail="User already has a team.")

    new_team = Team(name=team_data.name, race=team_data.race, owner_id=user.id)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return new_team

