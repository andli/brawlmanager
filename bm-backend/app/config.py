import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "brawlmanager"
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL")
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    SECRET_KEY: str = os.getenv("SECRET_KEY")

settings = Settings()