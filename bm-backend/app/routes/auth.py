from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse, JSONResponse
from app.db import database, SessionLocal
from app.models import User
from app.dependencies import oauth
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/auth/login")
async def login(request: Request):
    # Dynamically generate the redirect URI for the OAuth flow
    redirect_uri = request.url_for('auth')
    
    # Initiate the OAuth flow by redirecting to Google's OAuth endpoint
    # `authorize_redirect` will handle state generation internally
    return await oauth.google.authorize_redirect(request, redirect_uri)



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
        # Log the request parameters
        print(f"Request Query Params: {request.query_params}")
        
        # Attempt to exchange the authorization code for an access token
        token = await oauth.google.authorize_access_token(request)
        print(f"Token received: {token}")

        # Access user info from the token
        user_info = token.get('userinfo')
        if user_info:
            print(f"User info: {user_info}")
        else:
            print("User info not found in token")
            return JSONResponse(status_code=500, content={"message": "User info not found in token response"})

        # Database session
        db = SessionLocal()

        # Check if the user already exists
        user = get_user_by_email(db, user_info['email'])
        if not user:
            user = create_user(db, user_info)

        # Use the user object as needed
        print(f"User retrieved or created: {user}")
        
        return RedirectResponse(url="http://localhost:3000/dashboard")
    
    except ValueError as ve:
        print(f"ValueError during token exchange: {str(ve)}")
        return JSONResponse(status_code=500, content={"message": "Invalid token response"})
    
    except Exception as e:
        print(f"General error during token exchange: {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})