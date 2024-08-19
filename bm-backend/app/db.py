from sqlalchemy import create_engine, MetaData
from databases import Database
from app.config import settings

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI
database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)