from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
