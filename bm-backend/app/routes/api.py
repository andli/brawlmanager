from fastapi import Request, APIRouter, Depends, HTTPException
from app.dependencies import oauth
from app.db import get_db, SessionLocal
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from app.models import Team, User

router = APIRouter()

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    print("Checking user in request...")
    user_email = request.session.get('user_email')  # or however you are retrieving the email
    if user_email:
        print(f"User email found in session: {user_email}")
        user = db.query(User).filter(User.email == user_email).first()
        if user:
            print(f"User found: {user.name}")
            return user
        else:
            print("No user found with this email")
    else:
        print("No user email in session")
    raise HTTPException(status_code=401, detail="User not authenticated")


@router.get("/user")
def get_user(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    print("User:", user)
    if user:
        return user
    raise HTTPException(status_code=401, detail="User not authenticated")


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
