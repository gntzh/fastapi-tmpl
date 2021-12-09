from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user import User
from .base import FactoryMixin


class UserRepo(FactoryMixin):
    model = User
    _session: AsyncSession

    async def get(self, /, id: UUID) -> User | None:
        return (
            await self._session.execute(select(self.model).filter_by(id=id))
        ).scalar()

    async def get_by_username(self, /, username: str) -> User | None:
        return (
            await self._session.execute(select(self.model).filter_by(username=username))
        ).scalar()

    async def get_by_email(self, /, email: str) -> User | None:
        return (
            await self._session.execute(select(self.model).filter_by(email=email))
        ).scalar()
