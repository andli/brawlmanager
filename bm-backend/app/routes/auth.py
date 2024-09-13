from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Request, HTTPException, Depends, Response
from starlette.responses import RedirectResponse, JSONResponse
from app.dependencies import oauth
from app.config import settings

from app.db import get_db, SessionLocal
from sqlalchemy.orm import Session

from app.models import User

router = APIRouter()

@router.get("/auth/login")
async def login(request: Request):
    # Dynamically generate the redirect URI for the OAuth flow
    redirect_uri = request.url_for('auth')
    
    # Initiate the OAuth flow by redirecting to Google's OAuth endpoint
    # `authorize_redirect` will handle state generation internally
    return await oauth.google.authorize_redirect(request, redirect_uri, access_type="offline")


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_info: dict):
    db_user = User(email=user_info['email'], name=user_info['name'], picture=user_info['picture'])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/auth")
async def auth(request: Request):
    try:
        print(f"Request Query Params: {request.query_params}")
        
        # Exchange the authorization code for an access token
        token = await oauth.google.authorize_access_token(request)
        print(f"Token received: {token}")

        # Access user info from the token
        user_info = token.get('userinfo')
        if not user_info:
            return JSONResponse(status_code=500, content={"message": "User info not found in token response"})

        db = SessionLocal()

        # Check if the user already exists
        user = get_user_by_email(db, user_info['email'])
        if not user:
            user = create_user(db, user_info)

        # Save the refresh token and access token expiry
        refresh_token = token.get('refresh_token')
        if not refresh_token:
            print(f"Refresh token is missing for user {user.email}")
            # You can decide whether to raise an error here or proceed, depending on your use case
            # return JSONResponse(status_code=500, content={"message": "Refresh token is missing"})

        user.refresh_token = refresh_token
        access_token_expiry = datetime.utcnow() + timedelta(seconds=token.get('expires_in'))
        user.access_token_expiry = access_token_expiry

        db.commit()

        # Store the user's email in the session
        request.session['user'] = {'email': user.email}
        
        print(f"Session after login: {request.session}")

        frontend_url = settings.FRONTEND_URL

        return RedirectResponse(url=f"{frontend_url}/dashboard")
    
    except ValueError as ve:
        print(f"ValueError during OAuth process: {ve}")
        return JSONResponse(status_code=500, content={"message": "Invalid token response"})
    
    except Exception as e:
        print(f"Exception during OAuth process: {e}")
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

async def refresh_access_token_if_needed(user: User, db: Session):
    print("Refreshing access token if needed...")
    
    if not user.refresh_token:
        print(f"User {user.email} has no refresh token. Cannot refresh access token.")
        raise HTTPException(status_code=401, detail="User has no refresh token. Please log in again.")
    
    if datetime.now(timezone.utc) >= user.access_token_expiry:
        print("Access token expired, attempting to refresh...")
        
        # Access token expired, refresh it
        try:
            token = await oauth.google.refresh_token(token_url=oauth.google.token_url, refresh_token=user.refresh_token)
        except Exception as e:
            print(f"Error refreshing token for user {user.email}: {e}")
            raise HTTPException(status_code=401, detail="Failed to refresh access token")
        
        if not token:
            print("Failed to retrieve a new access token during refresh.")
            raise HTTPException(status_code=401, detail="Failed to refresh access token")
        
        print(f"Got new access token for user {user.email}")
        
        # Update user's access token and expiry
        user.access_token_expiry = datetime.now(timezone.utc) + timedelta(seconds=token.get('expires_in'))
        db.commit()
        print(f"New access token expiry: {user.access_token_expiry}")
        return token.get('access_token')

    print("Access token is still valid.")
    return None  # Token is still valid

@router.get("/auth/check-session")
async def check_session(request: Request):
    print("Checking session data...")
    user_data = request.session.get('user')
    
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

@router.post("/auth/signout")
async def sign_out(request: Request, response: Response):
    request.session.clear()  # Clear all session data
    response.delete_cookie("session")  # Delete the session cookie or token
    response.status_code = 204
    return response