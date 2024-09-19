# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, api, match
from app.db import engine
from app.config import settings

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the custom Postgres session middleware with proper cookie settings
app.add_middleware(
    CORSMiddleware,
    secret_key=settings.SECRET_KEY,
    samesite='lax',        # Use 'lax' for development
    https_only=False,      # Set to False to avoid setting 'Secure' attribute
    max_age=14 * 24 * 60 * 60,
)

# Connect to the database on startup
@app.on_event("startup")
async def startup():
    await engine.connect()

# Disconnect from the database on shutdown
@app.on_event("shutdown")
async def shutdown():
    await engine.disconnect()

# Include the routers
app.include_router(auth.router, prefix="/api")
app.include_router(api.router, prefix="/api")
app.include_router(match.router, prefix="/api")