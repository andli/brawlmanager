import os
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware 
from app.routes import auth, api
from app.db import database

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://bm-frontend:3000"],  # Update with the specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers (e.g., Content-Type, Authorization)
)

# Fetch the secret key from the environment variable
secret_key = os.getenv("SECRET_KEY", "default-secret-key")

# Add SessionMiddleware with the secret key from the environment
app.add_middleware(SessionMiddleware, secret_key=secret_key)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(auth.router, prefix="/api")
app.include_router(api.router, prefix="/api")