import sys
import random
import asyncio
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import MatchResult, Team


async def simulate_match(home_team_id: int, away_team_id: int, db: Session, tick_speed=None):
    # Fetch teams from the database
    home_team = db.query(Team).filter(Team.id == home_team_id).first()
    away_team = db.query(Team).filter(Team.id == away_team_id).first()

    if not home_team or not away_team:
        raise ValueError("Teams not found")

    home_score = 0
    away_score = 0

    print(f"Starting match between {home_team.name} (Home) and {away_team.name} (Away)")

    # Simulate two halves (16 turns each)
    for half in range(2):
        print(f"Starting half {half + 1}")
        for turn in range(16):
            print(f"Turn {turn + 1} of half {half + 1}")

            # Randomly decide which team gets the first attempt in this turn (home or away)
            teams = [home_team, away_team]
            random.shuffle(teams)  # Shuffle to randomly decide who gets the first attempt

            for team in teams:
                # Randomly select one player from the current team to attempt scoring
                player = random.choice(team.players)
                if random.random() < (player.stats[0] / 10):  # Basic stat-based chance
                    if team == home_team:
                        home_score += 1
                        print(f"{player.name} from {home_team.name} scored! Home Score: {home_score}")
                    else:
                        away_score += 1
                        print(f"{player.name} from {away_team.name} scored! Away Score: {away_score}")
                    # End the turn if a player scores
                    break  # End the turn immediately when a player scores
                sys.stdout.flush()

            # If tick speed is provided, wait between turns
            if tick_speed:
                await asyncio.sleep(tick_speed)

        print(f"End of half {half + 1}. Current Score - {home_team.name}: {home_score}, {away_team.name}: {away_score}")

    print(f"Final Score - {home_team.name}: {home_score}, {away_team.name}: {away_score}")

    # Log the result to the database
    match_result = MatchResult(
        home_team_id=home_team_id,
        away_team_id=away_team_id,
        home_score=home_score,
        away_score=away_score,
        finished_at=datetime.utcnow(),
    )
    db.add(match_result)
    db.commit()

    return match_result