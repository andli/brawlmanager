from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse, JSONResponse
from app.db import database
from app.models import users
from app.dependencies import oauth

router = APIRouter()

@router.get("/auth/login")
async def login(request: Request):
    # Dynamically generate the redirect URI for the OAuth flow
    redirect_uri = request.url_for('auth')
    
    # Initiate the OAuth flow by redirecting to Google's OAuth endpoint
    # `authorize_redirect` will handle state generation internally
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth")
async def auth(request: Request):
    try:
        # Attempt to exchange the authorization code for an access token
        token = await oauth.google.authorize_access_token(request)
        print(f"Token received: {token}")

        # Proceed with user info retrieval and other logic
        user_info = await oauth.google.parse_id_token(request, token)
        print(f"User info: {user_info}")

        return RedirectResponse(url="/dashboard")
    except ValueError as ve:
        # Capture more specific error information related to the token
        print(f"ValueError during token exchange: {str(ve)}")
        return JSONResponse(status_code=500, content={"message": "Invalid token response"})
    except Exception as e:
        # General exception handling to capture all other errors
        print(f"Error during token exchange: {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})
        
        # Insert user info into the database
        query = users.insert().values(
            email=user_info['email'],
            name=user_info['name'],
            picture=user_info['picture']
        )
        await database.execute(query)
        print("User info inserted into database")
        
        # Redirect the user to the dashboard
        return RedirectResponse(url="http://localhost:3000/dashboard")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Internal Server Error"})