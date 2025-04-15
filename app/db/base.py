from app.core.config import Config
from typing import AsyncIterator

from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine

from sqlalchemy.orm import sessionmaker

config = Config()

engine = AsyncEngine(create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True, future=True))
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        print("called get_session")
        yield session
