from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, db_url: str):
        self.engine = create_async_engine(db_url, echo=True)  # FIXME delete arg echo
        self.session_factory = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        self._scoped_session_factory = async_scoped_session(
            self.session_factory, scopefunc=current_task
        )

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        session = self._scoped_session_factory()
        try:
            yield session
        finally:
            await session.close()

    async def check_db(self):
        async with self.engine.connect() as conn:
            await conn.execute(text("select 1"))

    async def dispose_db(self):
        await self.engine.dispose()
