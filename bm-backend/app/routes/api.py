from fastapi import Request, APIRouter, Depends, HTTPException
from app.dependencies import oauth
from app.db import get_db, SessionLocal
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from app.models import Team, User, Player

router = APIRouter()

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    user_info = request.session.get('user')  # Retrieve the user dict
    if not user_info:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    user_email = user_info.get('email')  # Extract the email from the dict
    if not user_email:
        raise HTTPException(status_code=401, detail="User email not found in session")

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

@router.get("/user")
def get_user(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user:
        return user
    raise HTTPException(status_code=401, detail="User not authenticated")


@router.get("/teams")
def get_teams(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teams = db.query(Team).filter(Team.owner_id == current_user.id).options(joinedload(Team.players)).all()
    return teams

@router.get("/allteams")
def get_teams(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    teams = db.query(Team).all()
    return teams

# Define the CreateTeamRequest class here
class CreateTeamRequest(BaseModel):
    name: str
    race: str

@router.post("/teams")
def create_team(team_data: CreateTeamRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    # Check if the user already has a team
    existing_team = db.query(Team).filter(Team.owner_id == current_user.id).first()
    if (existing_team):
        raise HTTPException(status_code=400, detail="User already has a team.")

    new_team = Team(name=team_data.name, race=team_data.race, owner_id=current_user.id)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return new_team

class CreatePlayerRequest(BaseModel):
    name: str
    role: str
    race: str
    stats: list[int]  # Array of integers representing player stats
    team_id: int      # Foreign key to link the player to a team

@router.post("/players")
def create_player(player_data: CreatePlayerRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    # Check if the team exists and belongs to the current user
    team = db.query(Team).filter(Team.id == player_data.team_id, Team.owner_id == current_user.id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found or you do not have access to this team.")

    # Create the new player
    new_player = Player(
        name=player_data.name,
        role=player_data.role,
        race=player_data.race,
        stats=player_data.stats,
        team_id=player_data.team_id  # Associate player with the team
    )
    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return new_player