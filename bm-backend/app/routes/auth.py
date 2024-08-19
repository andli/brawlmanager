from fastapi import APIRouter, Depends, Request
from starlette.responses import RedirectResponse
from app.db import database
from app.models import users
from app.dependencies import oauth

router = APIRouter()

@router.get("/auth/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    query = users.insert().values(
        email=user_info.email,
        name=user_info.name,
        picture=user_info.picture
    )
    await database.execute(query)
    return RedirectResponse(url="/")