from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Request, HTTPException, Depends, Response
from starlette.responses import RedirectResponse, JSONResponse
from app.dependencies import oauth
from app.config import settings
from app.db import session_db_adapter
from sqlalchemy.orm import Session
from app.models import User
import uuid

router = APIRouter()

@router.get('/auth/login')
async def login(request: Request):
    print("Session data before redirect:", request.state.session)
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

# Helper function to get user by email
def get_user_by_email(email: str, db=Depends(session_db_adapter)):
    return db.query(User).filter(User.email == email).first()

# Helper function to create new user
def create_user(db: Session, user_info = Depends(fastapi_users.get_current_active_user)):
    db_user = User(email=user_info['email'], name=user_info['name'], picture=user_info['picture'])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# OAuth callback route
@router.get('/auth')
async def auth(request: Request):
    try:
        print("Session data at callback:", request.state.session)
        token = await oauth.google.authorize_access_token(request)
        user_info = await oauth.google.parse_id_token(request, token)
        request.state.session['user'] = dict(user_info)
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/dashboard")
    except OAuthError as error:
        print(f"Error during OAuth process: {error.error}, {error.description}")
        raise HTTPException(status_code=400, detail="Authentication failed")

# Refresh access token if needed
async def refresh_access_token_if_needed(user: User, db: Session):
    print("Refreshing access token if needed...")

    if not user.refresh_token:
        print(f"User {user.email} has no refresh token. Cannot refresh access token.")
        raise HTTPException(status_code=401, detail="User has no refresh token. Please log in again.")

    if datetime.now(timezone.utc) >= user.access_token_expiry:
        print("Access token expired, attempting to refresh...")
        try:
            token = await oauth.google.refresh_token(token_url=oauth.google.token_url, refresh_token=user.refresh_token)
        except Exception as e:
            print(f"Error refreshing token for user {user.email}: {e}")
            raise HTTPException(status_code=401, detail="Failed to refresh access token")

        if not token:
            print("Failed to retrieve a new access token during refresh.")
            raise HTTPException(status_code=401, detail="Failed to refresh access token")

        print(f"Got new access token for user {user.email}")
        user.access_token_expiry = datetime.now(timezone.utc) + timedelta(seconds=token.get('expires_in'))
        db.commit()
        return token.get('access_token')

    print("Access token is still valid.")
    return None  # Token is still valid

# Check session and refresh access token if necessary
@router.get("/auth/check-session")
async def check_session(request: Request):
    print("Checking session data...")
    user_data = request.state.session.get('user')
    if not user_data:
        print("No user data in session.")
        raise HTTPException(status_code=401, detail="User not authenticated")

    db = SessionLocal()
    user = get_user_by_email(db, user_data['email'])
    if not user:
        print(f"User not found in the database: {user_data['email']}")
        raise HTTPException(status_code=401, detail="User not found")

    print(f"User {user.email} found. Checking token expiry and refreshing if necessary.")
    access_token = await refresh_access_token_if_needed(user, db)
    return {"message": "Session is valid", "access_token": access_token}

# Sign out and clear session
@router.post("/auth/signout")
async def sign_out(request: Request, response: Response):
    request.state.session.clear()  # Clear all session data
    response.delete_cookie("session")  # Delete the session cookie or token
    response.status_code = 204
    return response