from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.db import get_async_session
from app.models import MatchResult, Team
import random
import asyncio
from datetime import datetime

router = APIRouter()

# WebSocket function to send real-time match updates and start the match
async def send_match_updates(websocket: WebSocket, home_team: Team, away_team: Team, tick_speed: float, db: Session):
    await websocket.accept()
    home_score = 0
    away_score = 0

    try:
        # Simulate two halves (16 turns each)
        for half in range(2):
            for turn in range(16):
                await websocket.send_text(f"Turn {turn + 1} of half {half + 1}")
                
                # Randomly simulate scoring for home or away team
                if random.random() < 0.5:
                    home_score += 1
                    await websocket.send_text(f"{home_team.name} scored! Home Score: {home_score}")
                else:
                    away_score += 1
                    await websocket.send_text(f"{away_team.name} scored! Away Score: {away_score}")

                await asyncio.sleep(tick_speed)

            await websocket.send_text(f"End of half {half + 1}. Current Score: {home_team.name} {home_score} - {away_team.name} {away_score}")

        await websocket.send_text(f"Final Score: {home_team.name} {home_score} - {away_team.name} {away_score}")

        # Log the match result in the database
        match_result = MatchResult(
            home_team_id=home_team.id,
            away_team_id=away_team.id,
            home_score=home_score,
            away_score=away_score,
            finished_at=datetime.utcnow(),
        )
        db.add(match_result)
        db.commit()

    except WebSocketDisconnect:
        print("WebSocket connection disconnected")
        return

    finally:
        await websocket.close()  # Ensure the WebSocket is closed when the match is over
        print("WebSocket connection closed after match completion")

# WebSocket route to start the match and stream updates
@router.websocket("/ws/match")
async def websocket_endpoint(
    websocket: WebSocket,
    home_team_id: int, 
    away_team_id: int, 
    tick_speed: float,
    db: Session = Depends(get_async_session)
):
    # Validate that both teams exist
    home_team = db.query(Team).filter(Team.id == home_team_id).first()
    away_team = db.query(Team).filter(Team.id == away_team_id).first()

    if not home_team or not away_team:
        await websocket.close(code=1003)  # Close WebSocket with an error code
        return

    await send_match_updates(websocket, home_team, away_team, tick_speed, db)