from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.simulation import simulate_match

router = APIRouter()

# Hardcoded team IDs for now
HOME_TEAM_ID = 1
AWAY_TEAM_ID = 3


@router.post("/startmatch")
async def start_match(db: Session = Depends(get_db), tick_speed: float = None):
    try:
        # Start the match simulation asynchronously
        match_result = await simulate_match(HOME_TEAM_ID, AWAY_TEAM_ID, db, tick_speed)
        
        return {
            "message": "Match completed",
            "home_team_id": match_result.home_team_id,
            "away_team_id": match_result.away_team_id,
            "home_score": match_result.home_score,
            "away_score": match_result.away_score,
            "finished_at": match_result.finished_at
        }
    except Exception as e:
        return {"error": str(e)}