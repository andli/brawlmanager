from fastapi import Request, APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from app.dependencies import google_oauth_client as oauth
from app.db import get_async_session
from sqlalchemy import func, case
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from app.models import Team, User, Player, MatchResult

router = APIRouter()

def get_current_user(request: Request, db: Session = Depends(get_async_session)) -> User:
    user_info = request.state.session.get('user')  # Retrieve the user dict
    if not user_info:
        raise HTTPException(status_code=401, detail="User not authenticated (api.py)")
    
    user_email = user_info.get('email')  # Extract the email from the dict
    if not user_email:
        raise HTTPException(status_code=401, detail="User email not found in session")

    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

@router.get("/user")
def get_user(db: Session = Depends(get_async_session), user: User = Depends(get_current_user)):
    if user:
        return user
    raise HTTPException(status_code=401, detail="User not authenticated (api.py)")


@router.get("/teams")
def get_teams(current_user: User = Depends(get_current_user), db: Session = Depends(get_async_session)):
    teams = db.query(Team).filter(Team.owner_id == current_user.id).options(joinedload(Team.players)).all()
    return teams

from sqlalchemy import func, case

@router.get("/allteams")
def get_teams(current_user: User = Depends(get_current_user), db: Session = Depends(get_async_session)):
    # Subquery to count wins for both home and away teams
    win_count_subquery = (
        db.query(
            Team.id.label("team_id"),
            func.count(
                case(
                    (MatchResult.home_team_id == Team.id, MatchResult.home_score > MatchResult.away_score)
                )
            ).label("home_wins"),
            func.count(
                case(
                    (MatchResult.away_team_id == Team.id, MatchResult.away_score > MatchResult.home_score)
                )
            ).label("away_wins")
        )
        .outerjoin(MatchResult, (MatchResult.home_team_id == Team.id) | (MatchResult.away_team_id == Team.id))
        .group_by(Team.id)
        .subquery()
    )

    # Main query to select teams and their win counts
    teams = (
        db.query(
            Team.id,
            Team.name,
            Team.race,
            func.coalesce(win_count_subquery.c.home_wins, 0).label("home_wins"),
            func.coalesce(win_count_subquery.c.away_wins, 0).label("away_wins"),
            (func.coalesce(win_count_subquery.c.home_wins, 0) + func.coalesce(win_count_subquery.c.away_wins, 0)).label("total_wins")
        )
        .outerjoin(win_count_subquery, win_count_subquery.c.team_id == Team.id)
        .all()
    )

    # Convert the query result to a list of dictionaries (JSON-serializable)
    result = []
    for team in teams:
        result.append({
            "id": team.id,
            "name": team.name,
            "race": team.race,
            "home_wins": team.home_wins,
            "away_wins": team.away_wins,
            "total_wins": team.total_wins
        })

    # Return the sorted result using FastAPI's jsonable_encoder to ensure proper encoding
    return jsonable_encoder(sorted(result, key=lambda x: x["total_wins"], reverse=True))
                                                           
# Define the CreateTeamRequest class here
class CreateTeamRequest(BaseModel):
    name: str
    race: str

@router.post("/teams")
def create_team(team_data: CreateTeamRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_async_session)):

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
def create_player(player_data: CreatePlayerRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_async_session)):

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