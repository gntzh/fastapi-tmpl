from typing import Any, Generic, Protocol, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ModelBase(Protocol):
    id: Any

    def __init__(*args, **kwargs):
        ...


ModelT = TypeVar("ModelT", bound=ModelBase)


class RepoBase(Generic[ModelT]):
    def __init__(self, model: Type[ModelT]) -> None:
        self.model = model

    async def get(self, db: AsyncSession, /, id: Any) -> ModelT | None:
        return (
            await db.execute(select(self.model).where(self.model.id == id))
        ).scalar()

    async def get_multi(
        self, db: AsyncSession, /, offset: int = 0, limit: int = 100
    ) -> list[ModelT]:
        return (
            (await db.execute(select(self.model).offset(offset).limit(limit)))
            .scalars()
            .all()
        )
