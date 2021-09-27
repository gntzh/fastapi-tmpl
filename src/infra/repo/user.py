from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.user import User


class UserRepo:
    def __init__(self, model):
        self.model = model

    async def get(self, db: Session, /, id: UUID) -> User | None:
        return (await db.execute(select(self.model).filter_by(id=id))).scalar()

    async def get_by_username(self, db: Session, /, username: str) -> User | None:
        return (
            await db.execute(select(self.model).filter_by(username=username))
        ).scalar()

    async def get_by_email(self, db: Session, /, email: str) -> User | None:
        return (await db.execute(select(self.model).filter_by(email=email))).scalar()


user_repo = UserRepo(User)
