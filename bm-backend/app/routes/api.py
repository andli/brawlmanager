from fastapi import APIRouter, Depends, HTTPException, Request
from app.dependencies import oauth
from app.db import get_db, SessionLocal
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from app.models import Team, User

router = APIRouter()

# Refactored function to get the authenticated user
def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_email = request.user.email
    user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.get("/user")
def get_user(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/teams")
def get_teams(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teams = db.query(Team).filter(Team.owner_id == current_user.id).options(joinedload(Team.players)).all()
    print("list teams " + str(teams))
    return teams

# Define the CreateTeamRequest class here
class CreateTeamRequest(BaseModel):
    name: str
    race: str

@router.post("/teams")
def create_team(team_data: CreateTeamRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    print("got team" + str(team_data))

    # Check if the user already has a team
    existing_team = db.query(Team).filter(Team.owner_id == current_user.id).first()
    if (existing_team):
        raise HTTPException(status_code=400, detail="User already has a team.")

    new_team = Team(name=team_data.name, race=team_data.race, owner_id=current_user.id)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return new_team
