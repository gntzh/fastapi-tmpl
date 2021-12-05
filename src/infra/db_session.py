from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from src.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def check_db():
    async with engine.connect() as conn:
        await conn.execute(text("select 1"))


async def dispose_db():
    await engine.dispose()
