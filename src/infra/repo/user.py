from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


class UserRepo:
    def __init__(self, model):
        self.model = model

    async def get(self, db: AsyncSession, /, id: UUID) -> User | None:
        return (await db.execute(select(self.model).filter_by(id=id))).scalar()

    async def get_by_username(self, db: AsyncSession, /, username: str) -> User | None:
        return (
            await db.execute(select(self.model).filter_by(username=username))
        ).scalar()

    async def get_by_email(self, db: AsyncSession, /, email: str) -> User | None:
        return (await db.execute(select(self.model).filter_by(email=email))).scalar()


user_repo = UserRepo(User)
