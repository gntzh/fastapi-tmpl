from typing import Any, Generic, Protocol, Type, TypeVar

from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession


class ModelBase(Protocol):
    id: Any

    def __init__(*args, **kwargs):
        ...


T = TypeVar("T")

ModelT = TypeVar("ModelT", bound=ModelBase)


class FactoryMixin:
    def __call__(self: T, session: AsyncSession) -> T:
        logger.debug("装填Item session")
        self._session = session
        return self


class RepoBase(Generic[ModelT], FactoryMixin):
    model: Type[ModelT]
    _session: AsyncSession

    async def get(self, /, id: Any) -> ModelT | None:
        return (
            await self._session.execute(select(self.model).where(self.model.id == id))
        ).scalar()

    async def get_multi(self, /, offset: int = 0, limit: int = 100) -> list[ModelT]:
        return (
            (
                await self._session.execute(
                    select(self.model).offset(offset).limit(limit)
                )
            )
            .scalars()
            .all()
        )

    async def count(self) -> int:
        return (
            (await self._session.execute(select(func.count(self.model.id))))
            .scalars()
            .one()
        )
