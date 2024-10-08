# main.py
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, api, match
from app.db import engine, create_db_and_tables
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    #secret_key=settings.SECRET_KEY,
    #samesite='lax',        # Use 'lax' for development
    #   https_only=False,      # Set to False to avoid setting 'Secure' attribute
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