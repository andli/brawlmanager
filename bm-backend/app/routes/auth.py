from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Request, HTTPException, Depends, Response
from starlette.responses import RedirectResponse, JSONResponse
from app.dependencies import oauth
from app.config import settings
from app.db import get_db, SessionLocal
from sqlalchemy.orm import Session
from app.models import User
import uuid

router = APIRouter()


@router.get('/auth/login')
async def login(request: Request):
    print("Session data before redirect:", request.state.session)
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

# Store state in session and initiate OAuth flow
""" @router.get("/auth/login")
async def login(request: Request):
    redirect_uri = str(request.url_for('auth'))
    client = oauth.google

    # Generate a unique state
    state = str(uuid.uuid4())

    # Generate the authorization URL
    authorization_response = await client.create_authorization_url(
        redirect_uri=redirect_uri,
        state=state,
        access_type='offline',
        prompt='consent'
    )

    # Extract the URL from the response
    authorization_url = authorization_response['url']

    # Save the state in the session
    request.state.session['state'] = state
    print(f"Login: state stored in session: {state}")

    # Create a JSON response with the OAuth URL
    response = JSONResponse({"oauth_url": authorization_url})

    return response
 """

# Helper function to get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Helper function to create new user
def create_user(db: Session, user_info: dict):
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

""" @router.get("/auth")
async def auth(request: Request):
    try:
        # Retrieve and validate the state parameter
        state_in_session = request.state.session.get('state')
        state_in_request = request.query_params.get('state')
        print(f"State in session: {state_in_session}, State in request: {state_in_request}")
        
        if state_in_session != state_in_request:
            print("State mismatch: CSRF warning!")
            return JSONResponse(status_code=400, content={"message": "CSRF Warning: State mismatch"})

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
        if refresh_token:
            user.refresh_token = refresh_token
            print(f"Refresh token saved for user: {user.email}")
        else:
            print("No refresh token received from Google")

        access_token_expiry = datetime.utcnow() + timedelta(seconds=token.get('expires_in'))
        user.access_token_expiry = access_token_expiry
        db.commit()

        # Store the user's email in the session
        request.state.session['user'] = {'email': user.email}
        print(f"Session after login: {request.state.session}")

        frontend_url = settings.FRONTEND_URL
        return RedirectResponse(url=f"{frontend_url}/dashboard")
    
    except Exception as e:
        print(f"Error during OAuth process: {e}")
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"}) """

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