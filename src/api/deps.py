from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.db_session import SessionLocal


async def get_db_session() -> AsyncSession:
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
