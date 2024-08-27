from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from app.config import settings

# Database URL from settings
DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

# Initialize the Database connection
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a MetaData instance
metadata = MetaData()

# Base class for ORM models
Base = declarative_base()

# Create the tables in the database (only if they don't exist)
def init_db():
    # Import the models here to ensure they are registered properly before creating the tables
    from app.models import User  # Import the model(s) here
    Base.metadata.create_all(bind=engine)

# Call init_db() to ensure the tables are created
init_db()