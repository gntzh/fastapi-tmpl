from sqlalchemy import select

from src.domain.item import Item
from src.libs.sa.uuid import UUID

from .base import RepoBase


class ItemRepo(RepoBase[Item]):
    model = Item

    async def get_multi_by_owner(
        self, /, owner_id: UUID, offset: int = 0, limit: int = 100
    ) -> list[Item]:
        return (
            (
                await self._session.execute(
                    select(self.model)
                    .where(Item.owner_id == owner_id)
                    .offset(offset)
                    .limit(limit)
                )
            )
            .scalars()
            .all()
        )
