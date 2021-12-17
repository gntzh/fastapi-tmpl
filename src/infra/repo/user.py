from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user import User
from .base import RepoBase


class UserRepo(RepoBase[User]):
    model = User
    _session: AsyncSession

    async def get_by_username(self, /, username: str) -> User | None:
        return (
            await self._session.execute(select(self.model).filter_by(username=username))
        ).scalar()

    async def get_by_email(self, /, email: str) -> User | None:
        return (
            await self._session.execute(select(self.model).filter_by(email=email))
        ).scalar()
