from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.config import settings
from fastapi_users.db import SQLAlchemyUserDatabase
from app.models import User, OAuthAccount
from typing import AsyncGenerator, List


# Use an async database URL
DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI.replace('postgresql://', 'postgresql+asyncpg://')

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)