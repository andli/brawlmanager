from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Request, HTTPException, Depends, Response
from starlette.responses import RedirectResponse, JSONResponse
from app.dependencies import oauth

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
        user.refresh_token = token.get('refresh_token')
        access_token_expiry = datetime.utcnow() + timedelta(seconds=token.get('expires_in'))
        user.access_token_expiry = access_token_expiry

        db.commit()

        # Store the user's email in the session
        request.session['user'] = {'email': user.email}
        
        print(f"Session after login: {request.session}")

        return RedirectResponse(url="http://localhost:3000/dashboard")
    
    except ValueError as ve:
        return JSONResponse(status_code=500, content={"message": "Invalid token response"})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})

async def refresh_access_token_if_needed(user: User, db: Session):
    # if datetime.now(timezone.utc) >= user.access_token_expiry:
    #     # Access token expired, refresh it
    #     token = await oauth.google.refresh_token(token_url=oauth.google.token_url, refresh_token=user.refresh_token)
        
    #     if not token:
    #         raise HTTPException(status_code=401, detail="Failed to refresh access token")
        
    #     # Update user's access token and expiry
    #     user.access_token_expiry = datetime.now(timezone.utc) + timedelta(seconds=token.get('expires_in'))
    #     db.commit()
    #     return token.get('access_token')

    return None  # Token is still valid

@router.get("/auth/check-session")
async def check_session(request: Request):
    user_data = request.session.get('user')
    if not user_data:
        raise HTTPException(status_code=401, detail="User not authenticated")

    db = SessionLocal()
    user = get_user_by_email(db, user_data['email'])
    
    if user:
        access_token = await refresh_access_token_if_needed(user, db)
        return {"message": "Session is valid", "access_token": access_token}
    
    raise HTTPException(status_code=401, detail="Invalid session")


@router.post("/auth/signout")
async def sign_out(request: Request, response: Response):
    request.session.clear()  # Clear all session data
    response.delete_cookie("session")  # Delete the session cookie or token
    response.status_code = 204
    return response
